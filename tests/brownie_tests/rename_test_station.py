import brownie
from brownie import ZERO_ADDRESS, Deployer
from brownie import SwapStation
from brownie import PoTStation, SuperPool

def test_initialize(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer({'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 4, 4, 0, 1e18, {'from': accounts[0]})
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    assert deployer.exchange_info(2) == ZERO_ADDRESS
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    new_exchange = SwapStation.at(new_station_addr)
    check_ex = new_exchange.token_a()
    assert check_ex == tokenA

def test_register_pot(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 4, 4, 0, 1e18, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    assert deployer.pot_station_list(new_station_addr) == ZERO_ADDRESS
    stable.initialize_pot_station(new_station_addr, 1e18, {'from': accounts[0]})
    assert deployer.pot_station_list(new_station_addr) != ZERO_ADDRESS
    pot_addr = deployer.pot_station_list(new_station_addr)
    new_pot = PoTStation.at(pot_addr)
    #Remove token pair
    deployer.remove_token_pair(tokenA, tokenB, {'from': accounts[0]})
    assert deployer.exchange_info(1) == ZERO_ADDRESS
    assert deployer.pot_station_list(new_station_addr) == ZERO_ADDRESS
    new_exchange = SwapStation.at(new_station_addr)
    check_ex = new_exchange.lock()
    check_pot = new_pot.lock()
    assert check_ex == True
    assert check_pot == True

def test_stableswap(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 4, 4, 0, 1e18, {'from': accounts[0]})
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, 1e18, {'from': accounts[0]})
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = PoTStation.at(pot_addr)
    station = SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    tokenB.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    station.add_liquidity(1000e18, 1000e18, 1000e18, 1000e18, 1e18, {'from': accounts[0]})
    lp_token_balance = station.balanceOf(accounts[0])
    station.approve(pot_addr, lp_token_balance, {'from': accounts[0]})
    pot_station.stake(lp_token_balance, 1e18, {'from': accounts[0]})
    # swap tokens to mint swd

    for i in range(10):
        tokenA.approve(new_station_addr, 100e18, {'from': accounts[0]})
        tx = station.swap_tokens(100e18, 99e18, tokenA, 1e18, {'from': accounts[0]})
        amount = tx.return_value
        assert amount[0] < 100e18
        assert amount[0] > 99e18
        assert amount[1] == tokenB
    for i in range(10):
        tokenB.approve(new_station_addr, 100e18, {'from': accounts[0]})
        tx = station.swap_tokens(100e18, 99e18, tokenB, 1e18, {'from': accounts[0]})
        amount = tx.return_value
        assert amount[0] < 100e18
        assert amount[0] > 99e18
        assert amount[1] == tokenA


    #check pair state (0 stable 1 dynamic)
    new_station_info = deployer.get_pair_info(1)
    station_stable = new_station_info[16]
    assert station_stable == 0


def test_lock_station(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 30, 30, 0, 1e18, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    new_exchange = SwapStation.at(new_station_addr)
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    deployer.lock_station(new_station_addr, 1, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    lock_status = new_station_info[17]
    print("new_station_info", new_station_info)
    assert lock_status == True
    check_ex = new_exchange.lock()
    assert check_ex == True
    deployer.lock_station(new_station_addr, 0, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    lock_status = new_station_info[17]
    assert lock_status == False
    check_ex = new_exchange.lock()
    assert check_ex == False

def test_update_token_fees(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 30, 30, 0, 1e18, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    new_station_info = deployer.get_pair_info(1)
    tokenA_fees = new_station_info[19]
    tokenB_fees = new_station_info[20]
    assert tokenA_fees == 30
    assert tokenB_fees == 30
    deployer.update_token_fees(new_station_addr, 45, 50, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    tokenA_fees = new_station_info[19]
    tokenB_fees = new_station_info[20]
    assert tokenA_fees == 45
    assert tokenB_fees == 50


def test_update_station_fees(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 20, 20, 0, 1e18, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    new_station_info = deployer.get_pair_info(1)
    new_exchange = SwapStation.at(new_station_addr)
    station_fees = new_station_info[21]
    assert station_fees == 9
    deployer.update_station_fees(new_station_addr, 30, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    station_fees = new_station_info[21]
    assert station_fees == 30


def test_unstake_station(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 30, 30, 0, 1e18, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, 1e18, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    unstake_status = new_station_info[15]
    assert unstake_status == 1
    new_exchange = SwapStation.at(new_station_addr)
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    deployer.lock_station(new_station_addr, 1, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    lock_status = new_station_info[17]
    assert lock_status == True
    check_ex = new_exchange.lock()
    assert check_ex == True
    deployer.lock_station(new_station_addr, 0, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    lock_status = new_station_info[17]
    assert lock_status == False
    check_ex = new_exchange.lock()
    assert check_ex == False
    #unstake
    deployer.unstake_station(new_station_addr, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    unstake_status = new_station_info[15]
    assert unstake_status == 0



def test_addliquidity(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 20, 20, 0, 1e18, {'from': accounts[0]})
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, 1e18, {'from': accounts[0]})
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = PoTStation.at(pot_addr)
    station = SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    tokenB.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    station.add_liquidity(1000e18, 1000e18, 1000e18, 1000e18, 1e18, {'from': accounts[0]})
    with brownie.reverts():
        station.add_liquidity(0, 0, 0, 0, 1e18, {'from': accounts[0]})
    lp_token_balance = station.balanceOf(accounts[0])
    print("lp_token_balance", lp_token_balance)
    #assert ((1000e18 + 1000e18) / 2) == lp_token_balance

def test_remove_liquidity(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    #token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 2, 2, 0, 1e18, {'from': accounts[0]})
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, 1e18, {'from': accounts[0]})
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = PoTStation.at(pot_addr)
    station = SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    tokenB.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    station.add_liquidity(1000e18, 1000e18, 1000e18, 1000e18, 1e18, {'from': accounts[0]})
    lp_token_balance = station.balanceOf(accounts[0])
    #assert ((1000e18 + 1000e18) / 2) == lp_token_balance
    #remove_liquidity
    station.remove_liquidity(lp_token_balance/2, 499e18, 499e18, 1e18, {'from': accounts[0]})
    lp_token_balance = station.balanceOf(accounts[0])
    #assert lp_token_balance == ((1000e18 + 1000e18) / 2)/2
    station.remove_liquidity(lp_token_balance, 499e18, 499e18, 1e18, {'from': accounts[0]})
    lp_token_balance = station.balanceOf(accounts[0])
    assert lp_token_balance == 0


###### Check unstable swap.

def test_dynamic_swap(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    router = deploy[7]

    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 30, 30, 1, 1e18, {'from': accounts[0]})
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, 1e18, {'from': accounts[0]})
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = PoTStation.at(pot_addr)
    station = SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, 20e18, {'from': accounts[0]})
    tokenB.approve(new_station_addr, 10000e18, {'from': accounts[0]})

    with brownie.reverts():
        station.add_liquidity(0, 0, 1, 1, 1e18, {'from': accounts[0]})
    station.add_liquidity(20e18, 20e18, 10000e18, 10000e18, 1e18, {'from': accounts[0]})
    lp_token_balance = station.balanceOf(accounts[0])
    station.approve(pot_addr, lp_token_balance, {'from': accounts[0]})
    pot_station.stake(lp_token_balance, 1e18, {'from': accounts[0]})
    # swap tokens to mint swd
    token1 = deploy[14]
    token1.approve(new_station_addr, 1e18, {'from': accounts[0]})
    get_amount_out = router.get_amount_out(new_station_addr, tokenA, 1e18)
    with brownie.reverts():
        station.swap_tokens(1e18, get_amount_out, token1, 1e18, {'from': accounts[0]}) # wrong token
    for i in range(10):
        tokenA.approve(new_station_addr, 1e18, {'from': accounts[0]})
        get_amount_out = router.get_amount_out(new_station_addr, tokenA, 1e18)
        tx = station.swap_tokens(1e18, get_amount_out, tokenA, 1e18, {'from': accounts[0]})
        amount = tx.return_value
        assert amount[0] == get_amount_out
        assert amount[1] == tokenB
    for i in range(5):
        tokenB.approve(new_station_addr, 500e18, {'from': accounts[0]})
        get_amount_out = router.get_amount_out(new_station_addr, tokenB, 500e18)
        print("get_amount_out", get_amount_out)
        tx = station.swap_tokens(500e18, get_amount_out, tokenB, 1e18, {'from': accounts[0]})
        amount = tx.return_value
        assert amount[0] == get_amount_out
        assert amount[1] == tokenA

    #check pair state (0 stable 1 dynamic)
    new_station_info = deployer.get_pair_info(1)
    station_dynamic = new_station_info[16]
    assert station_dynamic == 1
    #check status staked or not
    new_station_info = deployer.get_pair_info(1)
    unstake_status = new_station_info[15]
    assert unstake_status == 1

###### Cover all functions to get 100% test rate

def test_force_reward(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    router = deploy[7]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 30, 30, 1, 1e18, {'from': accounts[0]})
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, 1e18, {'from': accounts[0]})
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = PoTStation.at(pot_addr)
    station = SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, 20e18, {'from': accounts[0]})
    tokenB.approve(new_station_addr, 10000e18, {'from': accounts[0]})
    station.add_liquidity(20e18, 20e18, 10000e18, 10000e18, 1e18, {'from': accounts[0]})
    lp_token_balance = station.balanceOf(accounts[0])
    station.approve(pot_addr, lp_token_balance, {'from': accounts[0]})
    pot_station.stake(lp_token_balance, 1e18, {'from': accounts[0]})
    # swap tokens to mint swd
    assert token.balanceOf(pot_addr) == 0
    for i in range(10):
        tokenA.approve(new_station_addr, 1e18, {'from': accounts[0]})
        get_amount_out = router.get_amount_out(new_station_addr, tokenA, 1e18)
        tx = station.swap_tokens(1e18, get_amount_out, tokenA, 1e18, {'from': accounts[0]})
        amount = tx.return_value
        assert amount[0] == get_amount_out
        assert amount[1] == tokenB
    for i in range(5):
        tokenB.approve(new_station_addr, 500e18, {'from': accounts[0]})
        get_amount_out = router.get_amount_out(new_station_addr, tokenB, 500e18)
        print("get_amount_out", get_amount_out)
        tx = station.swap_tokens(500e18, get_amount_out, tokenB, 1e18, {'from': accounts[0]})
        amount = tx.return_value
        assert amount[0] == get_amount_out
        assert amount[1] == tokenA

    station.force_reward({'from': accounts[5]})
    assert token.balanceOf(pot_addr) > 0


def test_approval(deploy, accounts):
    station = deploy[3]
    station.approve(accounts[1], 500, {'from': accounts[0]})
    assert station.allowance(accounts[0], accounts[1]) == 500

def test_transfer(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    #token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 2, 2, 0, 1e18, {'from': accounts[0]})
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, 1e18, {'from': accounts[0]})
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = PoTStation.at(pot_addr)
    station = SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    tokenB.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    station.add_liquidity(1000e18, 1000e18, 1000e18, 1000e18, 1e18, {'from': accounts[0]})
    station.transfer(accounts[1], 10e18, {'from': accounts[0]})
    assert station.balanceOf(accounts[1]) == 10e18
    with brownie.reverts():
        station.transfer(accounts[2], 1e24, {'from': accounts[1]})

def test_transferFrom(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    #token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 2, 2, 0, 1e18, {'from': accounts[0]})
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, 1e18, {'from': accounts[0]})
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = PoTStation.at(pot_addr)
    station = SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    tokenB.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    station.add_liquidity(1000e18, 1000e18, 1000e18, 1000e18, 1e18, {'from': accounts[0]})
    station.transfer(accounts[1], 10e18, {'from': accounts[0]})
    assert station.balanceOf(accounts[1]) == 10e18
    with brownie.reverts():
        station.transfer(accounts[2], 1e24, {'from': accounts[1]})
    sender_balance = station.balanceOf(accounts[0])
    station.approve(accounts[1], 10e18, {'from': accounts[0]})
    station.transferFrom(accounts[0], accounts[2], 10e18, {'from': accounts[1]})
    assert station.balanceOf(accounts[0]) == sender_balance - 10e18

# test events

def test_swap_tokens_event_fires(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 4, 4, 0, 1e18, {'from': accounts[0]})
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, 1e18, {'from': accounts[0]})
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = PoTStation.at(pot_addr)
    station = SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    tokenB.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    station.add_liquidity(1000e18, 1000e18, 1000e18, 1000e18, 1e18, {'from': accounts[0]})
    lp_token_balance = station.balanceOf(accounts[0])
    station.approve(pot_addr, lp_token_balance, {'from': accounts[0]})
    pot_station.stake(lp_token_balance, 1e18, {'from': accounts[0]})
    tokenA.approve(new_station_addr, 100e18, {'from': accounts[0]})
    tx = station.swap_tokens(100e18, 99e18, tokenA, 1e18, {'from': accounts[0]})
    assert len(tx.events) == 4
    print("tx.events2", tx.events)
    assert tx.events["TokenSwaps"].values() == [accounts[0], tokenA, tx.return_value[1], 100e18, tx.return_value[0]]


def test_add_liquidity_event_fires(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 4, 4, 0, 1e18, {'from': accounts[0]})
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, 1e18, {'from': accounts[0]})
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = PoTStation.at(pot_addr)
    station = SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    tokenB.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    tx = station.add_liquidity(1000e18, 1000e18, 1000e18, 1000e18, 1e18, {'from': accounts[0]})
    lp_token_balance = station.balanceOf(accounts[0])
    assert len(tx.events) == 7
    assert tx.events["AddLiquidity"].values() == [accounts[0], tokenA, tokenB, 1000e18, 1000e18]

def test_add_liquidity_and_mint_super_pool_fees_event_fires(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 4, 4, 0, 1e18, {'from': accounts[0]})
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, 1e18, {'from': accounts[0]})
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = PoTStation.at(pot_addr)
    station = SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    tokenB.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    with brownie.reverts():
        station.add_liquidity(1000e18, 100e18, 100e18, 1000e18, 1e18, {'from': accounts[0]})
        station.add_liquidity(0, 0, 0, 0, 1e18, {'from': accounts[0]})
    tx = station.add_liquidity(1000e18, 1000e18, 1000e18, 1000e18, 1e18, {'from': accounts[0]})

    assert len(tx.events) == 7
    print("tx.events", tx.events)
    assert tx.events["AddLiquidity"].values() == [accounts[0], tokenA, tokenB, 1000e18, 1000e18]

    lp_token_balance = station.balanceOf(accounts[0])
    station.approve(pot_addr, lp_token_balance, {'from': accounts[0]})
    pot_station.stake(lp_token_balance, 1e18, {'from': accounts[0]})
    # swap tokens to mint swd

    for i in range(10):
        tokenA.approve(new_station_addr, 100e18, {'from': accounts[0]})
        tx = station.swap_tokens(100e18, 99e18, tokenA, 1e18, {'from': accounts[0]})
        amount = tx.return_value
        assert amount[0] < 100e18
        assert amount[0] > 99e18
        assert amount[1] == tokenB
    for i in range(10):
        tokenB.approve(new_station_addr, 100e18, {'from': accounts[0]})
        tx = station.swap_tokens(100e18, 99e18, tokenB, 1e18, {'from': accounts[0]})
        amount = tx.return_value
        assert amount[0] < 100e18
        assert amount[0] > 99e18
        assert amount[1] == tokenA

    tokenA.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    tokenB.approve(new_station_addr, 1000e18, {'from': accounts[0]})
    tx = station.add_liquidity(1000e18, 1000e18, 1000e18, 1000e18, 1e18, {'from': accounts[0]})

    assert len(tx.events) == 8
    assert tx.events["AddLiquidity"].values() == [accounts[0], tokenA, tokenB, 1000e18, 1000e18]
    print(tx.events)


def test_update_lock_event_fires(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 4, 4, 0, 1e18, {'from': accounts[0]})
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    tx = deployer.lock_station(new_station_addr, 1, {'from': accounts[0]})
    assert len(tx.events) == 1
    assert tx.events["LockStation"].values() == [deployer, 1]

def test_update_owner_event_fires(deploy, accounts):
    station = deploy[3]
    tx = station.update_owner(accounts[1], {'from': accounts[0]})
    assert len(tx.events) == 1
    assert tx.events["NewOwner"].values() == [accounts[0], accounts[1]]