# @version 0.3.3
# @License Copyright (c) Swap.Dance, 2022 - all rights reserved
# @Author Alexey K
# Swap.Dance Deployer

interface SUPER:
    def drop_distribution_balances(
        _tokens: address[10]
    ) -> bool: nonpayable

interface ERC20D:
    def lock() -> bool: view
    def token_a() -> address: view
    def token_b() -> address: view
    def name() -> String[32]: view
    def symbol() -> String[32]: view
    def decimals() -> uint256: view
    def pair_params() -> uint256: view
    def pot_station() -> address: view
    def totalSupply() -> uint256: view
    def balanceOf(_station: address) -> uint256: view

event NewOwner:
    old_owner: indexed(address)
    new_owner: indexed(address)
    
event NewGuardian:
    guardian: indexed(address)

# Variables
done: bool
owner_agree: bool
guardian_agree: bool
owner: public(address)
guardian: public(address)
exchange_count: public(uint256)
approved_tokens: public(HashMap[address, bool])
approved_for_reward: public(HashMap[address, bool])
pot_station_list: public(HashMap[address, address])
exchange_info: public(HashMap[uint256, uint256])
exchange_pairs_list: public(HashMap[uint256, address])

# Constants
STATION: immutable(address)
SWD_TOKEN: immutable(address)
SUPER_POOL: immutable(address)
POT_STATION: immutable(address)
MAX_STEPS: constant(int128) = 30


@external
def __init__(
    _swd_token: address,
    _super_pool: address,
    _pot_station: address,
    _station: address,
):
    self.owner = msg.sender
    SWD_TOKEN = _swd_token
    SUPER_POOL = _super_pool
    POT_STATION = _pot_station
    STATION = _station
    

@external
def register_new_pool(
        _token_a: address,
        _token_b: address,
        _token_fees_a: uint256,
        _token_fees_b: uint256,
        _station_type: uint256
) -> bool:
    decimal_diff_a: uint256 = empty(uint256)
    decimal_diff_b: uint256 = empty(uint256)
    decimal_a: uint256 = ERC20D(_token_a).decimals()
    decimal_b: uint256 = ERC20D(_token_b).decimals()
    token_pair: uint256 = bitwise_xor(convert(_token_a, uint256), convert(_token_b, uint256))
    assert self.exchange_pairs_list[token_pair] == ZERO_ADDRESS, "Pair already exist"
    assert _token_a not in [STATION, ZERO_ADDRESS]
    assert _token_b not in [STATION, ZERO_ADDRESS]
    assert msg.sender == STATION, "Wrong sender"
    assert _token_a != _token_b, "Token1 = Token2"
    assert _station_type <= 1, "Wrong station type"
    assert decimal_a != 0 and decimal_b != 0, "Token decimal cant be zero"
    assert _token_fees_a >= 1 and _token_fees_a <= 99, "Wrong Token Fees"
    assert _token_fees_b >= 1 and _token_fees_b <= 99, "Wrong Token Fees"

    if decimal_a == 18 and decimal_b == 18:
        decimal_diff_a = 1
        decimal_diff_b = 1
    elif decimal_a < 18 and decimal_b < 18:
        decimal_diff_a = pow_mod256(10, 18 - decimal_a)
        decimal_diff_b = pow_mod256(10, 18 - decimal_b)
    elif decimal_a == 18 and decimal_b < 18:
        decimal_diff_a = 1
        decimal_diff_b = pow_mod256(10, 18 - decimal_b)
    elif decimal_a < 18 and decimal_b == 18:
        decimal_diff_a = pow_mod256(10, 18 - decimal_a)
        decimal_diff_b = 1
    else:
        raise "Decimals too big"

    new_pool: address = ZERO_ADDRESS
    #station_type: uint256 = 0
    
    addr_salt: bytes32 = keccak256(
        concat(
            convert(msg.sender, bytes32),
            convert(token_pair, bytes32),
            convert(_token_a, bytes32),
            convert(_token_b, bytes32))
            )
    new_pool = create_forwarder_to(STATION, salt = addr_salt)

    self.exchange_count += 1
    count: uint256 = self.exchange_count
    self.exchange_pairs_list[token_pair] = new_pool
    self.exchange_info[count] = token_pair
    self.exchange_info[token_pair] = count
    # Super pool fees is 9 that equals 1.665% for stable
    # and 3.709% for dynamic pool by default
    # Station lock is 0 by default
    # Proof of trade is False by default
    station_approved: uint256 = 0
    if self.approved_tokens[_token_a] or self.approved_tokens[_token_b]:
        self.approved_for_reward[new_pool] = True
        station_approved = 1
    else:
        self.approved_for_reward[new_pool] = False

    proof_of_trade: uint256 = 0
    pair_params: uint256 = proof_of_trade \
                        + shift(_station_type, 4) \
                        + shift(0, 6) \
                        + shift(station_approved, 8) \
                        + shift(_token_fees_a, 16) \
                        + shift(_token_fees_b, 32) \
                        + shift(9, 64) \
                        + shift(decimal_diff_a, 128) \
                        + shift(decimal_diff_b, 192)

    pool_response: Bytes[32] = raw_call(
        new_pool,
        concat(
            method_id("setup(address,address,address,uint256)"),
            convert(_token_a, bytes32),
            convert(_token_b, bytes32),
            convert(SUPER_POOL, bytes32),
            convert(pair_params, bytes32),
        ),
        max_outsize=32,
    )
    if len(pool_response) > 0:
        assert convert(pool_response, bool), "Pool setup failed"

    super_response: Bytes[32] = raw_call(
        SUPER_POOL,
        concat(
            method_id("add_approved_tokens(address)"),
            convert(new_pool, bytes32),
        ),
        max_outsize=32,
    )
    if len(super_response) > 0:
        assert convert(super_response, bool), "Super pool response failed"

    return True


