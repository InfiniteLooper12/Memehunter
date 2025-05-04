import requests, os
HEAD = {
    "X-API-KEY": os.getenv("BIRDEYE_KEY"),
    "x-chain":  "solana",
    "accept":   "application/json"
}

addr = "JCeoBX79HfatfaY6xvuNyCHf86hwgkCCWDpEycVHtime"   # toly
url  = f"https://public-api.birdeye.so/defi/token/detail?address={addr}"

print(requests.get(url, headers=HEAD, timeout=10).json())
