import fastf1
import pandas as pd
import os
import time

fastf1.Cache.enable_cache("cache")

for round_num in [23, 24]:
    print(f"\nRound {round_num}...")
    backup_path = f"data/backups/2024_round{round_num:02d}_results.csv"
    lap_path    = f"data/backups/2024_round{round_num:02d}_laps.csv"

    try:
        session = fastf1.get_session(2024, round_num, 'R')
        session.load()

        results = session.results.copy()
        results['Year']      = 2024
        results['Round']     = round_num
        results['EventName'] = session.event['EventName']
        results['Country']   = session.event['Country']
        results.to_csv(backup_path, index=False)

        laps = session.laps.copy()
        laps['Year']      = 2024
        laps['Round']     = round_num
        laps['EventName'] = session.event['EventName']
        laps.to_csv(lap_path, index=False)

        print(f"   Round {round_num} saved")

    except Exception as e:
        print(f"   Failed: {e}")

    time.sleep(5)

saved = [r for r in range(1, 25)
         if os.path.exists(f"data/backups/2024_round{r:02d}_results.csv")]
missing = [r for r in range(1, 25) if r not in saved]
print(f"\nSaved: {len(saved)}/24 → {saved}")
if missing:
    print(f"Still missing: {missing}")
else:
    print("All 24 rounds collected!")