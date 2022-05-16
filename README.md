# Core

Welcome! [Swap.Dance](https://swap.dance/) is an Ethereum dApp which allows anyone to swap ERC20 tokens and ETH with low slippage. Proof of Trade concept provides a new type of staking mechanism for LP providers.

Swap.Dance smart contracts were deployed on [Vyper 3.3](https://github.com/vyperlang/vyper). and are immutable and not upgradeable.

### Testing
In order to test this code, you need to install the [Brownie](https://github.com/eth-brownie/brownie) package. To run the entire tests:

```buildoutcfg
 brownie test
```

### Deployment

To deploy the Proof of Trade AMM:
1. Install the [ApeWorX](https://github.com/ApeWorX/ape) packages:
   ```buildoutcfg
    pip install eth-ape
    ape plugins install vyper
    ape plugins install etherscan
    ape plugins install infura
    ape plugins install alchemy
    ape plugins install hardhat
    ```
   ```buildoutcfg
    export WEB3_ALCHEMY_PROJECT_ID=YOR_KEY_HERE 
    export WEB3_INFURA_PROJECT_ID=YOR_KEY_HERE 
    ```
2. Edit the configuration settings within scripts/deploy.py.
   
   Edit the account for production:
   ```buildoutcfg
    def load_accs(self):
        acc1 = accounts.load("account01")
        acc1.set_autosign(True)
        return acc1
    ```
   Edit the WETH address for the network, Rinkeby, Goerli...
   ```buildoutcfg
    WETH = "0xDf032Bc4B9dC2782Bb09352007D4C57B75160B15" # Rinkeby
    ```
3. Test the deployment locally or within existing testnets.
    ```buildoutcfg
    ape run deploy --network ethereum:rinkeby:infura 
    ```
   
### Docs
[Swap.Dance Docs and API](https://docs.swap.dance/)

### Licensing
The primary license for SwapDance V1 smart contracts is the Business Source License 1.1 (BUSL-1.1), see LICENSE.