import time
from ape import project
from ape import accounts

class SwapDance(object):

    pair_list = []
    token_list = []

    def load_accs(self):
        acc1 = accounts.load("trader03")
    #    acc1.set_autosign(True)
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

    def init_super_pool(self, token, owner, lock_time):
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
        new_pair = station.initialize(token1, token2, fee1, fee2, market_type, expiry, sender=sender)
        return new_pair

    def add_pre_approved_token(self, token_addr, deployer, sender):
        return deployer.add_approved_tokens(token_addr, sender=sender)


#wETH addr
#Mainnet:0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
#Rinkeby: 0xDf032Bc4B9dC2782Bb09352007D4C57B75160B15
#Ropsten: 0xc778417E063141139Fce010982780140Aa0cD5Ab
#Goerli: 0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6
###
#Settings
###
# pre-approved tokens

WBTC = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"  ### change this address if you are not on mainnet #Rinkeby for example: 0xDf032Bc4B9dC2782Bb09352007D4C57B75160B15
DAI = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
USDT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
# expiry
expiry = int(time.time()) + 3600 # 60min
###
deploy = SwapDance()
main_account = deploy.load_accs()
print("check main addr", main_account)
DANCE_token = deploy.create_token("SwapDance", "DANCE", main_account) ### What is better SWD or DANCE symbol?
station_template = deploy.init_station(DANCE_token, main_account)
stake_template = deploy.init_stake_station(DANCE_token, main_account)
super_pool = deploy.init_super_pool(DANCE_token, main_account, 86400)
deployer = deploy.init_deployer(DANCE_token, super_pool, stake_template, station_template, main_account)
deploy.deployer_register(station_template, super_pool, stake_template, DANCE_token, deployer, main_account) #register all parts
router = deploy.init_router(WETH, main_account) #mainnet by default
# add pre approved tokens
deploy.add_pre_approved_token(WBTC, deployer, main_account)
deploy.add_pre_approved_token(WETH, deployer, main_account)
deploy.add_pre_approved_token(DAI, deployer, main_account)
deploy.add_pre_approved_token(USDT, deployer, main_account)
deploy.add_pre_approved_token(USDC, deployer, main_account)
deploy.create_pair(WETH, str(DANCE_token), station_template, 30, 30, 1, int(expiry), sender=main_account)

