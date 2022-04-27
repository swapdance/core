import brownie
from brownie import ZERO_ADDRESS

def test_approval(deploy, accounts):
    token = deploy[4]
    token.approve(accounts[1], 500, {'from': accounts[0]})
    assert token.allowance(accounts[0], accounts[1]) == 500

def test_transfer(deploy, accounts):
    token = deploy[4]
    token.transfer(accounts[1], 1000e18, {'from': accounts[0]})
    assert token.balanceOf(accounts[0]) == 9000e18
    with brownie.reverts():
        token.transfer(accounts[2], 1e24, {'from': accounts[1]})

def test_transferFrom(deploy, accounts):
    token = deploy[4]
    sender_balance = token.balanceOf(accounts[0])
    amount = sender_balance // 4
    token.approve(accounts[1], amount, {'from': accounts[0]})
    token.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})
    assert token.balanceOf(accounts[0]) == sender_balance - amount

def test_new_deployer(deploy, accounts):
    token = deploy[4]
    token.new_deployer(accounts[1], {'from': accounts[0]})
    assert token.deployer() == accounts[1]

def test_register_deployer(deploy, accounts):
    token = deploy[4]
    token.new_deployer(accounts[1], {'from': accounts[0]})
    tx = token.register_deployer({'from': accounts[1]})
    assert token.deployer() == accounts[1]
    assert tx.return_value is True

def test_register_pot(deploy, accounts):
    token = deploy[4]
    token.new_deployer(accounts[1], {'from': accounts[0]})
    tx = token.register_deployer({'from': accounts[1]})
    tx_pot = token.register_pot(accounts[2], accounts[3], {'from': accounts[1]})
    assert token.deployer() == accounts[1]
    assert tx.return_value is True
    assert tx_pot.return_value is True

def test_mint_proof_of_trade(deploy, accounts):
    token = deploy[4]
    token.new_deployer(accounts[1], {'from': accounts[0]})
    tx = token.register_deployer({'from': accounts[1]})
    tx_pot = token.register_pot(accounts[2], accounts[3], {'from': accounts[1]})
    tx_mint = token.mint_proof_of_trade(10, {'from': accounts[2]})
    assert token.deployer() == accounts[1]
    assert tx.return_value is True
    assert tx_pot.return_value is True
    assert tx_mint.return_value is True

def test_dev_salary(deploy, accounts):
    token = deploy[4]
    tx = token.dev_salary(accounts[1], 1e18, {'from': accounts[0]})
    assert token.balanceOf(accounts[1]) == 1e18
    assert token.lock_time() > tx.timestamp
    assert token.lock_time() < (tx.timestamp + 30 * 24 * 60 * 60)

def test_increase_salary_rate(deploy, accounts):
    token = deploy[4]
    tx = token.increase_salary_rate(200, {'from': accounts[0]})
    tx2 = token.increase_salary_rate(2350, {'from': accounts[0]})
    assert tx.return_value is True
    assert not tx2.return_value is False

def test_burn(deploy, accounts):
    token = deploy[4]
    token.burn(1000e18, {'from': accounts[0]})
    assert token.balanceOf(accounts[0]) == 9000e18

#check guardian
def test_set_guardian(deploy, accounts):
    token = deploy[4]
    token.set_guardian(accounts[1], {'from': accounts[0]})
    assert token.guardian() == accounts[1]

#check owner
def test_ask_guardian(deploy, accounts):
    token = deploy[4]
    #print(token.owner_agree())
    #assert token.owner_agree() == True
    token.set_guardian(accounts[1], {'from': accounts[0]})
    token.ask_owner(1, {'from': accounts[0]})
    assert token.guardian() == accounts[1]
    token.ask_guardian(1, {'from': accounts[1]})
    #assert token.guardian_agree() == True

