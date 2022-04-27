import pytest

@pytest.fixture
def owner(accounts):
    return accounts[0]

@pytest.fixture
def deploy(owner, project):
    token = owner.deploy(project.SWDToken, "SwapDance", "DANCE", 10000, 30000000, 1000000000)
    tokenA = owner.deploy(project.SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)
    tokenB = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    tokenC = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    tokenD = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    tokenF = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    tokenG = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    tokenW = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    tokenZ = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token1 = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token2 = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token3 = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token4 = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token5 = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token6 = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token7 = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token8 = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token9 = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token10 = owner.deploy(project.SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)


    router = owner.deploy(project.SwapRouter, token)
    pot = owner.deploy(project.PoTStation, token)
    super = owner.deploy(project.SuperPool, token, 180)
    station = owner.deploy(project.SwapStation, token)
    deployer = owner.deploy(project.Deployer, token, super, pot, station)
    return (
        deployer, pot,
        super, station,
        token, tokenA,
        tokenB, router,
        tokenC, tokenD,
        tokenF, tokenG,
        tokenW, tokenZ,
        token1, token2,
        token3, token4,
        token5, token6,
        token7, token8,
        token9, token10
    )
