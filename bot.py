import os
import time
import requests
from web3 import Web3
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からAPIキーを取得
INFURA_API_KEY = os.getenv("INFURA_API_KEY")

# UniswapとSushiswapのエンドポイント
UNISWAP_URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
SUSHI_SWAP_URL = "https://api.thegraph.com/subgraphs/name/sushiswap/exchange"

# Web3インスタンスの設定（EthereumのRPC URLを使用）
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/${INFURA_API_KEY}'))

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

def get_price_from_sushiswap():
   query = """
{
 pair(id: "0xc3d03e4f041fd4cd388c549ee2a29a9e5075882f"){
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
   response = requests.post(SUSHI_SWAP_URL, json={'query':query})
   data = response.json()
   print(data)
   return float(data['data']['pair']['token0Price']), float(data['data']['pair']['token1Price'])

def arbitrage():
   while True:
      uniswap_price_a, uniswap_price_b = get_price_from_uniswap()
      sushiswap_price_a, sushiswap_price_b = get_price_from_sushiswap()

      if uniswap_price_a < sushiswap_price_a:
         print(f"Buy on Uniswap, sell on Sushiswap: {uniswap_price_a} < {sushiswap_price_a}")
            # 取引を実行するコードをここに追加
      elif sushiswap_price_a < uniswap_price_a:
         print(f"Buy on Sushiswap, sell on Uniswap: {sushiswap_price_a} < {uniswap_price_a}")
            # 取引を実行するコードをここに追加
      time.sleep(10)  # 10秒ごとにチェック

if __name__ == "__main__":
  arbitrage()