@external
def register_new_pot(_station: address) -> bool:
    assert self.approved_for_reward[_station], "Station not approved"
    assert self.pot_station_list[_station] == ZERO_ADDRESS, "Station has PoT"
    assert msg.sender == STATION, "Wrong sender"

    new_pot: address = create_forwarder_to(POT_STATION)
    proof_of_trade: uint256 = 1

    pot_response: Bytes[32] = raw_call(
        new_pot,
        concat(
            method_id("setup(address)"),
            convert(_station, bytes32),
        ),
        max_outsize=32,
    )
    if len(pot_response) > 0:
        assert convert(pot_response, bool), "PoT setup failed"

    station_response: Bytes[32] = raw_call(
        _station,
        concat(
            method_id("stake_review(uint256,address)"),
            convert(proof_of_trade, bytes32),
            convert(new_pot, bytes32),
        ),
        max_outsize=32,
    )
    if len(station_response) > 0:
        assert convert(station_response, bool), "Station response failed"

    swd_token_response: Bytes[32] = raw_call(
        SWD_TOKEN,
        concat(
            method_id("register_pot(address,address)"),
            convert(_station, bytes32),
            convert(new_pot, bytes32),
        ),
        max_outsize=32,
    )
    if len(swd_token_response) > 0:
        assert convert(swd_token_response, bool), "SWD response failed"

    self.pot_station_list[_station] = new_pot
    return True


@external
def register_deployer():
    assert msg.sender == self.owner, "Owner only"
    swd_response: Bytes[32] = raw_call(
        SWD_TOKEN,
        method_id("register_deployer()"),
        max_outsize=32,
    )
    if len(swd_response) > 0:
        assert convert(swd_response, bool), "Register failed!"


@external
def remove_token_pair(_token_a: address, _token_b: address):
    assert msg.sender == self.owner, "Owner only"
    lock_status: uint256 = 1
    token_pair: uint256 = bitwise_xor(
        convert(_token_a, uint256),
        convert(_token_b, uint256))
    count: uint256 = self.exchange_info[token_pair]
    station_addr: address = self.exchange_pairs_list[token_pair]
    assert station_addr != ZERO_ADDRESS, "Station not registred"
    self.exchange_info[count] = 0
    self.exchange_info[token_pair] = 0
    self.exchange_pairs_list[token_pair] = ZERO_ADDRESS
    pot_addr: address = self.pot_station_list[station_addr]
    if pot_addr != ZERO_ADDRESS:
        self.pot_station_list[station_addr] = ZERO_ADDRESS
        pot_response: Bytes[32] = raw_call(
            pot_addr,
            concat(
                method_id("update_lock(uint256)"),
                convert(lock_status, bytes32),
            ),
            max_outsize=32,
        )
        if len(pot_response) > 0:
            assert convert(pot_response, bool), "PoT response failed"

    station_response: Bytes[32] = raw_call(
        station_addr,
        concat(
            method_id("update_lock(uint256)"),
            convert(lock_status, bytes32),
        ),
        max_outsize=32,
    )
    if len(station_response) > 0:
        assert convert(station_response, bool), "Station response failed"

    super_response: Bytes[32] = raw_call(
        SUPER_POOL,
        concat(
            method_id("remove_approved_tokens(address)"),
            convert(station_addr, bytes32),
        ),
        max_outsize=32,
    )
    if len(super_response) > 0:
        assert convert(super_response, bool), "Super pool response failed"


