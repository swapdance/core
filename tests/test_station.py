import ape
from ape import project
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

def test_initialize(deployer, station, token, tokenA, tokenB, super, accounts):
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

def test_register_pot(deployer, station, token, tokenA, tokenB, super, accounts):
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

def test_stableswap(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 4, 4, 0, int(1e18), sender=accounts[0])
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, int(1e18), sender=accounts[0])
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = project.PoTStation.at(pot_addr)
    station = project.SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, int(1000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(1000e18), sender=accounts[0])
    station.add_liquidity(int(1000e18), int(1000e18), int(1000e18), int(1000e18), int(1e18), sender=accounts[0])
    lp_token_balance = station.balanceOf(accounts[0])
    station.approve(pot_addr, lp_token_balance, sender=accounts[0])
    pot_station.stake(lp_token_balance, int(1e18), sender=accounts[0])
    # swap tokens to mint swd

    for i in range(10):
        tokenA.approve(new_station_addr, int(100e18), sender=accounts[0])
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])

    for i in range(10):
        tokenB.approve(new_station_addr, int(100e18), sender=accounts[0])
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])

    #check pair state (0 stable 1 dynamic)
    new_station_info = deployer.get_pair_info(1)
    station_stable = new_station_info[16]
    assert station_stable == 0

def test_lock_station(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 30, 30, 0, int(1e18), sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    new_exchange = project.SwapStation.at(new_station_addr)
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    deployer.lock_station(new_station_addr, 1, sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    lock_status = new_station_info[17]
    print("new_station_info", new_station_info)
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
    stable.initialize(tokenA, tokenB, 30, 30, 0, int(1e18), sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    new_station_info = deployer.get_pair_info(1)
    tokenA_fees = new_station_info[19]
    tokenB_fees = new_station_info[20]
    assert tokenA_fees == 30
    assert tokenB_fees == 30

    with ape.reverts():
        deployer.update_token_fees(new_station_addr, 145, 150, sender=accounts[0])

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
    stable.initialize(tokenA, tokenB, 20, 20, 0, int(1e18), sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    new_station_info = deployer.get_pair_info(1)
    new_exchange = project.SwapStation.at(new_station_addr)
    station_fees = new_station_info[21]
    assert station_fees == 9

    with ape.reverts():
        deployer.update_station_fees(new_station_addr, 130, sender=accounts[0])

    deployer.update_station_fees(new_station_addr, 30, sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    station_fees = new_station_info[21]
    assert station_fees == 30


def test_unstake_station(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 30, 30, 0, int(1e18), sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, int(1e18), sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    unstake_status = new_station_info[15]
    assert unstake_status == 1
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
    #unstake
    deployer.unstake_station(new_station_addr, sender=accounts[0])
    new_station_info = deployer.get_pair_info(1)
    unstake_status = new_station_info[15]
    assert unstake_status == 0



def test_addliquidity(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 20, 20, 0, int(1e18), sender=accounts[0])
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, int(1e18), sender=accounts[0])
    station = project.SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, int(1000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(1000e18), sender=accounts[0])
    station.add_liquidity(int(1000e18), int(1000e18), int(1000e18), int(1000e18), int(1e18), sender=accounts[0])
    with ape.reverts():
        station.add_liquidity(0, 0, 0, 0, int(1e18), sender=accounts[0])
        station.add_liquidity(0, 10, 0, 0, int(1e18), sender=accounts[0])
        station.add_liquidity(0, 0, 10, 0, int(1e18), sender=accounts[0])
        station.add_liquidity(0, 0, 0, 0, 1, sender=accounts[0])
        station.add_liquidity(10, 0, 0, 0, int(1e18), sender=accounts[0])
        station.add_liquidity(10, 110, 1110, 11110, int(1e18), sender=accounts[0])
    lp_token_balance = station.balanceOf(accounts[0])
    print("lp_token_balance", lp_token_balance)

def test_remove_liquidity(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    #token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 2, 2, 0, int(1e18), sender=accounts[0])
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, int(1e18), sender=accounts[0])
    station = project.SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, int(1000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(1000e18), sender=accounts[0])
    station.add_liquidity(int(1000e18), int(1000e18), int(1000e18), int(1000e18), int(1e18), sender=accounts[0])
    lp_token_balance = station.balanceOf(accounts[0])
    #assert ((int(1000e18) + int(1000e18)) / 2) == lp_token_balance
    #remove_liquidity
    station.remove_liquidity(int(lp_token_balance/2), int(499e18), int(499e18), int(1e18), sender=accounts[0])
    lp_token_balance = station.balanceOf(accounts[0])
    #assert lp_token_balance == ((int(1000e18) + int(1000e18)) / 2)/2
    station.remove_liquidity(int(lp_token_balance), int(499e18), int(499e18), int(1e18), sender=accounts[0])
    lp_token_balance = station.balanceOf(accounts[0])
    assert lp_token_balance == 0


###### Check unstable swap.

def test_dynamic_swap(deployer, station, token, tokenA, tokenB, super, router, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 30, 30, 1, int(1e18), sender=accounts[0])
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, int(1e18), sender=accounts[0])
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = project.PoTStation.at(pot_addr)
    station = project.SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, int(20e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(10000e18), sender=accounts[0])

    with ape.reverts():
        station.add_liquidity(0, 0, 1, 1, int(1e18), sender=accounts[0])
    station.add_liquidity(int(20e18), int(20e18), int(10000e18), int(10000e18), int(1e18), sender=accounts[0])

    lp_token_balance = station.balanceOf(accounts[0])
    station.approve(pot_addr, lp_token_balance, sender=accounts[0])
    pot_station.stake(lp_token_balance, int(1e18), sender=accounts[0])
    # swap tokens to mint swd
    token1 = deploy[14]
    token1.approve(new_station_addr, int(1e18), sender=accounts[0])
    get_amount_out = router.get_amount_out(new_station_addr, tokenA, int(1e18))
    with ape.reverts():
        station.swap_tokens(int(1e18), get_amount_out, token1, int(1e18), sender=accounts[0]) # wrong token
    for i in range(10):
        tokenA.approve(new_station_addr, int(1e18), sender=accounts[0])
        get_amount_out = router.get_amount_out(new_station_addr, tokenA, int(1e18))
        station.swap_tokens(int(1e18), get_amount_out, tokenA, int(1e18), sender=accounts[0])

    for i in range(5):
        tokenB.approve(new_station_addr, int(500e18), sender=accounts[0])
        get_amount_out = router.get_amount_out(new_station_addr, tokenB, int(500e18))
        print("get_amount_out", get_amount_out)
        station.swap_tokens(int(500e18), get_amount_out, tokenB, int(1e18), sender=accounts[0])


    #check pair state (0 stable 1 dynamic)
    new_station_info = deployer.get_pair_info(1)
    station_dynamic = new_station_info[16]
    assert station_dynamic == 1
    #check status staked or not
    new_station_info = deployer.get_pair_info(1)
    unstake_status = new_station_info[15]
    assert unstake_status == 1

###### Cover all functions to get 100% test rate

def test_force_reward(deployer, station, token, tokenA, tokenB, super, router, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 30, 30, 1, int(1e18), sender=accounts[0])
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, int(1e18), sender=accounts[0])
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = project.PoTStation.at(pot_addr)
    station = project.SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, int(20e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(10000e18), sender=accounts[0])
    station.add_liquidity(int(20e18), int(20e18), int(10000e18), int(10000e18), int(1e18), sender=accounts[0])
    lp_token_balance = station.balanceOf(accounts[0])
    station.approve(pot_addr, lp_token_balance, sender=accounts[0])
    pot_station.stake(lp_token_balance, int(1e18), sender=accounts[0])
    # swap tokens to mint swd
    assert token.balanceOf(pot_addr) == 0
    for i in range(10):
        tokenA.approve(new_station_addr, int(1e18), sender=accounts[0])
        get_amount_out = router.get_amount_out(new_station_addr, tokenA, int(1e18))
        station.swap_tokens(int(1e18), get_amount_out, tokenA, int(1e18), sender=accounts[0])

    for i in range(5):
        tokenB.approve(new_station_addr, int(500e18), sender=accounts[0])
        get_amount_out = router.get_amount_out(new_station_addr, tokenB, int(500e18))
        station.swap_tokens(int(500e18), get_amount_out, tokenB, int(1e18), sender=accounts[0])

    station.force_reward(sender=accounts[0])
    assert token.balanceOf(pot_addr) > 0


def test_approval(station, accounts):
    station.approve(accounts[1], 500, sender=accounts[0])
    assert station.allowance(accounts[0], accounts[1]) == 500

def test_transfer(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    #token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 2, 2, 0, int(1e18), sender=accounts[0])
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, int(1e18), sender=accounts[0])
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = project.PoTStation.at(pot_addr)
    station = project.SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, int(1000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(1000e18), sender=accounts[0])
    station.add_liquidity(int(1000e18), int(1000e18), int(1000e18), int(1000e18), int(1e18), sender=accounts[0])
    station.transfer(accounts[1], int(10e18), sender=accounts[0])
    assert station.balanceOf(accounts[1]) == 10e18
    with ape.reverts():
        station.transfer(accounts[2], int(1e24), sender=accounts[1])

def test_transferFrom(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    #token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 2, 2, 0, int(1e18), sender=accounts[0])
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, int(1e18), sender=accounts[0])
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = project.PoTStation.at(pot_addr)
    station = project.SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, int(1000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(1000e18), sender=accounts[0])
    station.add_liquidity(int(1000e18), int(1000e18), int(1000e18), int(1000e18), int(1e18), sender=accounts[0])
    station.transfer(accounts[1], int(10e18), sender=accounts[0])
    assert station.balanceOf(accounts[1]) == 10e18
    with ape.reverts():
        station.transfer(accounts[2], int(1e24), sender=accounts[1])
    sender_balance = station.balanceOf(accounts[0])
    station.approve(accounts[1], int(10e18), sender=accounts[0])
    station.transferFrom(accounts[0], accounts[2], int(10e18), sender=accounts[1])
    assert station.balanceOf(accounts[0]) == sender_balance - int(10e18)
