import pytest

@pytest.fixture(scope="session")
def owner(accounts):
    return accounts[0]

@pytest.fixture(scope="session")
def token(project, owner):
    return owner.deploy(project.SWDToken, "SwapDance", "DANCE", 10000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def router(project, owner, token):
    return owner.deploy(project.SwapRouter, token)

@pytest.fixture(scope="session")
def pot(project, owner, token):
    return owner.deploy(project.PoTStation, token)

@pytest.fixture(scope="session")
def super(project, owner, token):
    return owner.deploy(project.SuperPool, token, 180)

@pytest.fixture(scope="session")
def station(project, owner, token):
    return owner.deploy(project.SwapStation, token)

@pytest.fixture(scope="session")
def deployer(project, owner, token, super, pot, station):
    return owner.deploy(project.Deployer, token, super, pot, station)

### MORE TOKENS ###
@pytest.fixture(scope="session")
def token1(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def token1(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def token2(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def token3(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def token4(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def token5(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def token6(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def token8(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def token9(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def token10(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def tokenA(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def tokenB(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def tokenC(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def tokenD(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def tokenF(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def tokenG(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def tokenW(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)

@pytest.fixture(scope="session")
def tokenZ(project, owner):
    return owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)