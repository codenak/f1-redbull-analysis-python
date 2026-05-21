import fastf1
import pandas as pd
import os
import time
fastf1.Cache.enable_cache("cache")

SEASONS = [2024]
SESSION_TYPES = ['R', 'Q']

def load_session_safe(year, round_num, session_type):
    try:
        session = fastf1.get_session(year, round_num, session_type)
        session.load()
        print(f"   Loaded {year} Round {round_num} ({session_type})")
        return session
    except Exception as e:
        print(f"   Failed {year} Round {round_num} ({session_type}): {e}")
        return None

def extract_race_results(session, year, round_num):
    try:
        results = session.results
        results['Year'] = year
        results['Round'] = round_num
        results['EventName'] = session.event['EventName']
        results['Country'] = session.event['Country']
        return results
    except Exception as e:
        print(f"   Could not extract results: {e}")
        return None

def extract_lap_data(session, year, round_num):
    try:
        laps = session.laps
        laps['Year'] = year
        laps['Round'] = round_num
        laps['EventName'] = session.event['EventName']
        return laps
    except Exception as e:
        print(f"   Could not extract laps: {e}")
        return None

all_race_results = []
all_lap_data = []

for year in SEASONS:
    schedule = fastf1.get_event_schedule(year, include_testing=False)
    total_rounds = len(schedule)
    print(f"\n{'='*50}")
    print(f"Season {year} — {total_rounds} rounds")
    print(f"{'='*50}")

    for round_num in range(1, total_rounds + 1):
        print(f"\nRound {round_num}...")
        backup_path = f"data/backups/{year}_round{round_num:02d}_results.csv"
        lap_path    = f"data/backups/{year}_round{round_num:02d}_laps.csv"
        if os.path.exists(backup_path) and os.path.exists(lap_path):
            print(f"   Already saved, skipping")
            continue
        race_session = load_session_safe(year, round_num, 'R')
        if race_session is not None:
            results = extract_race_results(race_session, year, round_num)
            if results is not None:
                all_race_results.append(results)
                results.to_csv(backup_path, index=False)
                print(f"   Backup saved: {backup_path}")
            laps = extract_lap_data(race_session, year, round_num)
            if laps is not None:
                all_lap_data.append(laps)
                laps.to_csv(lap_path, index=False)
        time.sleep(5)

print("\n\nCombining all data...")

if all_race_results:
    results_2024 = pd.concat(all_race_results, ignore_index=True)
    results_2023 = pd.read_csv("data/raw/master_race_results.csv")
    master_results = pd.concat([results_2023, results_2024], ignore_index=True)
    master_results.to_csv("data/raw/master_race_results.csv", index=False)
    print(f"Master results updated: {len(master_results)} rows")

if all_lap_data:
    laps_2024 = pd.concat(all_lap_data, ignore_index=True)
    laps_2023 = pd.read_csv("data/raw/master_lap_data.csv")
    master_laps = pd.concat([laps_2023, laps_2024], ignore_index=True)
    master_laps.to_csv("data/raw/master_lap_data.csv", index=False)
    print(f"Master laps updated: {len(master_laps)} rows")

print("\nData collection complete!")