# Core

Welcome! [Swap.Dance](https://swap.dance/) is an Ethereum dApp which allows anyone to swap ERC20 tokens and ETH with low slippage. Proof of Trade concept provides a new type of staking mechanism for LP providers.

Swap.Dance smart contracts were deployed on [Vyper v0.3.3](https://github.com/vyperlang/vyper). and are immutable and not upgradeable.

### Testing
In order to test this code, you need to install the [ApeWorX](https://github.com/ApeWorX/ape) packages. 

```
 pip install eth-ape
 ape plugins install vyper
 ape plugins install etherscan
 ape plugins install infura
 ape plugins install alchemy
 ape plugins install hardhat
 ```
 
 ```
 export WEB3_ALCHEMY_PROJECT_ID=YOR_KEY_HERE 
 export WEB3_INFURA_PROJECT_ID=YOR_KEY_HERE 
 ```

To run the entire tests:

```
 ape test
```

### Deployment

To deploy the Proof of Trade AMM:
1. Edit the configuration settings within scripts/deploy.py.
   
   A. Edit the account for production:
   ```
    def load_accs(self):
        acc1 = accounts.load("account01")
        acc1.set_autosign(True)
        return acc1
    ```
   B. Edit the WETH address for the network, Rinkeby, Goerli...
   ```
    WETH = "0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6" # Goerli
    ```
2. Test the deployment locally or within existing testnets.
    ```
    ape run deploy --network ethereum:goerli:infura 
    ```
   
### Docs
[Swap.Dance Docs and API](https://docs.swap.dance/)

### Licensing
The primary license for SwapDance V1 smart contracts is the Business Source License 1.1 (BUSL-1.1), see LICENSE.