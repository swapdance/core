import pytest
from brownie import SWDToken, PoTStation, SwapStation, SuperPool, Deployer, SwapRouter, accounts, ZERO_ADDRESS

@pytest.fixture
def owner(accounts):
    return accounts[0]

@pytest.fixture
def token(owner):
    return owner.deploy(SWDToken, "SwapDance", "DANCE", 10000, 30000000, 1000000000)

@pytest.fixture
def router(owner, token):
    return owner.deploy(SwapRouter, token)

@pytest.fixture
def pot(owner, token):
    return owner.deploy(PoTStation, token)

@pytest.fixture
def super(owner, token):
    return owner.deploy(SuperPool, token, 180)

@pytest.fixture
def station(owner, token):
    return owner.deploy(SwapStation, token)

@pytest.fixture
def deployer(owner, token, super, pot, station):
    return owner.deploy(Deployer, token, super, pot, station)

### MORE TOKENS ###
@pytest.fixture
def token1(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token1(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token2(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token3(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token4(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token5(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token6(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token7(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token8(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token9(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token10(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def tokenA(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def tokenB(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def tokenC(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def tokenD(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def tokenF(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def tokenG(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def tokenW(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def tokenK(owner):
    return owner.deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)