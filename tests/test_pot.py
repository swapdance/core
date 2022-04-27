from ape import project
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

def test_stake(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 4, 4, 0, int(1e18), sender=accounts[0])
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, int(1e18), sender=accounts[0])
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = project.PoTStation.at(pot_addr)
    station = project.SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, int(1000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(1000e18), sender=accounts[0])
    station.add_liquidity(int(1000e18), int(1000e18), int(1000e18), int(1000e18), int(1e18), sender=accounts[0])
    lp_token_balance = station.balanceOf(accounts[0])
    station.approve(pot_addr, lp_token_balance, sender=accounts[0])
    pot_station.stake(lp_token_balance, int(1e18), sender=accounts[0])
    # swap tokens to mint swd
    tokenA.approve(new_station_addr, int(int(700e18)), sender=accounts[0])
    tokenB.approve(new_station_addr, int(int(700e18)), sender=accounts[0])
    for i in range(7):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(7):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    user_reward = pot_station.actual_reward(accounts[0])
    assert user_reward != 0

def test_unstake(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 4, 4, 0, int(1e18), sender=accounts[0])
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, int(1e18), sender=accounts[0])
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = project.PoTStation.at(pot_addr)
    station = project.SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, int(1000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(1000e18), sender=accounts[0])
    station.add_liquidity(int(1000e18), int(1000e18), int(1000e18), int(1000e18), int(1e18), sender=accounts[0])
    lp_token_balance = station.balanceOf(accounts[0])
    station.approve(pot_addr, lp_token_balance, sender=accounts[0])
    pot_station.stake(lp_token_balance, int(1e18), sender=accounts[0])
    # swap tokens to mint swd
    tokenA.approve(new_station_addr, int(700e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(700e18), sender=accounts[0])
    for i in range(7):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(7):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    user_reward = pot_station.actual_reward(accounts[0])
    assert user_reward != 0
    assert station.balanceOf(pot_addr) > 0
    pot_station.unstake(int(1e18), sender=accounts[0]) # int(1e18) - expiry time
    assert station.balanceOf(pot_addr) == 0
    assert station.balanceOf(accounts[0]) == lp_token_balance

def test_update_owner(deploy, accounts):
    pot = deploy[1]
    pot.update_owner(accounts[1], sender=accounts[0])
    assert pot.owner() == accounts[1]

def test_update_lock(deploy, accounts):
    pot = deploy[1]
    pot.update_lock(1, sender=accounts[0])
    assert pot.lock() == True
    pot.update_lock(0, sender=accounts[0])
    assert pot.lock() == False

# Complicated Proof of trade tests

def test_complicated_stake(deploy, accounts):
    deployer = deploy[0]
    stable = deploy[3]
    token = deploy[4]
    tokenA = deploy[5]
    tokenB = deploy[6]
    super = deploy[2]
    super.update_owner(deployer, sender=accounts[0])
    stable.update_owner(deployer, sender=accounts[0])
    token.new_deployer(deployer, sender=accounts[0])
    deployer.register_deployer(sender=accounts[0])
    deployer.add_approved_tokens(tokenA, sender=accounts[0])
    stable.initialize(tokenA, tokenB, 4, 4, 0, int(1e18), sender=accounts[0])
    assert deployer.exchange_info(1) != ZERO_ADDRESS
    #add liquidity
    new_station_info = deployer.get_pair_info(1)
    new_station_addr = new_station_info[0]
    stable.initialize_pot_station(new_station_addr, int(1e18), sender=accounts[0])
    pot_addr = deployer.pot_station_list(new_station_addr)
    pot_station = project.PoTStation.at(pot_addr)
    station = project.SwapStation.at(new_station_addr)
    tokenA.approve(new_station_addr, int(10000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(10000e18), sender=accounts[0])
    station.add_liquidity(int(10000e18), int(10000e18), int(10000e18), int(10000e18), int(1e18), sender=accounts[0])

    # load balances
    station.transfer(accounts[1], int(100e18), sender=accounts[0])
    station.approve(pot_addr, int(100e18), sender=accounts[1])
    station.transfer(accounts[2], int(1000e18), sender=accounts[0])
    station.approve(pot_addr, int(1000e18), sender=accounts[2])
    station.transfer(accounts[3], int(600e18), sender=accounts[0])
    station.approve(pot_addr, int(600e18), sender=accounts[3])
    station.transfer(accounts[4], int(900e18), sender=accounts[0])
    station.approve(pot_addr, int(900e18), sender=accounts[4])
    station.transfer(accounts[5], int(2000e18), sender=accounts[0])
    station.approve(pot_addr, int(2000e18), sender=accounts[5])
    station.transfer(accounts[6], int(1990e18), sender=accounts[0])
    station.approve(pot_addr, int(1990e18), sender=accounts[6])
    station.transfer(accounts[7], int(500e18), sender=accounts[0])
    station.approve(pot_addr, int(500e18), sender=accounts[7])
    station.transfer(accounts[8], int(910e18), sender=accounts[0])
    station.approve(pot_addr, int(910e18), sender=accounts[8])
    station.transfer(accounts[9], int(1500e18), sender=accounts[0])
    station.approve(pot_addr, int(1500e18), sender=accounts[9])
    # stake/unstake random
    # Note 1st user has only 500 lp - 0.000000001 (Min liq)
    # several swaps before stake. for instance
    # to check end balance after distribution
    # for every swap, pot station receive < 0.03 and >0.029 swd in the mainnet
    # but in testing gas is lower so 1 reward ~ 0.01850336152
    lp_token_balance = station.balanceOf(accounts[0])
    assert int(lp_token_balance) == 499999999999000000000
    station.approve(pot_addr, lp_token_balance, sender=accounts[0])
    pot_station.stake(lp_token_balance, int(1e18), sender=accounts[0])
    # if one account will stake LPs
    # for example there will be 34 trades
    # so the end reward must be > 1 swd for only one user
    # test it for 1 user
    # 0.64390732 ~ 34 swaps ~ 0.01893845058
    tokenA.approve(new_station_addr, int(3000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(3000e18), sender=accounts[0])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    user_reward = pot_station.actual_reward(accounts[0])
    assert user_reward > int(0.6e18)
    # well everything goes good so
    # lets add a new user(1)
    # 2nd round start
    print("user_reward", user_reward)
    pot_station.stake(int(100e18), int(1e18), sender=accounts[1])
    #make some swaps again
    # user 2 has 100 lp
    tokenA.approve(new_station_addr, int(3000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(3000e18), sender=accounts[0])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    #so, 1st user receive > 1.26 at start and (0.64390732 / 500+100 ) * 500
    # 0.64390732 first user reward
    # second reward round is 0.64390732 for user1 and user2
    # ~ (0.64390732 / (500+100) ) * 500 = 0.52426191 for 1st user
    # ~ (0.64390732 / (500+100) ) * 100 = 0.104852382 for second user
    user_reward1_old = pot_station.actual_reward(accounts[0])
    user_reward2_old = pot_station.actual_reward(accounts[1])
    assert user_reward1_old > int(1.15e18)
    assert user_reward2_old > int(0.1e18)
    #lets add 3rd user
    pot_station.stake(int(1000e18), int(1e18), sender=accounts[2])
    #swap tokens
    # 3rd round start
    tokenA.approve(new_station_addr, int(3000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(3000e18), sender=accounts[0])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])


    user_reward3 = pot_station.actual_reward(accounts[2])
    assert user_reward3 > int(0.39e18)
    # 2nd user
    # (0.64390732/ (500+100+1000)) * 100 = 0.03931964325
    user_reward2 = pot_station.actual_reward(accounts[1])
    assert user_reward2 > (int(0.039e18) + user_reward2_old)
    # 1st user
    # (0.64390732/ (500+100+1000)) * 500 = 0.19659821625
    user_reward1 = pot_station.actual_reward(accounts[0])
    assert user_reward1 > (int(0.195e18) + user_reward1_old)
    # well... lets add one more user
    pot_station.stake(int(600e18), int(1e18), sender=accounts[3])
    # swap tokens to earn 0.64390732 swd
    tokenA.approve(new_station_addr, int(3000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(3000e18), sender=accounts[0])
    # swap to mint
    # 4th round start
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    # init get_reward for user2 and user1 (it will be count as start of the round n5)

    pot_station.get_reward(int(1e18), sender=accounts[0])
    pot_station.get_reward(int(1e18), sender=accounts[1])
    # full reward for user1 will be 0.19659821625 + 0.52426191 + 0.64390732
    # full reward for user2 will be 0.104852382 + 0.03931964325
    assert token.balanceOf(accounts[1]) >= 0.14e18
    #cal reward for user3 (0.64390732/ (500+100+1000+600)) * 600 ~ 0.17
    user_reward3 = pot_station.actual_reward(accounts[3])
    assert user_reward3 >= int(0.17e18)
    #lets unstake user1 with 100 lp
    #user1 already got its actual reward.
    #with unstake user1 can get round reward ~ 0.02859610418 == (0.64390732/ (500+100+1000+600))*100
    pot_station.unstake(int(1e18), sender=accounts[1])
    assert token.balanceOf(accounts[1]) >= 0.168e18
    # swap a little more, and let's add user 4
    pot_station.stake(int(900e18), int(1e18), sender=accounts[4])
    # 5th round start
    tokenA.approve(new_station_addr, int(3000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(3000e18), sender=accounts[0])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    # also lets restake user1 funds
    # (it will be count as start of the round n6)
    station.approve(pot_addr, int(100e18), sender=accounts[1])
    pot_station.stake(int(100e18), int(1e18), sender=accounts[1])

    #with this step we can get full reward and round reward == 0
    #also actual reward will be 0
    pot_station.get_reward(int(1e18), sender=accounts[0])
    pot_station.get_reward(int(1e18), sender=accounts[2])
    pot_station.get_reward(int(1e18), sender=accounts[3])
    pot_station.get_reward(int(1e18), sender=accounts[4])
    # assert actual reward == 0 for user0,2,3,4

    assert pot_station.actual_reward(accounts[4]) == 0
    assert pot_station.actual_reward(accounts[3]) == 0
    assert pot_station.actual_reward(accounts[2]) == 0
    assert pot_station.actual_reward(accounts[1]) == 0
    assert pot_station.actual_reward(accounts[0]) == 0

    # ok all rewards were withdrawn so actual == zero
    # bc all accs took their reward and user1 just stake
    # so its account[1] got zero too
    # lets make some  swaps again
    # 6th round start
    tokenA.approve(new_station_addr, int(3000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(3000e18), sender=accounts[0])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])

    # user5 with 2000 enter the game
    # (it will be count as start of the round n7)
    pot_station.stake(int(2000e18), int(1e18), sender=accounts[5])
    # 7th round start
    tokenA.approve(new_station_addr, int(3000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(3000e18), sender=accounts[0])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])

    # user5 with 2000 enter the game
    # (it will be count as start of the round n8)
    pot_station.stake(int(1990e18), int(1e18), sender=accounts[6])
    # 8th round start
    tokenA.approve(new_station_addr, int(3000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(3000e18), sender=accounts[0])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    # (it will be count as start of the round n9)
    #lets unstake user2(1k lp)
    pot_station.unstake(int(1e18), sender=accounts[2])
    # 9th round start 2xSWAPS
    tokenA.approve(new_station_addr, int(3000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(3000e18), sender=accounts[0])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    tokenA.approve(new_station_addr, int(3000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(3000e18), sender=accounts[0])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])

    # (it will be count as start of the round n10)
    pot_station.stake(int(500e18), int(1e18), sender=accounts[7])

    pot_station.unstake(int(1e18), sender=accounts[3])
    # 10th round start
    tokenA.approve(new_station_addr, int(3000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(3000e18), sender=accounts[0])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    # (it will be count as start of the round n11)
    pot_station.stake(int(910e18), int(1e18), sender=accounts[8])
    pot_station.stake(int(1500e18), int(1e18), sender=accounts[9])
    station.approve(pot_addr, int(600e18), sender=accounts[3])
    pot_station.stake(int(600e18), int(1e18), sender=accounts[3])
    station.approve(pot_addr, int(1000e18), sender=accounts[2])
    pot_station.stake(int(1000e18), int(1e18), sender=accounts[2])
    #station.approve(pot_addr, int(100e18), sender=accounts[1])
    #pot_station.stake(int(100e18), sender=accounts[1])

    # 11th round start 4xSWAPS
    tokenA.approve(new_station_addr, int(3000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(3000e18), sender=accounts[0])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    tokenA.approve(new_station_addr, int(3000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(3000e18), sender=accounts[0])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    tokenA.approve(new_station_addr, int(3000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(3000e18), sender=accounts[0])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    tokenA.approve(new_station_addr, int(3000e18), sender=accounts[0])
    tokenB.approve(new_station_addr, int(3000e18), sender=accounts[0])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenA, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])
    for i in range(17):
        station.swap_tokens(int(100e18), int(99e18), tokenB, int(1e18), sender=accounts[0])
        station.force_reward(sender=accounts[7])


    pot_station.unstake(int(1e18), sender=accounts[0])
    pot_station.unstake(int(1e18), sender=accounts[1])
    pot_station.unstake(int(1e18), sender=accounts[2])
    pot_station.unstake(int(1e18), sender=accounts[3])
    pot_station.unstake(int(1e18), sender=accounts[4])
    pot_station.unstake(int(1e18), sender=accounts[5])
    pot_station.unstake(int(1e18), sender=accounts[6])
    pot_station.unstake(int(1e18), sender=accounts[7])
    pot_station.unstake(int(1e18), sender=accounts[8])
    pot_station.unstake(int(1e18), sender=accounts[9])
    assert token.balanceOf(pot_addr) <= 30000 ### there may be some precision loss
    # there are small account balance due to precision loss
    # NOTE. it's 2000e18/10**18
    # cal. total balance
    # for account[0] BalanceNow - 30k(init mint)
    # 34 swaps ==  0.64390732 minted SWD
    # first round only user0
    # 2nd round - user0 and user1
    # 3rd round - user0, user1 and user2
    # 4th round - user0, user1, user2 and user3
    # 5th round, (user0, user1) - init get_reward, (user1 has unstaked its lps), user2, user3, user4
    # 6th round - user0, user1(restake), (user0, user2, user3, user4 - init get_reward)
    # 7th round - user0, user1, user2, user3, user4, user5
    # 8th round - user0, user1, user2, user3, user4, user5, user6
    # 9th round - user0, user1, user2(unstake), user3, user4, user5, user6 - 2xSWAPS
    # 10th round - user0, user1, user3(unstake), user4, user5, user6, user7
    # 11th round - user0, user1, user2(restake), user3(restake), user4, user5, user6, user7, user8, user9 - 4xSWAPS
    # unstake all account

    # 1st round (0.64390732/499.999999999 * 499.999999999) rate = 0.64390732

    # 2nd round rate = 0.00107317886 = (0.64390732/(499.999999999 + 100))
    # 2nd round 0.00107317886 * 499.999999999 user0 + 1st round = 0.53658942999 + 0.64390732
    # 2nd round 0.00107317886 * 100 user1 = 0.107317886

    # 3rd round rate 0.00040244207 = (0.64390732/(499.999999999 + 100 + 1000))
    # 3rd round 0.00040244207 * 500 user0 + 1st round + 2nd round = 0.201221035 + 0.53658942999 + 0.64390732
    # 3rd round 0.00040244207 * 100 user1 + 2nd round 0.040244207 + 0.107317886
    # 3rd round 0.00040244207 * 1000 user2 = 0.40244207

    # 4th round rate = 0.00029268514 = (0.64390732/(499.999999999 + 100 + 1000 + 600))
    # 4th round 0.00029268514 * 500 user0 + 1st round + 2nd round + 3rd round = 0.14634257 + 0.201221035 + 0.53658942999 + 0.64390732
    # 4th round 0.00029268514 * 100 user1 + 2nd round + 3rd round = 0.029268514 + 0.040244207 + 0.107317886
    # 4th round 0.00029268514 * 1000 user2 + 3rd round = 0.29268514 + 0.40244207
    # 4th round 0.00029268514 * 600 user3 = 0.175611084

    # !!! 5th round (0.64390732/(499.999999999 + 100 + 1000 + 600)) * 100 user1 + 2nd round + 3rd round + 4th round - unstaked


    # 5th raund rate = 0.00021463577 = (0.64390732/(499.999999999 + 1000 + 600 + 900))
    # 5th round 0.00021463577 * 500 user0 + 1st round + 2nd round + 3rd round + 4th round = 0.107317885 + 0.14634257 + 0.201221035 + 0.53658942999 + 0.64390732
    # 5th round 0.00021463577 * 1000 user2 + 3rd round + 4th round = 0.21463577 + 0.29268514 + 0.40244207
    # 5th round 0.00021463577 * 600 user3 + 4th round = 0.128781462 + 0.175611084
    # 5th round 0.00021463577 * 900 user4 = 0.193172193

    # 6th round rate 0.00020771203 = (0.64390732/(499.999999999 + 100 + 1000 + 600 + 900)) - user1 restake
    # 6th round 0.00020771203 * 500 user0 + 1st round + 2nd round + 3rd round + 4th round + 5th round = 0.103856015 + 0.107317885 + 0.14634257 + 0.201221035 + 0.53658942999 + 0.64390732
    # 6th round 0.00020771203 * 1000 user2 + 3rd round + 4th round + 5th round = 0.20771203 + 0.21463577 + 0.29268514 + 0.40244207
    # 6th round 0.00020771203 * 600 user3 + 4th round + 5th round = 0.124627218 + 0.128781462 + 0.175611084
    # 6th round 0.00020771203 * 900 user4 + 5th round = 0.186940827 + 0.193172193
    # 6th round 0.00020771203 * 100 user1 = 0.020771203



    # 7th round rate 0.00012625633 = (0.64390732/(499.999999999 + 100 + 1000 + 600 + 2000 + 900))
    # 7th round 0.00012625633 * 500 user0 + 1st round + 2nd round + 3rd round + 4th round + 5th round + 6th round = 0.063128165 + 0.103856015 + 0.107317885 + 0.14634257 + 0.201221035 + 0.53658942999 + 0.64390732
    # 7th round 0.00012625633 * 1000 user2 + 3rd round + 4th round + 5th round + 6th round = 0.12625633 + 0.20771203 + 0.21463577 + 0.29268514 + 0.40244207
    # 7th round 0.00012625633 * 600 user3 + 4th round + 5th round + 6th round = 0.075753798 + 0.124627218 + 0.128781462 + 0.175611084
    # 7th round 0.00012625633 * 900 user4 + 5th round + 6th round = 0.113630697 + 0.186940827 + 0.193172193
    # 7th round 0.00012625633 * 100 user1 + 6th round = 0.012625633 + 0.020771203
    # 7th round 0.00012625633 * 2000 user5 = 0.25251266

    # 8th round rate 0.00009081908 = (0.64390732/(499.999999999 + 100 + 1000 + 600 + 2000 + 1990 + 900))
    # 8th round 0.00009081908 * 500 user0 + 1st round + 2nd round + 3rd round + 4th round + 5th round + 6th round + 7th round = 0.04540954 + 0.063128165 + 0.103856015 + 0.107317885 + 0.14634257 + 0.201221035 + 0.53658942999 + 0.64390732
    # 8th round 0.00009081908 * 1000 user2 + 3rd round + 4th round + 5th round + 6th round + 7th round = 0.09081908 + 0.12625633 + 0.20771203 + 0.21463577 + 0.29268514 + 0.40244207
    # 8th round 0.00009081908 * 600 user3 + 4th round + 5th round + 6th round + 7th round = 0.054491448 + 0.075753798 + 0.124627218 + 0.128781462 + 0.175611084
    # 8th round 0.00009081908 * 900 user4 + 5th round + 6th round + 7th round = 0.081737172 + 0.113630697 + 0.186940827 + 0.193172193
    # 8th round 0.00009081908 * 100 user1 + 6th round + 7th round = 0.009081908 + 0.012625633 + 0.020771203
    # 8th round 0.00009081908 * 2000 user5 + 7th round = 0.18163816 + 0.25251266
    # 8th round 0.00009081908 * 1990 user6 = 0.1807299692


####
    # 9th round rate 0.00021146381 = (0.64390732*2/(499.999999999 + 100 + 600 + 2000 + 1990 + 900))
    # 9th round 0.00021146381 * 500 user0 + 1st round + 2nd round + 3rd round + 4th round + 5th round + 6th round + 7th round + 8th round = 0.105731905 + 0.04540954 + 0.063128165 + 0.103856015 + 0.107317885 + 0.14634257 + 0.201221035 + 0.53658942999 + 0.64390732
    # 9th round 0.00021146381 * 600 user3 + 4th round + 5th round + 6th round + 7th round + 8th round = 0.126878286 + 0.054491448 + 0.075753798 + 0.124627218 + 0.128781462 + 0.175611084
    # 8th round 0.00021146381 * 900 user4 + 5th round + 6th round + 7th round + 8th round = 0.190317429 +  0.081737172 + 0.113630697 + 0.186940827 + 0.193172193
    # 9th round 0.00021146381 * 100 user1 + 6th round + 7th round + 8th round = 0.021146381 + 0.009081908 + 0.012625633 + 0.020771203
    # 9th round 0.00021146381 * 2000 user5 + 7th round + 8th round = 0.42292762 + 0.18163816 + 0.25251266
    # 9th round 0.00021146381 * 1990 user6 + 8th round = 0.4208129819 + 0.1807299692


    # 10th round - user0, user1, user3(unstake), user4, user5, user6, user7


    # 10th round rate 0.00010749704 = (0.64390732/(499.999999999 + 100  + 2000 + 1990 + 900 + 500))
    # 10th round 0.00010749704 * 500 user0 + 1st round + 2nd round + 3rd round + 4th round + 5th round + 6th round + 7th round + 8th round + 9th round = 0.05374852 + 0.105731905 + 0.04540954 + 0.063128165 + 0.103856015 + 0.107317885 + 0.14634257 + 0.201221035 + 0.53658942999 + 0.64390732
    # 10th round 0.00010749704 * 900 user4 + 5th round + 6th round + 7th round + 8th round + 9th round = 0.096747336 + 0.190317429 +  0.081737172 + 0.113630697 + 0.186940827 + 0.193172193
    # 10th round 0.00010749704 * 100 user1 + 6th round + 7th round + 8th round + 9th round = 0.010749704 + 0.021146381 + 0.009081908 + 0.012625633 + 0.020771203
    # 10th round 0.00010749704 * 2000 user5 + 7th round + 8th round + 9th round = 0.21499408 + 0.42292762 + 0.18163816 + 0.25251266
    # 10th round 0.00010749704 * 1990 user6 + 8th round + 9th round = 0.2139191096 + 0.4208129819 + 0.1807299692
    # 10th round 0.00010749704 * 500 user7 = 0.05374852

    # 11th round - user0, user1, user2(restake), user3(restake), user4, user5, user6, user7, user8, user9 - 4xSWAPS

    # 11th round rate 0.00025756292 = (0.64390732*4/(499.999999999 + 100 + 1000 + 600 + 900 + 2000 + 1990 + 500 + 910 + 1500))
    # 11th round 0.00025756292 * 500 user0 + 1st round + 2nd round + 3rd round + 4th round + 5th round + 6th round + 7th round + 8th round + 9th round = 0.12878146 + 0.05374852 + 0.105731905 + 0.04540954 + 0.063128165 + 0.103856015 + 0.107317885 + 0.14634257 + 0.201221035 + 0.53658942999 + 0.64390732
    # 11th round 0.00025756292 * 900 user4 + 5th round + 6th round + 7th round + 8th round + 9th round = 0.231806628 + 0.096747336 + 0.190317429 +  0.081737172 + 0.113630697 + 0.186940827 + 0.193172193
    # 11th round 0.00025756292 * 100 user1 + 6th round + 7th round + 8th round + 9th round = 0.025756292 + 0.010749704 + 0.021146381 + 0.009081908 + 0.012625633 + 0.020771203
    # 11th round 0.00025756292 * 2000 user5 + 7th round + 8th round + 9th round = 0.51512584 + 0.21499408 + 0.42292762 + 0.18163816 + 0.25251266
    # 11th round 0.00025756292 * 1990 user6 + 8th round + 9th round = 0.5125502108 + 0.2139191096 + 0.4208129819 + 0.1807299692
    # 11th round 0.00025756292 * 1000 user2 = 0.25756292
    # 11th round 0.00025756292 * 600 user3 = 0.154537752

    # 11th round 0.00025164571 * 500 user7 = 0.12878146 + 0.05374852
    # 11th round 0.00025164571 * 910 user8 = 0.2343822572
    # 11th round 0.00025164571 * 1500 user9 = 0.38634438

    #user0 = 0.12878146 + 0.05374852 + 0.105731905 + 0.04540954 + 0.063128165 + 0.103856015 + 0.107317885 + 0.14634257 + 0.201221035 + 0.53658942999 + 0.64390732 = 2.13603384499
    #user1 = 0.029268514 + 0.040244207 + 0.107317886 + 0.025756292 + 0.010749704 + 0.021146381 + 0.009081908 + 0.012625633 + 0.020771203 = 0.276961728
    #user2 = 0.09081908 + 0.12625633 + 0.20771203 + 0.21463577 + 0.29268514 + 0.40244207 + 0.25756292 = 1.59211334
    #user3 = 0.126878286 + 0.054491448 + 0.075753798 + 0.124627218 + 0.128781462 + 0.175611084 + 0.154537752 = 0.840681048
    #user4 = 0.231806628 + 0.096747336 + 0.190317429 +  0.081737172 + 0.113630697 + 0.186940827 + 0.193172193 = 1.094352282
    #user5 = 0.51512584 + 0.21499408 + 0.42292762 + 0.18163816 + 0.25251266 = 1.58719836
    #user6 = 0.5125502108 + 0.2139191096 + 0.4208129819 + 0.1807299692 = 1.3280122715
    #user7 = 0.12878146 + 0.05374852 = 0.18252998
    #user8 = 0.2343822572
    #user9 = 0.38634438
    # total # there may be some precision loss... maybe I'm wrong in first calc bc for cycle is 11 instead 10
    # user0 - 500e18 (2.086)
    # user1 - int(100e18) (0.270)
    # user2 - int(1000e18) (1.59)
    # user3 - 600e18 (0.84)
    # user4 - 900e18 (1.09)
    # user5 - 2000e18 (1.58)
    # user6 - 1990e18 (1.32)
    # user7 - 500e18 (0.18)
    # user8 - int(910e18) (0.234)
    # user9 - 1500e18 (0.386)
    print("users balances",
          token.balanceOf(accounts[0]), token.balanceOf(accounts[1]),
          token.balanceOf(accounts[2]), token.balanceOf(accounts[3]),
          token.balanceOf(accounts[4]), token.balanceOf(accounts[5]),
          token.balanceOf(accounts[6]), token.balanceOf(accounts[7]),
          token.balanceOf(accounts[8]), token.balanceOf(accounts[9])
    )

    assert (token.balanceOf(accounts[0]) - int(int(10000e18))) >= int(2.086e18)
    assert token.balanceOf(accounts[1]) >= int(0.269e18)
    assert token.balanceOf(accounts[2]) >= int(1.54e18)
    assert token.balanceOf(accounts[3]) >= int(0.816e18)
    assert token.balanceOf(accounts[4]) >= int(1.06e18)
    assert token.balanceOf(accounts[5]) >= int(1.54e18)
    assert token.balanceOf(accounts[6]) >= int(1.29e18)
    assert token.balanceOf(accounts[7]) >= int(0.177e18)
    assert token.balanceOf(accounts[8]) >= int(0.227e18)
    assert token.balanceOf(accounts[9]) >= int(0.37e18)
