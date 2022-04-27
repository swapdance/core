import time
import random
from ape import project
from ape import accounts
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

class SwapDance(object):

    pair_list = []
    token_list = []

    def load_accs(self):
        acc1 = accounts.load("trader03")
        acc1.set_autosign(True)
        return acc1

    def init_router(self, wrapped_token, owner): #Router
        swap_router = owner.deploy(project.SwapRouter, wrapped_token)
        return swap_router

    def init_station(self, token, owner): # Swap Station template
        swap_station = owner.deploy(project.SwapStation, token)
        return swap_station

    def init_stake_station(self, token, owner): # Proof of Trade template
        stake_station = owner.deploy(project.PoTStation, token)
        return stake_station

    def init_super_pool(self, token, lock_time, owner):
        super_pool = owner.deploy(project.SuperPool, token, lock_time)
        return super_pool

    def init_deployer(self, token, super, proof, station, owner):
        deployer = owner.deploy(project.Deployer, token, super, proof, station)
        return deployer

    def deployer_register(self, swap_station, super_pool, stake_station, token, deployer, sender):
        swap_station.update_owner(deployer, sender=sender)
        stake_station.update_owner(deployer, sender=sender)
        super_pool.update_owner(deployer, sender=sender)
        token.new_deployer(deployer, sender=sender)
        deployer.register_deployer(sender=sender)

    def create_token(self, name, symbol, owner):
        token = owner.deploy(project.SWDToken, name, symbol, 350000, 30000000, 1000000000)
        return token

    def create_pair(self, token1, token2, station, fee1, fee2, market_type, expiry, sender):
        new_pair = station.initialize(token1, token2, fee1, fee2, market_type, expiry*2, sender=sender)
        return new_pair

    def create_stake_pool(self, station, pair_addr, expiry, sender):
        station = project.SwapStation.at(station)
        new_stake_pool = station.initialize_pot_station(pair_addr, expiry*2, sender=sender)
        return new_stake_pool

    def add_pre_approved_token(self, token_addr, deployer, sender):
        return deployer.add_approved_tokens(token_addr, sender=sender)

    def add_liquidity(self, amount1, amount_min1, amount2, amount_min2, station, expiry, sender):
        station = project.SwapStation.at(station)
        tx = station.add_liquidity(int(amount1), int(amount_min1), int(amount2), int(amount_min2), expiry*2, sender=sender)
        return tx

    def remove_liquidity(self, station, lp_amount, amount1, amount2, expiry, sender):
        station = project.SwapStation.at(station)
        tx = station.remove_liquidity(int(lp_amount), int(amount1), int(amount2), expiry*2, sender=sender)
        return tx

    def force_reward(self, station, sender):
        station = project.SwapStation.at(station)
        tx = station.force_reward(sender=sender)
        return tx

    def token_approve(self, token, receiver, amount, sender):
        token1 = project.SWDToken.at(token)
        tx = token1.approve(receiver, int(amount), sender=sender)
        return tx

    def get_balance(self, station, sender):
        station = project.SwapStation.at(station)
        return int(station.balanceOf(sender))

    def stake_proof_of_trade(self, pool, amount, expiry, sender):
        pool = project.PoTStation.at(pool)
        tx = pool.stake(int(amount), expiry*2, sender=sender)
        return tx

    def get_reward(self, pool, expiry, sender):
        pool = project.PoTStation.at(pool)
        tx = pool.get_reward(expiry*2, sender=sender)
        return tx

    def unstake_proof_of_trade(self, pool, expiry, sender):
        pool = project.PoTStation.at(pool)
        tx = pool.unstake(expiry*2, sender=sender)
        return tx

    def swap_tokens(self, station, amount_in, amount_min_out, expiry, token, sender):
        station = project.SwapStation.at(station)
        tx = station.swap_tokens(int(amount_in), int(amount_min_out), token, expiry*2, sender=sender)
        return tx


    ### get different info with deployer
    def return_pair_info(self, deployer, pair_id, info_id):
        new_station_info = deployer.get_pair_info(pair_id)
        info = new_station_info[info_id]
        return info

