import pytest
from brownie import SWDToken, PoTStation, SwapStation, SuperPool, Deployer, SwapRouter, accounts, ZERO_ADDRESS

@pytest.fixture
def deploy():
    token = accounts[0].deploy(SWDToken, "SwapDance", "DANCE", 10000, 30000000, 1000000000)
    tokenA = accounts[0].deploy(SWDToken, "AToken", "ATK", 100000, 30000000, 1000000000)
    tokenB = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    tokenC = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    tokenD = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    tokenF = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    tokenG = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    tokenW = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    tokenZ = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token1 = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token2 = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token3 = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token4 = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token5 = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token6 = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token7 = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token8 = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token9 = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)
    token10 = accounts[0].deploy(SWDToken, "BToken", "BTK", 100000, 30000000, 1000000000)

    #token1,token2,token3,token4,token5,token6,token7,token8,token9,token10,token11, token12, token13, token14, token15, token16, token17, token18, token19, token20,token21, token22, token23, token24, token25, token26, token27, token28, token29, token30,token31, token32, token33, token34, token35, token36, token37, token38, token39, token40,token41, token42, token43, token44, token45, token46, token47, token48, token49, token50, token51

    router = accounts[0].deploy(SwapRouter, token)
    pot = accounts[0].deploy(PoTStation, token)
    super = accounts[0].deploy(SuperPool, token, 180)
    station = accounts[0].deploy(SwapStation, token)
    deployer = accounts[0].deploy(Deployer, token, super, pot, station)
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