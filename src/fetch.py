import requests
import pandas as pd
import os
from config import BIRDEYE_API_KEY, TARGET_TOKEN, CHAIN

def fetch_latest_100_trades():
    os.makedirs("output", exist_ok=True)  # ✅ 自动创建 output 文件夹
    url = f"https://public-api.birdeye.so/defi/v3/token/txs?address={TARGET_TOKEN}&offset=0&limit=100&sort_by=block_unix_time&sort_type=desc&tx_type=swap"
    headers = {
        "accept": "application/json",
        "x-chain": CHAIN,
        "X-API-KEY": BIRDEYE_API_KEY
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"API 请求失败: {response.status_code} - {response.text}")

    data = response.json()["data"]["items"]
    df = pd.DataFrame(data)
    df.to_csv("output/latest_100_trades.csv", index=False)
    print(f"拉取成功，共 {len(df)} 条记录，已保存至 output/latest_100_trades.csv")
    return df

if __name__ == "__main__":
    fetch_latest_100_trades()
