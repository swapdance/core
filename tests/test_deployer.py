from ape import project, chain
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

def test_register_new_pool(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    stable.initialize(tokenA, tokenB, 4, 4, 0, int(1e18), sender=accounts[0])
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    assert deployer.exchange_info(2) == 0
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    new_exchange = project.SwapStation.at(new_station_addr)
    check_ex = new_exchange.token_a()
    assert check_ex == tokenA


def test_unstake_station(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 4, 4, 0, int(1e18), sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    assert deployer.pot_station_list(new_station_addr) == ZERO_ADDRESS
    stable.initialize_pot_station(new_station_addr, int(1e18), sender=accounts[0])
    assert deployer.pot_station_list(new_station_addr) != ZERO_ADDRESS
    new_station_info = deployer.get_pair_info(1)
    new_pot_addr = new_station_info[3]
    assert new_pot_addr != ZERO_ADDRESS
    new_pot = project.PoTStation.at(new_pot_addr)
    new_station_addr = new_station_info[0]
    new_exchange = project.SwapStation.at(new_station_addr)
    deployer.unstake_station(new_station_addr, sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    new_pot_addr = new_station_info[3]
    assert new_pot_addr == ZERO_ADDRESS
    check_ex = new_exchange.lock()
    check_pot = new_pot.lock()
    assert check_ex == False
    assert check_pot == False


def test_register_new_pot(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 1, 1, 0, int(1e18), sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    assert deployer.pot_station_list(new_station_addr) == ZERO_ADDRESS
    stable.initialize_pot_station(new_station_addr, int(1e18), sender=accounts[0])
    assert deployer.pot_station_list(new_station_addr) != ZERO_ADDRESS
    pot_addr = deployer.pot_station_list(new_station_addr)
    new_pot = project.PoTStation.at(pot_addr)
    #Remove token pair
    deployer.remove_token_pair(tokenA, tokenB, sender=accounts[0])
    assert deployer.exchange_info(1) == 0
    assert deployer.pot_station_list(new_station_addr) == ZERO_ADDRESS
    new_exchange = project.SwapStation.at(new_station_addr)
    check_ex = new_exchange.lock()
    check_pot = new_pot.lock()
    assert check_ex == True
    assert check_pot == True

def test_remove_token_pair(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    stable.initialize(tokenA, tokenB, 4, 4, 0, int(1e18), sender=accounts[0])
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    assert deployer.exchange_info(2) == 0
    deployer.remove_token_pair(tokenB, tokenA, sender=accounts[0])
    assert deployer.exchange_info(1) == 0
    assert deployer.exchange_info(2) == 0

def test_lock_station(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 4, 4, 0, int(1e18), sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    new_exchange = project.SwapStation.at(new_station_addr)
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    deployer.lock_station(new_station_addr, 1, sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    lock_status = new_station_info[17]
    assert lock_status == True
    check_ex = new_exchange.lock()
    assert check_ex == True
    deployer.lock_station(new_station_addr, 0, sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    lock_status = new_station_info[17]
    assert lock_status == False
    check_ex = new_exchange.lock()
    assert check_ex == False

def test_update_token_fees(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 4, 4, 0, int(1e18), sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    new_station_info = deployer.get_pair_info(1)
    tokenA_fees = new_station_info[19]
    tokenB_fees = new_station_info[20]
    assert tokenA_fees == 4
    assert tokenB_fees == 4
    deployer.update_token_fees(new_station_addr, 45, 50, sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    tokenA_fees = new_station_info[19]
    tokenB_fees = new_station_info[20]
    assert tokenA_fees == 45
    assert tokenB_fees == 50

def test_update_station_fees(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 4, 4, 0, int(1e18), sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    new_station_info = deployer.get_pair_info(1)
    station_fees = new_station_info[21]
    assert station_fees == 9
    deployer.update_station_fees(new_station_addr, 30, sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    station_fees = new_station_info[21]
    assert station_fees == 30


def test_register_deployer(deployer, station, token, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    assert token.deployer() == deployer

def test_update_owner(deployer, accounts):
    deployer.set_guardian(accounts[1], sender=accounts[0])
    deployer.ask_owner(1, sender=accounts[0])
    assert deployer.guardian() == accounts[1]
    deployer.ask_guardian(1, sender=accounts[1])
    deployer.update_owner(accounts[3], sender=accounts[0])
    assert deployer.owner() == accounts[3]

def test_add_approved_tokens(deployer, token, accounts):
    deployer.add_approved_tokens(token, sender=accounts[0])
    assert deployer.approved_tokens(token) is True

def test_remove_approved_tokens(deployer, token, accounts):
    deployer.add_approved_tokens(token, sender=accounts[0])
    assert deployer.approved_tokens(token) is True
    deployer.remove_approved_tokens(token, sender=accounts[0])
    assert deployer.approved_tokens(token) is False

    ### super pool control

def test_lock_super_pool(deployer, station, token, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    token.approve(super, int(1e18), sender=accounts[0])
    super.deposit(int(1e18), int(1e18), sender=accounts[0])
    deployer.lock_super_pool(1, sender=accounts[0])
    #init 0
    assert super.lock() == True
    chain.pending_timestamp += 181

    ### time.sleep should work but... Brownie test goes fine here.
    deployer.lock_super_pool(0, sender=accounts[0])
    assert super.lock() == False


def test_set_deployer_guardian(deployer, accounts):
    deployer.set_guardian(accounts[1], sender=accounts[0])
    assert deployer.guardian() == accounts[1]


def test_ask_deployer_guardian(deployer, accounts):
    deployer.set_guardian(accounts[1], sender=accounts[0])
    deployer.ask_owner(1, sender=accounts[0])
    assert deployer.guardian() == accounts[1]
    deployer.ask_guardian(1, sender=accounts[1])


def test_ask_deployer_owner(deployer, accounts):
    deployer.set_guardian(accounts[1], sender=accounts[0])
    assert deployer.guardian() == accounts[1]
    deployer.ask_owner(1, sender=accounts[0])
    deployer.ask_guardian(1, sender=accounts[1])


def test_update_deployer_owner(deployer, accounts):
    deployer.set_guardian(accounts[1], sender=accounts[0])
    deployer.ask_owner(1, sender=accounts[0])
    assert deployer.guardian() == accounts[1]
    deployer.ask_guardian(1, sender=accounts[1])
    deployer.update_owner(accounts[3], sender=accounts[0])
    assert deployer.owner() == accounts[3]


def test_update_deployer_guard(deployer, accounts):
    deployer.set_guardian(accounts[1], sender=accounts[0])
    deployer.ask_owner(1, sender=accounts[0])
    assert deployer.guardian() == accounts[1]
    deployer.ask_guardian(1, sender=accounts[1])
    deployer.update_guardian(sender=accounts[0])
    deployer.set_guardian(accounts[3], sender=accounts[0])
    assert deployer.guardian() == accounts[3]
