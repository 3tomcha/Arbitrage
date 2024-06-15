import time
import requests
from web3 import Web3

# UniswapとSushiswapのエンドポイント
UNISWAP_URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
SUSHI_SWAP_URL = "https://api.thegraph.com/subgraphs/name/sushiswap/exchange"

# Web3インスタンスの設定（EthereumのRPC URLを使用）
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/f762421fa9634dffbf00b2a275e15b77'))

# 取引ペアの設定
TOKEN_A = "0x6b175474e89094c44da98b954eedeac495271d0f"  # DAI
TOKEN_B = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"  # USDC

def get_price_from_uniswap():
   query = """
{
 pair(id: "0xa478c2975ab1ea89e8196811f51a7b7ade33eb11"){
     token0 {
       id
       symbol
       name
       derivedETH
     }
     token1 {
       id
       symbol
       name
       derivedETH
     }
     reserve0
     reserve1
     reserveUSD
     trackedReserveETH
     token0Price
     token1Price
     volumeUSD
     txCount
 }
}
"""
   response = requests.post(UNISWAP_URL, json={'query':query})
   data = response.json()
   print(data)
   return float(data['data']['pair']['token0Price']), float(data['data']['pair']['token1Price'])


if __name__ == "__main__":
   get_price_from_uniswap()