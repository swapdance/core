import ape
from ape import chain
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

def test_approval(token, accounts):
    token.approve(accounts[1], 500, sender=accounts[0])
    assert token.allowance(accounts[0], accounts[1]) == 500

def test_transfer(deploy, accounts):
    token = deploy[4]
    token.transfer(accounts[1], int(1000e18), sender=accounts[0])
    assert token.balanceOf(accounts[0]) == 9000e18
    with ape.reverts():
        token.transfer(accounts[2], int(1e24), sender=accounts[1])

def test_transferFrom(token, accounts):
    sender_balance = token.balanceOf(accounts[0])
    amount = sender_balance // 4
    token.approve(accounts[1], amount, sender=accounts[0])
    token.transferFrom(accounts[0], accounts[2], amount, sender=accounts[1])
    assert token.balanceOf(accounts[0]) == sender_balance - amount

def test_new_deployer(token, accounts):
    token.new_deployer(accounts[1], sender=accounts[0])
    assert token.deployer() == accounts[1]

def test_register_deployer(token, accounts):
    token.new_deployer(accounts[1], sender=accounts[0])
    tx = token.register_deployer(sender=accounts[1])
    assert token.deployer() == accounts[1]

def test_register_pot(token, accounts):
    token.new_deployer(accounts[1], sender=accounts[0])
    token.register_deployer(sender=accounts[1])
    token.register_pot(accounts[2], accounts[3], sender=accounts[1])
    assert token.deployer() == accounts[1]

def test_mint_proof_of_trade(token, accounts):
    token.new_deployer(accounts[1], sender=accounts[0])
    token.register_deployer(sender=accounts[1])
    token.register_pot(accounts[2], accounts[3], sender=accounts[1])
    token.mint_proof_of_trade(10, sender=accounts[2])
    assert token.deployer() == accounts[1]

def test_dev_salary(token, accounts):
    tx = token.dev_salary(accounts[1], int(1e18), sender=accounts[0])
    assert token.balanceOf(accounts[1]) == int(1e18)
    assert token.lock_time() > chain.pending_timestamp
    assert token.lock_time() < (chain.pending_timestamp + 30 * 24 * 60 * 60)

def test_increase_salary_rate(token, accounts):
    assert token.increase_salary_rate(int(50), sender=accounts[0])
    ### why ape.reverts doesn't work???
    #with ape.reverts("Wrong rate"):
    #    token.increase_salary_rate(int(23550e18), sender=accounts[0])
    assert token.increase_salary_rate(int(23550e18), sender=accounts[0]) == False ### this doesn't work too
    ### check SWD token contract it has ###assert _new_rate >= 50 or _new_rate <= 200, "Wrong rate"

def test_burn(token, accounts):
    token.burn(int(1000e18), sender=accounts[0])
    assert token.balanceOf(accounts[0]) == int(9000e18)

#check guardian
def test_set_guardian(token, accounts):
    token.set_guardian(accounts[1], sender=accounts[0])
    assert token.guardian() == accounts[1]

#check owner
def test_ask_guardian(token, accounts):
    token.set_guardian(accounts[1], sender=accounts[0])
    token.ask_owner(1, sender=accounts[0])
    assert token.guardian() == accounts[1]
    token.ask_guardian(1, sender=accounts[1])

#check owner
def test_ask_owner(token, accounts):
    token.set_guardian(accounts[1], sender=accounts[0])
    assert token.guardian() == accounts[1]
    token.ask_owner(1, sender=accounts[0])
    #assert token.owner_agree() == True
    token.ask_guardian(1, sender=accounts[1])
    #assert token.guardian_agree() == True

#check owner
def test_update_swd_owner(token, accounts):
    token.set_guardian(accounts[1], sender=accounts[0])
    token.ask_owner(1, sender=accounts[0])
    #assert token.owner_agree() == True
    assert token.guardian() == accounts[1]
    token.ask_guardian(1, sender=accounts[1])
    #assert token.guardian_agree() == True
    token.update_owner(accounts[3], sender=accounts[0])
    assert token.owner() == accounts[3]

#check update guard
def test_update_guard(token, accounts):
    token.set_guardian(accounts[1], sender=accounts[0])
    token.ask_owner(1, sender=accounts[0])
    #assert token.owner_agree() == True
    assert token.guardian() == accounts[1]
    token.ask_guardian(1, sender=accounts[1])
    #assert token.guardian_agree() == True
    token.update_guardian(sender=accounts[0])
    token.set_guardian(accounts[3], sender=accounts[0])
    assert token.guardian() == accounts[3]
# set a new guard # to do

# test reverts
def test_revert_mint_proof_of_trade(token, accounts):
    with ape.reverts():
        token.mint_proof_of_trade(int(1e18), sender=accounts[0])

def test_revert_max_dev_salary(token, accounts):
    with ape.reverts():
        token.dev_salary(accounts[1], int(1000000e18), sender=accounts[0]) # test max
    token.dev_salary(accounts[1], int(50e18), sender=accounts[0])
    with ape.reverts():
        token.dev_salary(accounts[1], int(1e18), sender=accounts[0]) # test time


def test_revert_register_deployer(deployer, station, token, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    with ape.reverts():
        token.register_deployer(sender=accounts[0])


def test_revert_update_deployer(deployer, station, token, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    token.set_guardian(accounts[1], sender=accounts[0])
    token.ask_owner(1, sender=accounts[0])
    token.ask_guardian(1, sender=accounts[1])
    with ape.reverts():
        token.update_deployer(sender=accounts[1])

    token.update_deployer(sender=accounts[0])

    token.new_deployer(accounts[2], sender=accounts[0])