#wETH addr
#Mainnet:0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
#Rinkeby: 0xDf032Bc4B9dC2782Bb09352007D4C57B75160B15
#Ropsten: 0xc778417E063141139Fce010982780140Aa0cD5Ab
#Goerli: 0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6
###
#Settings
###
# how many swaps do, min 3
swap_count = 3
# how many pairs we need, min 10
pairs_count = 10
# how many tokens we need, min 12
tokens_count = 12
# dynamic amount for liquidity
amount1 = 20e18
amount2 = 10000e18
# stable amount for liquidity
amount_stable = 1000e18
# expiry
expiry = int(time.time())
print(expiry)
###
deploy = SwapDance()
main_account = deploy.load_accs()
print("check main addr", main_account)
main_token = deploy.create_token("SwapDance", "DANCE", main_account)
station_template = deploy.init_station(main_token, main_account)
stake_template = deploy.init_stake_station(main_token, main_account)
super_pool = deploy.init_super_pool(main_token, main_account, 180)
deployer = deploy.init_deployer(main_token, super_pool, stake_template, station_template, main_account)
deploy.deployer_register(station_template, super_pool, stake_template, main_token, deployer, main_account) #register all parts
router = deploy.init_router("0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6", main_account) #Goerli by default
# Add token
deploy.token_list.append(main_token)

