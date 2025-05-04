import time, requests, pandas as pd
from datetime import datetime, timezone, timedelta
from config import *

URL  = f"{BASE_URL}/defi/v3/token/list"
HEAD = {"X-API-KEY": API_KEY, "x-chain": CHAIN, "accept": "application/json"}

def keep_old_coins(df: pd.DataFrame, min_hours: int) -> pd.DataFrame:
    df = df.copy()
    df["listed_at"] = pd.to_datetime(df["recent_listing_time"],
                                     unit="s", utc=True, errors="coerce")
    cutoff = datetime.now(timezone.utc) - timedelta(hours=min_hours)
    mask = df["listed_at"].isna() | (df["listed_at"] <= cutoff)
    return df[mask]

def fetch_candidates() -> pd.DataFrame:
    rows, offset = [], 0
    for _ in range(MAX_PAGES):
        params = {
            "sort_by":  "volume_24h_usd",
            "sort_type":"desc",
            "offset":   offset,
            "limit":    PAGE_LIMIT,
            "min_liquidity":      MIN_LIQUIDITY,
            "max_market_cap":     MAX_MARKET_CAP,
            "min_volume_24h_usd": MIN_VOLUME_24H_USD
        }
        js = requests.get(URL, params=params, headers=HEAD, timeout=10).json()
        items = js.get("data", {}).get("items", [])
        print(f"[DEBUG] offset={offset}, 本页拉到 {len(items)} 条")
        if not items:
            break
        rows.extend(items)
        offset += PAGE_LIMIT
        time.sleep(0.8)

    if not rows:
        print("[提示] 服务器无返回")
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    df = keep_old_coins(df, LISTING_MIN_HOURS)

    wanted = ["address", "symbol", "market_cap", "volume_24h_usd",
              "liquidity", "holder", "trade_24h_count",
              "recent_listing_time", "listed_at"]
    df = df[[c for c in wanted if c in df.columns]].reset_index(drop=True)
    return df
