import time
from brownie import ZERO_ADDRESS, Deployer
from brownie import SwapStation, PoTStation

def test_register_new_pool(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    stable.initialize(tokenA, tokenB, 4, 4, 0, 1e18, {'from': accounts[0]})
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    assert deployer.exchange_info(2) == ZERO_ADDRESS
    new_station_info = deployer.get_pair_info(1)

    new_station_addr = new_station_info[0]
    new_exchange = SwapStation.at(new_station_addr)
    check_ex = new_exchange.token_a()
    assert check_ex == tokenA


def test_unstake_station(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
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
    print("new_station_infonew_station_infonew_station_info", new_station_info)
    stable.initialize_pot_station(new_station_addr, 1e18, {'from': accounts[0]})
    assert deployer.pot_station_list(new_station_addr) != ZERO_ADDRESS
    new_station_info = deployer.get_pair_info(1)
    new_pot_addr = new_station_info[3]
    assert new_pot_addr != ZERO_ADDRESS
    new_pot = PoTStation.at(new_pot_addr)
    new_station_addr = new_station_info[0]
    new_exchange = SwapStation.at(new_station_addr)
    deployer.unstake_station(new_station_addr, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    new_pot_addr = new_station_info[3]
    assert new_pot_addr == ZERO_ADDRESS
    check_ex = new_exchange.lock()
    check_pot = new_pot.lock()
    assert check_ex == False
    assert check_pot == False


def test_register_new_pot(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 1, 1, 0, 1e18, {'from': accounts[0]})
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

def test_remove_token_pair(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    stable.initialize(tokenA, tokenB, 4, 4, 0, 1e18, {'from': accounts[0]})
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    assert deployer.exchange_info(2) == ZERO_ADDRESS
    deployer.remove_token_pair(tokenB, tokenA, {'from': accounts[0]})
    assert deployer.exchange_info(1) == ZERO_ADDRESS
    assert deployer.exchange_info(2) == ZERO_ADDRESS

def test_lock_station(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 4, 4, 0, 1e18, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
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

def test_update_token_fees(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 4, 4, 0, 1e18, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    new_station_info = deployer.get_pair_info(1)
    tokenA_fees = new_station_info[19]
    tokenB_fees = new_station_info[20]
    assert tokenA_fees == 4
    assert tokenB_fees == 4
    deployer.update_token_fees(new_station_addr, 45, 50, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    tokenA_fees = new_station_info[19]
    tokenB_fees = new_station_info[20]
    assert tokenA_fees == 45
    assert tokenB_fees == 50

def test_update_station_fees(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    deployer.add_approved_tokens(tokenA, {'from': accounts[0]})
    stable.initialize(tokenA, tokenB, 4, 4, 0, 1e18, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    new_station_info = deployer.get_pair_info(1)
    station_fees = new_station_info[21]
    assert station_fees == 9
    deployer.update_station_fees(new_station_addr, 30, {'from': accounts[0]})
    new_station_info = deployer.get_pair_info(1)
    station_fees = new_station_info[21]
    assert station_fees == 30


def test_register_deployer(deployer, station, token, tokenA, tokenB, super, accounts):
    stable = station
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    assert token.deployer() == deployer

def test_update_owner(deployer, accounts):
    deployer.set_guardian(accounts[1], {'from': accounts[0]})
    deployer.ask_owner(1, {'from': accounts[0]})
    assert deployer.guardian() == accounts[1]
    deployer.ask_guardian(1, {'from': accounts[1]})
    deployer.update_owner(accounts[3], {'from': accounts[0]})
    assert deployer.owner() == accounts[3]

def test_add_approved_tokens(deployer, token, accounts):
    deployer.add_approved_tokens(token, {'from': accounts[0]})
    assert deployer.approved_tokens(0, token) is True

def test_remove_approved_tokens(deployer, token, accounts):
    deployer.add_approved_tokens(token, {'from': accounts[0]})
    assert deployer.approved_tokens(0, token) is True
    deployer.remove_approved_tokens(token, {'from': accounts[0]})
    assert deployer.approved_tokens(0, token) is False

    ### super pool control

def test_lock_super_pool(deployer, station, token, super, accounts):
    stable = station
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    token.approve(super, 1e18, {'from': accounts[0]})
    super.deposit(1e18, 1e18, {'from': accounts[0]})
    deployer.lock_super_pool(1, {'from': accounts[0]})
    #init 0
    assert super.lock() == True
    time.sleep(181)
    deployer.lock_super_pool(0, {'from': accounts[0]})
    assert super.lock() == False


def test_set_deployer_guardian(deployer, accounts):
    deployer.set_guardian(accounts[1], {'from': accounts[0]})
    assert deployer.guardian() == accounts[1]


def test_ask_deployer_guardian(deployer, accounts):
    deployer.set_guardian(accounts[1], {'from': accounts[0]})
    deployer.ask_owner(1, {'from': accounts[0]})
    assert deployer.guardian() == accounts[1]
    deployer.ask_guardian(1, {'from': accounts[1]})


def test_ask_deployer_owner(deployer, accounts):
    deployer.set_guardian(accounts[1], {'from': accounts[0]})
    assert deployer.guardian() == accounts[1]
    deployer.ask_owner(1, {'from': accounts[0]})
    deployer.ask_guardian(1, {'from': accounts[1]})


def test_update_deployer_owner(deployer, accounts):
    deployer.set_guardian(accounts[1], {'from': accounts[0]})
    deployer.ask_owner(1, {'from': accounts[0]})
    assert deployer.guardian() == accounts[1]
    deployer.ask_guardian(1, {'from': accounts[1]})
    deployer.update_owner(accounts[3], {'from': accounts[0]})
    assert deployer.owner() == accounts[3]


def test_update_deployer_guard(deployer, accounts):
    deployer.set_guardian(accounts[1], {'from': accounts[0]})
    deployer.ask_owner(1, {'from': accounts[0]})
    assert deployer.guardian() == accounts[1]
    deployer.ask_guardian(1, {'from': accounts[1]})
    deployer.update_guardian({'from': accounts[0]})
    deployer.set_guardian(accounts[3], {'from': accounts[0]})
    assert deployer.guardian() == accounts[3]

### events

def test_new_owner_event_fires(deployer, accounts):
    deployer.set_guardian(accounts[1], {'from': accounts[0]})
    deployer.ask_owner(1, {'from': accounts[0]})
    assert deployer.guardian() == accounts[1]
    deployer.ask_guardian(1, {'from': accounts[1]})
    tx = deployer.update_owner(accounts[3], {'from': accounts[0]})
    assert deployer.owner() == accounts[3]
    assert len(tx.events) == 1
    assert tx.events["NewOwner"].values() == [accounts[0], accounts[3]]