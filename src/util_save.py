# src/util_save.py

import os
import pandas as pd
from config import DATA_DIR, MASTER_FILE, TODAY_FILE

def update_master_and_today(df_today: pd.DataFrame) -> None:
    """
    1. 先把 df_today（去重后）写入 today.csv，其中 appear_count=1
    2. 载入或初始化 master.csv，
       对每个 address：如果在 today 出现，则 master.appear_count += 1；否则保持原值
    3. 再把更新后的 master.appear_count 写回 today.csv（覆盖原文件）
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    # ── 1. 写 today.csv（首版，appear_count=1） ─────────────
    today = df_today.drop_duplicates("address").copy()
    today["appear_count"] = 1
    today.to_csv(TODAY_FILE, index=False)
    print(f"[保存] 初版 Today -> {TODAY_FILE} ({len(today)} 行, appear_count=1)")

    # ── 2. 读 / 初始化 master.csv ────────────────────────
    if os.path.exists(MASTER_FILE):
        master = pd.read_csv(MASTER_FILE, dtype={"address": str})
    else:
        master = pd.DataFrame(columns=["address", "appear_count"])
    if "appear_count" not in master.columns:
        master["appear_count"] = 0

    # 确保 address 列是字符串
    master["address"] = master["address"].astype(str)
    today["address"]  = today["address"].astype(str)

    # 把 today.appear_count (=1) 加到 master
    # 首先，把 master 中不存在的 address 补进来，count=0
    new_addrs = set(today["address"]) - set(master["address"])
    if new_addrs:
        df_new = pd.DataFrame({
            "address": list(new_addrs),
            "appear_count": [0] * len(new_addrs)
        })
        master = pd.concat([master, df_new], ignore_index=True)

    # 然后，对 master 中所有 address，按 today 中是否出现加1
    master = master.set_index("address")
    for addr in today["address"]:
        master.at[addr, "appear_count"] = master.at[addr, "appear_count"] + 1
    master = master.reset_index()

    # ── 3. 把最新 master.appear_count 写回 today.csv ───────
    # 将 master 的 appear_count 映射到 today
    today = today.set_index("address")
    today["appear_count"] = master.set_index("address")["appear_count"]
    today = today.reset_index()

    # 覆盖写 today.csv
    today.to_csv(TODAY_FILE, index=False)
    print(f"[保存] 更新版 Today -> {TODAY_FILE} (含累计 appear_count)")

    # 最后，把 master 写回 master.csv
    master.to_csv(MASTER_FILE, index=False)
    print(f"[保存] Master 共 {len(master)} 行 -> {MASTER_FILE}")