@external
def add_approved_tokens(_new_token: address):
    assert msg.sender == self.owner, "Owner only"
    assert _new_token != ZERO_ADDRESS, "ZERO ADDRESS"
    assert not self.approved_tokens[_new_token]
    self.approved_tokens[_new_token] = True


@external
def remove_approved_tokens(_new_token: address):
    assert msg.sender == self.owner, "Owner only"
    assert self.approved_tokens[_new_token]
    self.approved_tokens[_new_token] = False


# super pool control
@external
def super_pool_drop_balances(_tokens: address[10]) -> bool:
    assert msg.sender == self.owner, "Owner only"
    SUPER(SUPER_POOL).drop_distribution_balances(_tokens)
    return True


@external
def lock_super_pool(_lock: uint256, _expiry: uint256) -> bool:
    assert msg.sender == self.owner, "Owner only"
    super_response: Bytes[32] = raw_call(
        SUPER_POOL,
        concat(
            method_id("update_lock(uint256)"),
            convert(_lock, bytes32),
        ),
        max_outsize=32,
    )
    if len(super_response) > 0:
        assert convert(super_response, bool), "Super pool response failed"
    return True


# station control
@external
def lock_station(_station: address, _lock: uint256):
    assert msg.sender == self.owner, "Owner only"
    assert _lock <= 1, "1 Locked, 0 Unlocked"
    pot_addr: address = self.pot_station_list[_station]

    if pot_addr != ZERO_ADDRESS:
        pot_response: Bytes[32] = raw_call(
            pot_addr,
            concat(
                method_id("update_lock(uint256)"),
                convert(_lock, bytes32),
            ),
            max_outsize=32,
        )
        if len(pot_response) > 0:
            assert convert(pot_response, bool), "PoT response failed"

    station_response: Bytes[32] = raw_call(
        _station,
        concat(
            method_id("update_lock(uint256)"),
            convert(_lock, bytes32),
        ),
        max_outsize=32,
    )
    if len(station_response) > 0:
        assert convert(station_response, bool), "Station response failed"


@external
def unstake_station(_station: address):
    assert msg.sender == self.owner, "Owner only"
    assert self.pot_station_list[_station] != ZERO_ADDRESS, "Station hasn't PoT"
    station_response: Bytes[32] = raw_call(
        _station,
        concat(
            method_id("stake_review(uint256,address)"),
            convert(0, bytes32),
            convert(ZERO_ADDRESS, bytes32),
        ),
        max_outsize=32,
    )
    if len(station_response) > 0:
        assert convert(station_response, bool), "Station response failed"


@external
def update_token_fees(_station: address, _token_fees_a: uint256, _token_fees_b: uint256):
    assert msg.sender == self.owner, "Owner only"
    assert _token_fees_a >= 1 and _token_fees_a <= 99, "Wrong token fees"
    assert _token_fees_b >= 1 and _token_fees_b <= 99, "Wrong token fees"
    station_response: Bytes[32] = raw_call(
        _station,
        concat(
            method_id("token_fees_review(uint256,uint256)"),
            convert(_token_fees_a, bytes32),
            convert(_token_fees_b, bytes32),
        ),
        max_outsize=32,
    )
    if len(station_response) > 0:
        assert convert(station_response, bool), "Station response failed"


@external
def update_station_fees(_station: address, _station_fees: uint256):
    assert msg.sender == self.owner, "Owner only"
    assert _station_fees >= 5 and _station_fees <= 30, "Wrong station fees"
    station_response: Bytes[32] = raw_call(
        _station,
        concat(
            method_id("station_fees_review(uint256)"),
            convert(_station_fees, bytes32)
        ),
        max_outsize=32,
    )
    if len(station_response) > 0:
        assert convert(station_response, bool), "Station response failed"


@external
@view
def get_pair(
    _token_a: address,
    _token_b: address,
) -> (
    uint256,
    address
):
    token_pair: uint256 = bitwise_xor(convert(_token_a, uint256), convert(_token_b, uint256))
    if self.exchange_pairs_list[token_pair] == ZERO_ADDRESS:
        return (0, ZERO_ADDRESS)
    else:
        station: address = self.exchange_pairs_list[token_pair]
        return (token_pair, station)


