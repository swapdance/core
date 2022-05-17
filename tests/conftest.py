import pytest

@pytest.fixture
def owner(accounts):
    return accounts[0]

@pytest.fixture
def token(project, owner):
    return owner.deploy(project.SWDToken, "SwapDance", "DANCE", 10000, 30000000, 1000000000)

@pytest.fixture
def router(project, owner, token):
    return owner.deploy(project.SwapRouter, token)

@pytest.fixture
def pot(project, owner, token):
    return owner.deploy(project.PoTStation, token)

@pytest.fixture
def super(project, owner, token):
    return owner.deploy(project.SuperPool, token, 180)

@pytest.fixture
def station(project, owner, token):
    return owner.deploy(project.SwapStation, token)

@pytest.fixture
def deployer(project, owner, token, super, pot, station):
    return owner.deploy(project.Deployer, token, super, pot, station)

### MORE TOKENS ###
@pytest.fixture
def token1(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token1(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token2(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token3(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token4(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token5(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token6(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token7(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token8(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token9(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def token10(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def tokenA(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def tokenB(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def tokenC(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def tokenD(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def tokenF(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def tokenG(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def tokenW(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture
def tokenK(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)