#check owner
def test_ask_owner(deploy, accounts):
    token = deploy[4]
    token.set_guardian(accounts[1], {'from': accounts[0]})
    assert token.guardian() == accounts[1]
    token.ask_owner(1, {'from': accounts[0]})
    #assert token.owner_agree() == True
    token.ask_guardian(1, {'from': accounts[1]})
    #assert token.guardian_agree() == True

#check owner
def test_update_swd_owner(deploy, accounts):
    token = deploy[4]
    token.set_guardian(accounts[1], {'from': accounts[0]})
    token.ask_owner(1, {'from': accounts[0]})
    #assert token.owner_agree() == True
    assert token.guardian() == accounts[1]
    token.ask_guardian(1, {'from': accounts[1]})
    #assert token.guardian_agree() == True
    token.update_owner(accounts[3], {'from': accounts[0]})
    assert token.owner() == accounts[3]

#check update guard
def test_update_guard(deploy, accounts):
    token = deploy[4]
    token.set_guardian(accounts[1], {'from': accounts[0]})
    token.ask_owner(1, {'from': accounts[0]})
    #assert token.owner_agree() == True
    assert token.guardian() == accounts[1]
    token.ask_guardian(1, {'from': accounts[1]})
    #assert token.guardian_agree() == True
    token.update_guardian({'from': accounts[0]})
    token.set_guardian(accounts[3], {'from': accounts[0]})
    assert token.guardian() == accounts[3]
# set a new guard # to do

# Test Events
def test_approval_event_fires(deploy, accounts):
    token = deploy[4]
    tx = token.approve(accounts[1], 100e18, {'from': accounts[0]})
    assert len(tx.events) == 1
    assert tx.events["Approval"].values() == [accounts[0], accounts[1], 100e18]

def test_transfer_event_fires(deploy, accounts):
    token = deploy[4]
    tx = token.transfer(accounts[1], 100e18, {'from': accounts[0]})
    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [accounts[0], accounts[1], 100e18]

def test_increase_salary_rate_event_fires(deploy, accounts):
    token = deploy[4]
    tx = token.increase_salary_rate(200, {'from': accounts[0]})
    assert len(tx.events) == 1
    assert tx.events["NewSalaryRate"].values() == [accounts[0], 200]

def test_dev_salary_event_fires(deploy, accounts):
    token = deploy[4]
    tx = token.dev_salary(accounts[1], 1e18, {'from': accounts[0]})
    assert len(tx.events) == 2
    assert tx.events["Transfer"].values() == [ZERO_ADDRESS, accounts[1], 1e18]
    assert tx.events["Salary"].values() == [accounts[1], 1e18]

# test reverts
def test_revert_mint_proof_of_trade(deploy, accounts):
    token = deploy[4]
    with brownie.reverts():
        token.mint_proof_of_trade(1e18, {'from': accounts[0]})

def test_revert_max_dev_salary(deploy, accounts):
    token = deploy[4]
    with brownie.reverts():
        token.dev_salary(accounts[1], 1000e18, {'from': accounts[0]}) # test max
    token.dev_salary(accounts[1], 50e18, {'from': accounts[0]})
    with brownie.reverts():
        token.dev_salary(accounts[1], 1e18, {'from': accounts[0]}) # test time


def test_revert_register_deployer(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    with brownie.reverts():
        token.register_deployer()


def test_revert_update_deployer(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    super = deploy[2]
    super.update_owner(deployer, {'from': accounts[0]})
    stable.update_owner(deployer, {'from': accounts[0]})
    token.new_deployer(deployer, {'from': accounts[0]})
    deployer.register_deployer()
    token.set_guardian(accounts[1], {'from': accounts[0]})
    token.ask_owner(1, {'from': accounts[0]})
    token.ask_guardian(1, {'from': accounts[1]})
    with brownie.reverts():
        token.update_deployer({'from': accounts[1]})

    token.update_deployer({'from': accounts[0]})

    token.new_deployer(accounts[2], {'from': accounts[0]})