@external
@view
def get_pair_info(
    _pair_id: uint256
) -> (
    address, address,
    address, address,
    String[32], String[32], 
    String[32], String[32], 
    uint256, uint256, 
    uint256, uint256, 
    uint256, uint256, 
    uint256, uint256, 
    uint256, uint256, 
    uint256, uint256, 
    uint256, uint256, 
    uint256, uint256
):
    token_pair: uint256 = self.exchange_info[_pair_id]
    if token_pair > 0:
        station: address = self.exchange_pairs_list[token_pair]
        
        token_a: address = ERC20D(station).token_a()
        token_name_a: String[32] = ERC20D(token_a).name()
        token_symbol_a: String[32] = ERC20D(token_a).symbol()
        token_decimals_a: uint256 = ERC20D(token_a).decimals()

        token_b: address = ERC20D(station).token_b()
        token_name_b: String[32] = ERC20D(token_b).name()
        token_symbol_b: String[32] = ERC20D(token_b).symbol()
        token_decimals_b: uint256 = ERC20D(token_b).decimals()

        pot_station: address = ERC20D(station).pot_station()

        token_balance_a: uint256 = ERC20D(token_a).balanceOf(station)
        token_balance_b: uint256 = ERC20D(token_b).balanceOf(station)
        station_token_balance: uint256 = ERC20D(station).totalSupply()

        pot_station_swd_balance: uint256 = 0
        if pot_station != ZERO_ADDRESS:
            pot_station_swd_balance = ERC20D(SWD_TOKEN).balanceOf(pot_station)

        params: uint256 = ERC20D(station).pair_params()
        staked: uint256 = bitwise_and(params, 2 ** 2 - 1)

        station_type: uint256 = bitwise_and(
            shift(params, -4), 2 ** 2 - 1)
        locked: uint256 = bitwise_and(
            shift(params, -6), 2 ** 2 - 1)
        station_approved: uint256 = bitwise_and(
            shift(params, -8), 2 ** 2 - 1)

        token_fees_a: uint256 = bitwise_and(
            shift(params, -16), 2 ** 16 - 1)
        token_fees_b: uint256 = bitwise_and(
            shift(params, -32), 2 ** 16 - 1)
        station_fees: uint256 = bitwise_and(
            shift(params, -64), 2 ** 16 - 1)
        decimal_diff_a: uint256 = bitwise_and(
            shift(params, -128), 2 ** 64 - 1)
        decimal_diff_b: uint256 = shift(params, -192)

        return ( #24
            station, token_a,
            token_b, pot_station,
            token_name_a, token_symbol_a,
            token_name_b, token_symbol_b,
            token_decimals_a, token_decimals_b,
            token_balance_a, token_balance_b,
            station_token_balance, pot_station_swd_balance,
            params, staked, station_type, locked, 
            station_approved, token_fees_a, token_fees_b,
            station_fees, decimal_diff_a, decimal_diff_b
        )
    else:
        return (
            ZERO_ADDRESS, ZERO_ADDRESS,
            ZERO_ADDRESS, ZERO_ADDRESS,
            "ZERO", "ZERO", "ZERO", "ZERO",
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
        )


