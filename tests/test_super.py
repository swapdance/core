import ape
from ape import project, chain
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
swap_count = 5

def test_update_owner(deployer, super, accounts):
    super.update_owner(deployer, sender=accounts[0])


def test_deposit(token, super, accounts):
    token.approve(super, int(1e18), sender=accounts[0])
    super.deposit(int(1e18), int(1e18), sender=accounts[0])
    assert super.balances(accounts[0]) == int(1e18)
    assert super.balances(accounts[1]) == 0

def test_withdraw_with_reward(
        deployer, station, token,
        tokenA, tokenB, tokenC,
        tokenD, tokenF, tokenG,
        tokenW, tokenK, super,
        token1, token2, token3,
        token4, token5, token6,
        token7, token8, token9,
        token10, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    deployer.add_approved_tokens(tokenC, sender=accounts[0])
    deployer.add_approved_tokens(tokenF, sender=accounts[0])
    deployer.add_approved_tokens(tokenW, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 4, 4, 0, int(1e18), sender=accounts[0])
    stable.initialize(tokenC, tokenD, 4, 4, 0, int(1e18), sender=accounts[0])
    stable.initialize(tokenF, tokenG, 4, 4, 0, int(1e18), sender=accounts[0])
    stable.initialize(tokenW, tokenK, 4, 4, 0, int(1e18), sender=accounts[0])
    stable.initialize(token1, token2, 4, 4, 0, int(1e18), sender=accounts[0])
    stable.initialize(token3, token4, 4, 4, 0, int(1e18), sender=accounts[0])
    stable.initialize(token5, token6, 4, 4, 0, int(1e18), sender=accounts[0])
    stable.initialize(token7, token8, 4, 4, 0, int(1e18), sender=accounts[0])
    stable.initialize(token9, token10, 4, 4, 0, int(1e18), sender=accounts[0])
    stable.initialize(tokenA, token10, 4, 4, 0, int(1e18), sender=accounts[0])
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    # add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr1 = new_station_info[0]
    new_station_info = deployer.get_pair_info(2)
    new_station_addr2 = new_station_info[0]
    new_station_info = deployer.get_pair_info(3)
    new_station_addr3 = new_station_info[0]
    new_station_info = deployer.get_pair_info(4)
    new_station_addr4 = new_station_info[0]
    new_station_info = deployer.get_pair_info(5)
    new_station_addr5 = new_station_info[0]
    new_station_info = deployer.get_pair_info(6)
    new_station_addr6 = new_station_info[0]
    new_station_info = deployer.get_pair_info(7)
    new_station_addr7 = new_station_info[0]
    new_station_info = deployer.get_pair_info(8)
    new_station_addr8 = new_station_info[0]
    new_station_info = deployer.get_pair_info(9)
    new_station_addr9 = new_station_info[0]
    new_station_info = deployer.get_pair_info(10)
    new_station_addr10 = new_station_info[0]
    stable.initialize_pot_station(new_station_addr1, int(1e18), sender=accounts[0])

    station1 = project.SwapStation.at(new_station_addr1)
    station2 = project.SwapStation.at(new_station_addr2)
    station3 = project.SwapStation.at(new_station_addr3)
    station4 = project.SwapStation.at(new_station_addr4)
    station5 = project.SwapStation.at(new_station_addr5)
    station6 = project.SwapStation.at(new_station_addr6)
    station7 = project.SwapStation.at(new_station_addr7)
    station8 = project.SwapStation.at(new_station_addr8)
    station9 = project.SwapStation.at(new_station_addr9)
    station10 = project.SwapStation.at(new_station_addr10)

    tokenA.approve(new_station_addr1, int(10000e18), sender=accounts[0])
    tokenB.approve(new_station_addr1, int(10000e18), sender=accounts[0])
    station1.add_liquidity(int(10000e18), int(10000e18), int(10000e18), int(10000e18), int(1e18), sender=accounts[0])

    tokenC.approve(new_station_addr2, int(10000e18), sender=accounts[0])
    tokenD.approve(new_station_addr2, int(10000e18), sender=accounts[0])
    station2.add_liquidity(int(10000e18), int(10000e18), int(10000e18), int(10000e18), int(1e18), sender=accounts[0])

    tokenF.approve(new_station_addr3, int(10000e18), sender=accounts[0])
    tokenG.approve(new_station_addr3, int(10000e18), sender=accounts[0])
    station3.add_liquidity(int(10000e18), int(10000e18), int(10000e18), int(10000e18), int(1e18), sender=accounts[0])

    tokenW.approve(new_station_addr4, int(10000e18), sender=accounts[0])
    tokenK.approve(new_station_addr4, int(10000e18), sender=accounts[0])
    station4.add_liquidity(int(10000e18), int(10000e18), int(10000e18), int(10000e18), int(1e18), sender=accounts[0])

    token1.approve(new_station_addr5, int(10000e18), sender=accounts[0])
    token2.approve(new_station_addr5, int(10000e18), sender=accounts[0])
    station5.add_liquidity(int(10000e18), int(10000e18), int(10000e18), int(10000e18), int(1e18), sender=accounts[0])

    token3.approve(new_station_addr6, int(10000e18), sender=accounts[0])
    token4.approve(new_station_addr6, int(10000e18), sender=accounts[0])
    station6.add_liquidity(int(10000e18), int(10000e18), int(10000e18), int(10000e18), int(1e18), sender=accounts[0])

    token5.approve(new_station_addr7, int(10000e18), sender=accounts[0])
    token6.approve(new_station_addr7, int(10000e18), sender=accounts[0])
    station7.add_liquidity(int(10000e18), int(10000e18), int(10000e18), int(10000e18), int(1e18), sender=accounts[0])

    token7.approve(new_station_addr8, int(10000e18), sender=accounts[0])
    token8.approve(new_station_addr8, int(10000e18), sender=accounts[0])
    station8.add_liquidity(int(10000e18), int(10000e18), int(10000e18), int(10000e18), int(1e18), sender=accounts[0])

    token9.approve(new_station_addr9, int(10000e18), sender=accounts[0])
    token10.approve(new_station_addr9, int(10000e18), sender=accounts[0])
    station9.add_liquidity(int(10000e18), int(10000e18), int(10000e18), int(10000e18), int(1e18), sender=accounts[0])

    token10.approve(new_station_addr10, int(10000e18), sender=accounts[0])
    tokenA.approve(new_station_addr10, int(10000e18), sender=accounts[0])
    station10.add_liquidity(int(10000e18), int(10000e18), int(10000e18), int(10000e18), int(1e18), sender=accounts[0])
    # make some swaps to receive station fees
    k = 0
    while k < 10:
        tokenA.approve(new_station_addr1, int(3000e18), sender=accounts[0])
        tokenB.approve(new_station_addr1, int(3000e18), sender=accounts[0])
        for i in range(swap_count):
            station1.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        for i in range(swap_count):
            station1.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        k += 1

    k = 0
    while k < 10:
        tokenC.approve(new_station_addr2, int(3000e18), sender=accounts[0])
        tokenD.approve(new_station_addr2, int(3000e18), sender=accounts[0])
        for i in range(swap_count):
            station2.swap_tokens(int(100e18), int(99e18), tokenC, int(1e18), sender=accounts[0])
        for i in range(swap_count):
            station2.swap_tokens(int(100e18), int(99e18), tokenD, int(1e18), sender=accounts[0])
        k += 1

    k = 0
    while k < 10:
        tokenF.approve(new_station_addr3, int(3000e18), sender=accounts[0])
        tokenG.approve(new_station_addr3, int(3000e18), sender=accounts[0])
        for i in range(swap_count):
            station3.swap_tokens(int(100e18), int(99e18), tokenF, int(1e18), sender=accounts[0])
        for i in range(swap_count):
            station3.swap_tokens(int(100e18), int(99e18), tokenG, int(1e18), sender=accounts[0])
        k += 1

    k = 0
    while k < 10:
        tokenW.approve(new_station_addr4, int(3000e18), sender=accounts[0])
        tokenK.approve(new_station_addr4, int(3000e18), sender=accounts[0])
        for i in range(swap_count):
            station4.swap_tokens(int(100e18), int(99e18), tokenW, int(1e18), sender=accounts[0])
        for i in range(swap_count):
            station4.swap_tokens(int(100e18), int(99e18), tokenK, int(1e18), sender=accounts[0])
        k += 1
    k = 0

    while k < 10:
        tokenA.approve(new_station_addr10, int(3000e18), sender=accounts[0])
        token10.approve(new_station_addr10, int(3000e18), sender=accounts[0])
        for i in range(swap_count):
            station10.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        for i in range(swap_count):
            station10.swap_tokens(int(100e18), int(99e18), token10, int(1e18), sender=accounts[0])
        k += 1
    k = 0

    while k < 10:
        token1.approve(new_station_addr5, int(3000e18), sender=accounts[0])
        token2.approve(new_station_addr5, int(3000e18), sender=accounts[0])
        for i in range(swap_count):
            station5.swap_tokens(int(100e18), int(99e18), token1, int(1e18), sender=accounts[0])
        for i in range(swap_count):
            station5.swap_tokens(int(100e18), int(99e18), token2, int(1e18), sender=accounts[0])
        k += 1
    k = 0

    while k < 10:
        token3.approve(new_station_addr6, int(3000e18), sender=accounts[0])
        token4.approve(new_station_addr6, int(3000e18), sender=accounts[0])
        for i in range(swap_count):
            station6.swap_tokens(int(100e18), int(99e18), token3, int(1e18), sender=accounts[0])
        for i in range(swap_count):
            station6.swap_tokens(int(100e18), int(99e18), token4, int(1e18), sender=accounts[0])
        k += 1
    k = 0

    while k < 10:
        token5.approve(new_station_addr7, int(3000e18), sender=accounts[0])
        token6.approve(new_station_addr7, int(3000e18), sender=accounts[0])
        for i in range(swap_count):
            station7.swap_tokens(int(100e18), int(99e18), token5, int(1e18), sender=accounts[0])
        for i in range(swap_count):
            station7.swap_tokens(int(100e18), int(99e18), token6, int(1e18), sender=accounts[0])
        k += 1
    k = 0

    while k < 10:
        token7.approve(new_station_addr8, int(3000e18), sender=accounts[0])
        token8.approve(new_station_addr8, int(3000e18), sender=accounts[0])
        for i in range(swap_count):
            station8.swap_tokens(int(100e18), int(99e18), token7, int(1e18), sender=accounts[0])
        for i in range(swap_count):
            station8.swap_tokens(int(100e18), int(99e18), token8, int(1e18), sender=accounts[0])
        k += 1
    k = 0

    while k < 10:
        token9.approve(new_station_addr9, int(3000e18), sender=accounts[0])
        token10.approve(new_station_addr9, int(3000e18), sender=accounts[0])
        for i in range(swap_count):
            station9.swap_tokens(int(100e18), int(99e18), token9, int(1e18), sender=accounts[0])
        for i in range(swap_count):
            station9.swap_tokens(int(100e18), int(99e18), token10, int(1e18), sender=accounts[0])
        k += 1

    # remove liquidity
    station1.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station2.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station3.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station4.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station5.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station6.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station7.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station8.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station9.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station10.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])

    token.transfer(accounts[1], int(1000e18), sender=accounts[0])
    token.transfer(accounts[2], int(825e18), sender=accounts[0])
    token.transfer(accounts[3], int(1000e18), sender=accounts[0])
    token.transfer(accounts[4], int(700e18), sender=accounts[0])
    token.transfer(accounts[5], int(1024e18), sender=accounts[0])

    #deposit to super pool
    #user0
    token.approve(super, int(3000e18), sender=accounts[0])
    super.deposit(int(3000e18), int(1e18), sender=accounts[0])
    assert super.balances(accounts[0]) == int(3000e18)
    #user1
    token.approve(super, int(1000e18), sender=accounts[1])
    super.deposit(int(1000e18), int(1e18), sender=accounts[1])
    assert super.balances(accounts[1]) == int(1000e18)
    #user2
    token.approve(super, int(825e18), sender=accounts[2])
    super.deposit(int(825e18), int(1e18), sender=accounts[2])
    assert super.balances(accounts[2]) == 825e18
    #user3
    token.approve(super, int(1000e18), sender=accounts[3])
    super.deposit(int(1000e18), int(1e18), sender=accounts[3])
    assert super.balances(accounts[3]) == int(1000e18)
    #user4
    token.approve(super, int(700e18), sender=accounts[4])
    super.deposit(int(700e18), int(1e18), sender=accounts[4])
    assert super.balances(accounts[4]) == 700e18
    #user5
    token.approve(super, int(1024e18), sender=accounts[5])
    super.deposit(int(1024e18), int(1e18), sender=accounts[5])
    assert super.balances(accounts[5]) == int(1024e18)

    #7549 total locked (swap count = 5)
    # user 0 reward 0.01191079198
    # user 1 reward 0.00397026399
    # user 2 reward 0.00327546779
    # user 3 reward 0.00397026399
    # user 4 reward 0.00277918479
    # user 5 reward 0.00406555032

    deployer.lock_super_pool(1, sender=accounts[0])

    old_bal1 = station1.balanceOf(super)
    old_bal2 = station2.balanceOf(super)
    old_bal3 = station3.balanceOf(super)
    old_bal4 = station4.balanceOf(super)
    old_bal5 = station5.balanceOf(super)
    old_bal6 = station6.balanceOf(super)
    old_bal7 = station7.balanceOf(super)
    old_bal8 = station8.balanceOf(super)
    old_bal9 = station9.balanceOf(super)
    old_bal10 = station10.balanceOf(super)

    tokens_map = [
        new_station_addr1, new_station_addr2,
        new_station_addr3, new_station_addr4,
        new_station_addr5, new_station_addr6,
        new_station_addr7, new_station_addr8,
        new_station_addr9, new_station_addr10
    ]
    tokens_map_dubles = [
        new_station_addr1, new_station_addr2,
        new_station_addr3, new_station_addr4,
        new_station_addr5, new_station_addr6,
        new_station_addr7, new_station_addr8,
        new_station_addr9, new_station_addr1
    ]
    with ape.reverts():
        super.get_reward_and_withdraw(tokens_map_dubles, int(1e18), sender=accounts[0])

    super.get_reward_and_withdraw(tokens_map, int(1e18), sender=accounts[0])
    super.get_reward_and_withdraw(tokens_map, int(1e18), sender=accounts[1])
    super.get_reward_and_withdraw(tokens_map, int(1e18), sender=accounts[2])
    super.get_reward_and_withdraw(tokens_map, int(1e18), sender=accounts[3])
    super.get_reward_and_withdraw(tokens_map, int(1e18), sender=accounts[4])
    super.get_reward_and_withdraw(tokens_map, int(1e18), sender=accounts[5])

    # calc super balances after distr (should be ~ 10% from initial balances)
    assert station1.balanceOf(super) >= old_bal1/10
    assert station2.balanceOf(super) >= old_bal2/10
    assert station3.balanceOf(super) >= old_bal3/10
    assert station4.balanceOf(super) >= old_bal4/10
    assert station5.balanceOf(super) >= old_bal5/10
    assert station6.balanceOf(super) >= old_bal6/10
    assert station7.balanceOf(super) >= old_bal7/10
    assert station8.balanceOf(super) >= old_bal8/10
    assert station9.balanceOf(super) >= old_bal9/10
    assert station10.balanceOf(super) >= old_bal10/10
    print("old_bal1", old_bal1, old_bal2, old_bal3, old_bal4, old_bal5, old_bal6, old_bal7, old_bal8, old_bal9, old_bal10)
    assert station1.balanceOf(accounts[0]) >= int(0.01191079198e18)
    assert station1.balanceOf(accounts[1]) >= int(0.00397026399e18)
    assert station2.balanceOf(accounts[2]) >= int(0.00327546779e18)
    assert station3.balanceOf(accounts[3]) >= int(0.00397026399e18)
    assert station4.balanceOf(accounts[4]) >= int(0.00277918479e18)
    assert station5.balanceOf(accounts[5]) >= int(0.00406555032e18)


    assert token.balanceOf(accounts[1]) == int(1000e18)
    assert token.balanceOf(accounts[2]) == int(825e18)
    assert token.balanceOf(accounts[3]) == int(1000e18)
    assert token.balanceOf(accounts[4]) == int(700e18)
    assert token.balanceOf(accounts[5]) == int(1024e18)
    # test burn function
    # unlock to increase burn percent
    with ape.reverts():
        deployer.lock_super_pool(0, sender=accounts[0])

    chain.pending_timestamp += 181

    deployer.lock_super_pool(0, sender=accounts[0])
    # make some swaps to receive station fees
    k = 0
    while k < 10:
        tokenA.approve(new_station_addr1, int(3000e18), sender=accounts[0])
        tokenB.approve(new_station_addr1, int(3000e18), sender=accounts[0])
        for i in range(swap_count):
            station1.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        for i in range(swap_count):
            station1.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        k += 1

    k = 0
    while k < 10:
        tokenC.approve(new_station_addr2, int(3000e18), sender=accounts[0])
        tokenD.approve(new_station_addr2, int(3000e18), sender=accounts[0])
        for i in range(swap_count):
            station2.swap_tokens(int(100e18), int(99e18), tokenC, int(1e18), sender=accounts[0])
        for i in range(swap_count):
            station2.swap_tokens(int(100e18), int(99e18), tokenD, int(1e18), sender=accounts[0])
        k += 1

    k = 0
    while k < 10:
        tokenF.approve(new_station_addr3, int(3000e18), sender=accounts[0])
        tokenG.approve(new_station_addr3, int(3000e18), sender=accounts[0])
        for i in range(swap_count):
            station3.swap_tokens(int(100e18), int(99e18), tokenF, int(1e18), sender=accounts[0])
        for i in range(swap_count):
            station3.swap_tokens(int(100e18), int(99e18), tokenG, int(1e18), sender=accounts[0])
        k += 1

    k = 0
    while k < 10:
        tokenW.approve(new_station_addr4, int(3000e18), sender=accounts[0])
        tokenK.approve(new_station_addr4, int(3000e18), sender=accounts[0])
        for i in range(swap_count):
            station4.swap_tokens(int(100e18), int(99e18), tokenW, int(1e18), sender=accounts[0])
        for i in range(swap_count):
            station4.swap_tokens(int(100e18), int(99e18), tokenK, int(1e18), sender=accounts[0])
        k += 1

    station1.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station2.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station3.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station4.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station4.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    # test remove w/o super pool fees
    station5.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station6.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station7.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station8.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station9.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    station10.remove_liquidity(int(1e18), int(9e17), int(9e17), int(1e18), sender=accounts[0])
    #deposit to super pool
    #user0
    token.approve(super, int(3000e18), sender=accounts[0])
    super.deposit(int(3000e18), int(1e18), sender=accounts[0])
    assert super.balances(accounts[0]) == int(3000e18)
    #user1
    token.approve(super, int(1000e18), sender=accounts[1])
    super.deposit(int(1000e18), int(1e18), sender=accounts[1])
    assert super.balances(accounts[1]) == int(1000e18)
    #user2
    token.approve(super, int(825e18), sender=accounts[2])
    super.deposit(int(825e18), int(1e18), sender=accounts[2])
    assert super.balances(accounts[2]) == 825e18
    #user3
    token.approve(super, int(1000e18), sender=accounts[3])
    super.deposit(int(1000e18), int(1e18), sender=accounts[3])
    assert super.balances(accounts[3]) == int(1000e18)
    #user4
    token.approve(super, int(700e18), sender=accounts[4])
    super.deposit(int(700e18), int(1e18), sender=accounts[4])
    assert super.balances(accounts[4]) == 700e18
    #user5
    token.approve(super, int(1024e18), sender=accounts[5])
    super.deposit(int(1024e18), int(1e18), sender=accounts[5])
    assert super.balances(accounts[5]) == 1024e18

    deployer.lock_super_pool(1, sender=accounts[0])


    old_bal1 = station1.balanceOf(super)
    old_bal2 = station2.balanceOf(super)
    old_bal3 = station3.balanceOf(super)
    old_bal4 = station4.balanceOf(super)
    old_bal5 = station5.balanceOf(super)
    old_bal6 = station6.balanceOf(super)
    old_bal7 = station7.balanceOf(super)
    old_bal8 = station8.balanceOf(super)
    old_bal9 = station9.balanceOf(super)
    old_bal10 = station10.balanceOf(super)

    tokens_map = [
        new_station_addr1, new_station_addr2,
        new_station_addr3, new_station_addr4,
        new_station_addr5, new_station_addr6,
        new_station_addr7, new_station_addr8,
        new_station_addr9, new_station_addr10
    ]
    tokens_map_dubles = [
        new_station_addr1, new_station_addr2,
        new_station_addr3, new_station_addr4,
        new_station_addr5, new_station_addr6,
        new_station_addr7, new_station_addr8,
        new_station_addr9, new_station_addr1
    ]
    with ape.reverts():
        super.get_reward_and_withdraw(tokens_map_dubles, int(1e18), sender=accounts[0])

    super.get_reward_and_withdraw(tokens_map, int(1e18), sender=accounts[0])
    super.get_reward_and_withdraw(tokens_map, int(1e18), sender=accounts[1])
    super.get_reward_and_withdraw(tokens_map, int(1e18), sender=accounts[2])
    super.get_reward_and_withdraw(tokens_map, int(1e18), sender=accounts[3])
    super.get_reward_and_withdraw(tokens_map, int(1e18), sender=accounts[4])
    super.get_reward_and_withdraw(tokens_map, int(1e18), sender=accounts[5])

    print("old_bal1", old_bal1, old_bal2, old_bal3, old_bal4, old_bal5, old_bal6, old_bal7, old_bal8, old_bal9,
          old_bal10)
    # calc super balances after distr (should be ~ 10% from initial balances)
    # total lp collected st1, st2, st3, st4 0.03662531361
    # st5, st6, st7, st8, st9, st10 0.00333016921 - these pair didn't return any profit
    assert station1.balanceOf(super) >= old_bal1/10
    assert station2.balanceOf(super) >= old_bal2/10
    assert station3.balanceOf(super) >= old_bal3/10
    assert station4.balanceOf(super) >= old_bal4/10
    assert station5.balanceOf(super) >= old_bal5/10
    assert station6.balanceOf(super) >= old_bal6/10
    assert station7.balanceOf(super) >= old_bal7/10
    assert station8.balanceOf(super) >= old_bal8/10
    assert station9.balanceOf(super) >= old_bal9/10
    assert station10.balanceOf(super) >= old_bal10/10

    #assert station1.balanceOf(accounts[0]) == 0.01191079198e18 + 0.00436650976e18*3
    assert station1.balanceOf(accounts[1]) >= 0.00397026399e18 + 0.00436650976e18
    assert station2.balanceOf(accounts[2]) >= 0.00327546779e18 + 0.00360237055e18
    assert station3.balanceOf(accounts[3]) >= 0.00397026399e18 + 0.00436650976e18
    assert station4.balanceOf(accounts[4]) >= 0.00277918479e18 + 0.00305655683e18
    assert station5.balanceOf(accounts[5]) >= 0.00406555032e18 + 0.00040655503e18
    # -1% burn
    assert token.balanceOf(accounts[1]) >= (int(1000e18) - int(1000e18)/100)
    assert token.balanceOf(accounts[2]) >= int(816.75e18)
    assert token.balanceOf(accounts[3]) >= (int(1000e18) - int(1000e18)/100)
    assert token.balanceOf(accounts[4]) >= int(693e18)
    assert token.balanceOf(accounts[5]) >= int(1013.76e18)

    with ape.reverts():
        deployer.lock_super_pool(0, sender=accounts[0])

    chain.pending_timestamp += 181

    deployer.lock_super_pool(0, sender=accounts[0])

    token.approve(super, int(10e18), sender=accounts[1])
    super.deposit(10e18, int(1e18), sender=accounts[1])

    deployer.lock_super_pool(1, sender=accounts[0])
    # make some swaps to receive station fees
    with ape.reverts():
        deployer.lock_super_pool(0, sender=accounts[0])

    chain.pending_timestamp += 181

    deployer.lock_super_pool(0, sender=accounts[0])
    deployer.lock_super_pool(1, sender=accounts[0])


def test_withdraw_without_reward(deployer, station, token, super, accounts):
    stable = station
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    old_balance = token.balanceOf(accounts[0])
    token.approve(super, int(1e18), sender=accounts[0])
    super.deposit(int(1e18), int(1e18), sender=accounts[0])
    assert super.balances(accounts[0]) == int(1e18)
    assert token.balanceOf(super) == int(1e18)
    assert token.balanceOf(accounts[0]) == old_balance - int(1e18)
    assert super.balances(accounts[1]) == 0
    super.withdraw_without_reward(int(1e18), sender=accounts[0])
    assert super.balances(accounts[0]) == 0
    assert token.balanceOf(super) == 0
    assert token.balanceOf(accounts[0]) == old_balance
