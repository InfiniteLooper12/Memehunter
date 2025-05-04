"""
pull_tokenlist_full.py
----------------------
拉取 Birdeye V1 tokenlist（Solana 全链），写入 data/sol_tokenlist_full.csv
Starter / Standard 套餐可用
"""

import os, time, requests, pandas as pd
from datetime import datetime

API_KEY = os.getenv("BIRDEYE_KEY")
if not API_KEY:
    raise RuntimeError("❌ 环境变量 BIRDEYE_KEY 未设置")

HEAD = {
    "X-API-KEY": API_KEY,
    "x-chain":  "solana",
    "accept":   "application/json"
}
URL  = "https://public-api.birdeye.so/defi/tokenlist"

OUT_FILE = f"data/sol_tokenlist_full_{datetime.utcnow().date()}.csv"
os.makedirs("data", exist_ok=True)
first_write = True          # 第一次写 header

offset = 0
total  = 0
backoff = 1.0               # 初始 1 秒回退

while True:
    params = {
        "sort_by":  "v24hUSD",
        "sort_type":"desc",
        "offset":   offset,
        "limit":    50,
        "min_liquidity": 0
    }

    resp = requests.get(URL, headers=HEAD, params=params, timeout=10)
    if resp.status_code == 429:
        # 触发限速：指数回退
        print(f"[429] 速率受限，{backoff:.1f}s 后重试 …")
        time.sleep(backoff)
        backoff = min(backoff * 2, 30)
        continue
    backoff = 1.0                     # 请求成功则重置回退

    js = resp.json()
    items = js.get("data", {}).get("tokens", [])
    print(f"[DEBUG] offset={offset:<5} 取得 {len(items)} 条")
    if not items:                     # 已翻到底部
        break

    pd.DataFrame(items).to_csv(
        OUT_FILE,
        mode="w" if first_write else "a",
        header=first_write,
        index=False
    )
    first_write = False

    total  += len(items)
    offset += 50
    time.sleep(0.3)                   # 主动“防 429”

print(f"✅ 完成，共写入 {total} 行 → {OUT_FILE}")