@external
@view
def get_data_block(
    _break: uint256,
    _position: uint256
) -> (
    address[30], address[30], 
    address[30], address[30], 
    bytes32[30], bytes32[30], 
    bytes32[30], uint256[30], 
    uint256[30], uint256[30]
):
    idx: uint256 = 0
    pot_array: address[30] = empty(address[30])
    station_array: address[30] = empty(address[30])
    token_array_a: address[30] = empty(address[30])
    token_array_b: address[30] = empty(address[30])    

    pair_params_array: uint256[30] = empty(uint256[30])
    token_array_name_a: bytes32[30] = empty(bytes32[30])
    token_array_name_b: bytes32[30] = empty(bytes32[30])

    token_array_symbols: bytes32[30] = empty(bytes32[30])
    token_array_decimals_balances: uint256[30] = empty(uint256[30])
    station_pot_array_balances: uint256[30] = empty(uint256[30])
    
    START_RANGE: int128 = convert(_position, int128)
    for i in range(START_RANGE, START_RANGE + MAX_STEPS):
        # add break
        if _break != 0:
            if idx == _break:
                break
        pair_id: uint256 = convert(i, uint256)
        token_pair: uint256 = self.exchange_info[pair_id]
        station: address = self.exchange_pairs_list[token_pair]
        if station != ZERO_ADDRESS:

            token_a: address = ERC20D(station).token_a()
            token_name_a: String[32] = ERC20D(token_a).name()
            token_symbol_a: String[32] = ERC20D(token_a).symbol()
            token_decimals_a: uint256 = ERC20D(token_a).decimals()

            token_b: address = ERC20D(station).token_b()
            token_name_b: String[32] = ERC20D(token_b).name()
            token_symbol_b: String[32] = ERC20D(token_b).symbol()
            token_decimals_b: uint256 = ERC20D(token_b).decimals()
            
            pot_station: address = ERC20D(station).pot_station()
            pair_params: uint256 = ERC20D(station).pair_params()

            token_balance_a: uint256 = ERC20D(token_a).balanceOf(station)
            token_balance_b: uint256 = ERC20D(token_b).balanceOf(station)
            station_token_balance: uint256 = ERC20D(station).totalSupply()

            pot_station_swd_balance: uint256 = 0
            if pot_station != ZERO_ADDRESS:
                pot_station_swd_balance = ERC20D(SWD_TOKEN).balanceOf(pot_station)

            get_token_name_bytes_a: Bytes[96] = _abi_encode(token_name_a)
            get_token_name_bytes_b: Bytes[96] = _abi_encode(token_name_b)
            # optimize symbols
            concat_symbols: String[65] = concat(token_symbol_a, "/", token_symbol_b)
            get_token_symbols_bytes: Bytes[160] = _abi_encode(concat_symbols)
            
            slice_name_bytes_a: bytes32 = extract32(slice(
                get_token_name_bytes_a, 64, 32), 0, output_type=bytes32)
            slice_name_bytes_b: bytes32 = extract32(slice(
                get_token_name_bytes_b, 64, 32), 0, output_type=bytes32)
            slice_symbols_bytes: bytes32 = extract32(slice(
                get_token_symbols_bytes, 64, 32), 0, output_type=bytes32)
            # optimize decimals, balances
            tokens_decimals_balances: uint256 = token_decimals_a \
                                    + shift(token_decimals_b, 6) \
                                    + shift(token_balance_a, 12) \
                                    + shift(token_balance_b, 124)
            station_pot_balances: uint256 = station_token_balance \
                                    + shift(pot_station_swd_balance, 128)

            station_array[idx] = station
            token_array_a[idx] = token_a
            token_array_b[idx] = token_b
            pot_array[idx] = pot_station
            pair_params_array[idx] = pair_params
            token_array_name_a[idx] = slice_name_bytes_a
            token_array_name_b[idx] = slice_name_bytes_b

            token_array_symbols[idx] = slice_symbols_bytes
            station_pot_array_balances[idx] = station_pot_balances
            token_array_decimals_balances[idx] = tokens_decimals_balances
            
        idx += 1

    return (
        station_array, pot_array, 
        token_array_a, token_array_b, 
        token_array_name_a, token_array_name_b,
        token_array_symbols, pair_params_array,
        token_array_decimals_balances, station_pot_array_balances
    )


@external
def update_owner(_new_owner: address):
    assert msg.sender == self.owner, "Owner only"
    assert self.owner_agree, "Owner not agree"
    assert self.guardian_agree, "Guardian not agree"
    self.owner = _new_owner
    self.owner_agree = False
    self.guardian_agree = False
    log NewOwner(msg.sender, _new_owner)


@external
def set_guardian(guardian: address):
    assert msg.sender == self.owner, "Owner only"
    assert not self.done, "Guardian already registred"
    assert guardian != ZERO_ADDRESS
    self.guardian_agree = False
    self.owner_agree = False
    self.guardian = guardian
    self.done = True
    log NewGuardian(guardian)


@external
def update_guardian():
    assert msg.sender == self.owner, "Owner only"
    assert self.done, "Guardian not registred"
    assert self.owner_agree, "Owner not agree"
    assert self.guardian_agree, "Guardian not agree"
    self.done = False


@external
def ask_guardian(_agree: uint256):
    assert msg.sender == self.guardian, "Guardian only"
    assert self.owner_agree, "Owner not agree"
    assert _agree <= 1, "1 Yes, 0 No"
    self.guardian_agree = convert(_agree, bool)


@external
def ask_owner(_agree: uint256):
    assert msg.sender == self.owner, "Owner only"
    assert _agree <= 1, "1 Yes, 0 No"
    self.owner_agree = convert(_agree, bool)