def main():

    for i in range(tokens_count):
        token = deploy.create_token("SwapDance"+str(i), "DANCE"+str(i), main_account)
        deploy.token_list.append(token)

        if (i % 3) == 0:
            deploy.add_pre_approved_token(token, deployer, main_account) # add pre approved tokens

    print("token list: ", deploy.token_list)

    for i in range(pairs_count):
        fee1 = random.randint(1, 99)
        fee2 = random.randint(1, 99)
        market_type = random.randint(0, 1)
        print("settings pair:", i, fee1, fee2, market_type, deploy.token_list[i], deploy.token_list[i+2])
        new_pair = deploy.create_pair(
            deploy.token_list[i],
            deploy.token_list[i+2],
            station_template,
            fee1,
            fee2,
            market_type,
            expiry,
            main_account
        )
        deploy.pair_list.append(new_pair)

    print("pair list: ", deploy.pair_list)

    ### Add Liquidity
    for i in range(pairs_count):
        pair = deploy.return_pair_info(deployer, i+1, 0)
        # get tokens
        token1 = deploy.return_pair_info(deployer, i+1, 1)
        token2 = deploy.return_pair_info(deployer, i+1, 2)
        # get pair type (stable 0, dynamic 1)
        station_type = deploy.return_pair_info(deployer, i+1, 16)
        if station_type == 0: # stable
            deploy.token_approve(token1, pair, amount_stable, main_account)
            deploy.token_approve(token2, pair, amount_stable, main_account)
            deploy.add_liquidity(amount_stable, amount_stable, amount_stable, amount_stable, pair, expiry, main_account)
        else:
            deploy.token_approve(token1, pair, amount1, main_account)
            deploy.token_approve(token2, pair, amount2, main_account)
            deploy.add_liquidity(amount1, amount1, amount2, amount2, pair, expiry, main_account)

    ### lets init some stake pools
    for i in range(pairs_count):
        pair = deploy.return_pair_info(deployer, i+1, 0)
        # get pair status (approved 1)
        station_status = deploy.return_pair_info(deployer, i+1, 18)
        if station_status == 1:
            deploy.create_stake_pool(str(stake_template), pair, expiry, main_account)
    ###
    ### Swap/Mint DANCE/Check BURN RATE.
    ### NOTE!!! EDIT SuperPool.vy:
    ###TIME: constant(uint256) = 180  # min time lock for LP-Distribution phase
    ###

    ### Deposit LP to Stake Pool
    for i in range(pairs_count):
        # get pair status (approved 1)
        station_status = deploy.return_pair_info(deployer, i+1, 18)
        if station_status == 1:
            pool = deploy.return_pair_info(deployer, i+1, 3)
            deploy.stake_proof_of_trade(pool, 1e18, expiry, main_account)

    for i in range(pairs_count):
        pair = deploy.return_pair_info(deployer, i+1, 0)
        # get tokens
        token1 = deploy.return_pair_info(deployer, i+1, 1)
        token2 = deploy.return_pair_info(deployer, i+1, 2)
        # get pair type (stable 0, dynamic 1)
        station_type = deploy.return_pair_info(deployer, i+1, 16)
        station_status = deploy.return_pair_info(deployer, i + 1, 18)
        if station_type == 0:  # stable
            for k in range(swap_count):
                deploy.token_approve(token1, pair, 100e18, main_account)
                deploy.swap_tokens(pair, 100e18, 98e18, expiry, token1, sender=main_account)
                if station_status == 1:
                    deploy.force_reward(pair, main_account)
            for k in range(1, swap_count):
                deploy.token_approve(token2, pair, amount_stable, main_account)
                deploy.swap_tokens(pair, 100e18, 98e18, expiry, token2, sender=main_account)
                if station_status == 1:
                    deploy.force_reward(pair, main_account)
        else:
            for k in range(1, swap_count):
                deploy.token_approve(token1, pair, 1e18, main_account)
                get_amount_out = router.get_amount_out(pair, token1, int(1e18))
                amount_out = int(get_amount_out)
                deploy.swap_tokens(pair, 1e18, amount_out, expiry, token1, sender=main_account)
                if station_status == 1:
                    deploy.force_reward(pair, main_account)
            for k in range(1, swap_count):
                deploy.token_approve(token2, pair, 500e18, main_account)
                get_amount_out = router.get_amount_out(pair, token2, int(500e18))
                amount_out = int(get_amount_out)
                deploy.swap_tokens(pair, 500e18, amount_out, expiry, token2, sender=main_account)
                if station_status == 1:
                    deploy.force_reward(pair, main_account)

    ### remove 1/10 liquidity to mint super pool fees
    for i in range(pairs_count):
        pair = deploy.return_pair_info(deployer, i+1, 0)
        lp_token_balance = deploy.get_balance(pair, main_account)
        lp_amount = int(lp_token_balance/10)
        call_router = router.calc_remove_liquidity(pair, lp_amount)
        amount_out1 = int(call_router[0])
        amount_out2 = int(call_router[1])
        deploy.remove_liquidity(pair, lp_amount, amount_out1, amount_out2, expiry, main_account)


    ### Withdraw LP from Stake Pool with reward
    for i in range(pairs_count):
        # get pair status (approved 1)
        station_status = deploy.return_pair_info(deployer, i+1, 18)
        if station_status == 1:
            pool = deploy.return_pair_info(deployer, i+1, 3)
            deploy.unstake_proof_of_trade(pool, expiry, main_account)
            print("Check reward")

    ### test super pool
    ### deposit funds first
    ### lock Super Pool
    ### Unlock Funds with 10 LPs
    token_map = []
    for i in range(pairs_count):
        pair = deploy.return_pair_info(deployer, i+1, 0)
        token_map.append(pair)
    print("token_map: ", token_map)
    deploy.token_approve(str(main_token), str(super_pool), 500e18, main_account)
    super_pool.deposit(int(500e18), expiry*2, sender=main_account)
    deployer.lock_super_pool(1, expiry*2, sender=main_account)
    super_pool.get_reward_and_withdraw(token_map, expiry*2, sender=main_account)
    print("Check tx above :)")


    ### BURN RATE

    for i in range(pairs_count):
        pair = deploy.return_pair_info(deployer, i+1, 0)
        # get tokens
        token1 = deploy.return_pair_info(deployer, i+1, 1)
        token2 = deploy.return_pair_info(deployer, i+1, 2)
        # get pair type (stable 0, dynamic 1)
        station_type = deploy.return_pair_info(deployer, i+1, 16)
        station_status = deploy.return_pair_info(deployer, i + 1, 18)
        if station_type == 0:  # stable
            for k in range(swap_count):
                deploy.token_approve(token1, pair, 100e18, main_account)
                deploy.swap_tokens(pair, 100e18, 97e18, expiry, token1, sender=main_account)
                if station_status == 1:
                    deploy.force_reward(pair, main_account)
            for k in range(1, swap_count):
                deploy.token_approve(token2, pair, amount_stable, main_account)
                deploy.swap_tokens(pair, 100e18, 97e18, expiry, token2, sender=main_account)
                if station_status == 1:
                    deploy.force_reward(pair, main_account)
        else:
            for k in range(1, swap_count):
                deploy.token_approve(token1, pair, 1e18, main_account)
                get_amount_out = router.get_amount_out(pair, token1, int(1e18))
                amount_out = int(get_amount_out)
                deploy.swap_tokens(pair, 1e18, amount_out, expiry, token1, sender=main_account)
                if station_status == 1:
                    deploy.force_reward(pair, main_account)
            for k in range(1, swap_count):
                deploy.token_approve(token2, pair, 500e18, main_account)
                get_amount_out = router.get_amount_out(pair, token2, int(500e18))
                amount_out = int(get_amount_out)
                deploy.swap_tokens(pair, 500e18, amount_out, expiry, token2, sender=main_account)
                if station_status == 1:
                    deploy.force_reward(pair, main_account)

    ### Get Reward
    ### Load account 2
    ### Send some LP to acc 2 to stake them to be able to get reward with acc1
    ### or unstake LP to get LP back with reward
