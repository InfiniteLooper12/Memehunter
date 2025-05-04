from fetch_candidates import fetch_candidates
from util_save import update_master_and_today   # ← 新增导入

def main():
    df_today = fetch_candidates()
    print(f"\n[阶段1] 得到 {len(df_today)} 枚候选币")
    if df_today.empty:
        return

    # ↓ 把今日结果写入“今日表”，并累积到 master
    update_master_and_today(df_today)

if __name__ == "__main__":
    main()