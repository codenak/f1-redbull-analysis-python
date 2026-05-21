import pandas as pd
import numpy as np

df = pd.read_csv("data/raw/master_race_results.csv")

print("RAW DATA")
print(f"Shape: {df.shape}")
print(f"\nAll columns:\n{df.columns.tolist()}")
print(f"\nNull counts:\n{df.isnull().sum()}")
print(f"\nData types:\n{df.dtypes}")

cols_to_drop = ['BroadcastName', 'TeamColor', 'HeadshotUrl', 'CountryCode', 'Q1', 'Q2', 'Q3', 'TeamId', 'DriverId']

df = df.drop(columns=cols_to_drop)
print(f"\nAfter dropping useless columns: {df.shape}")

df = df.rename(columns={
    'DriverNumber'      : 'driver_number',
    'Abbreviation'      : 'driver_code',
    'FirstName'         : 'first_name',
    'LastName'          : 'last_name',
    'FullName'          : 'driver_name',
    'TeamName'          : 'team',
    'Position'          : 'finish_position',
    'ClassifiedPosition': 'classified_position',
    'GridPosition'      : 'grid_position',
    'Time'              : 'race_time',
    'Status'            : 'status',
    'Points'            : 'points',
    'Laps'              : 'laps_completed',
    'Year'              : 'year',
    'Round'             : 'round',
    'EventName'         : 'race_name',
    'Country'           : 'country',
})

print(f"\nRenamed columns:\n{df.columns.tolist()}")

df['finish_position'] = pd.to_numeric(df['finish_position'], errors='coerce')
df['grid_position']   = pd.to_numeric(df['grid_position'],   errors='coerce')
df['points']          = pd.to_numeric(df['points'],          errors='coerce').fillna(0)
df['laps_completed']  = pd.to_numeric(df['laps_completed'],  errors='coerce')
df['year']            = df['year'].astype(int)
df['round']           = df['round'].astype(int)
df['driver_number']   = pd.to_numeric(df['driver_number'],   errors='coerce')

print(f"\nData types after fixing:\n{df.dtypes}")

print(f"\nUnique teams before standardising:\n{sorted(df['team'].unique())}")

team_name_map = {'Alfa Romeo': 'Sauber', 'AlphaTauri': 'RB F1 Team'}

df['team'] = df['team'].replace(team_name_map)

df['team_original'] = df['team'].copy()

print(f"\nUnique teams after standardising:\n{sorted(df['team'].unique())}")

df['finished'] = df['classified_position'].apply(lambda x: True if str(x).isdigit() else False)

df['is_redbull'] = df['team'] == 'Red Bull'

df['positions_gained'] = df['grid_position'] - df['finish_position']

df['points_finish'] = df['points'] > 0

DNF_STATUSES = ['Retired', 'Accident', 'Collision damage', 'Undertray', 'Withdrew']
DNS_STATUSES = ['Did not start']

df['dnf'] = df['status'].isin(DNF_STATUSES)
df['dns'] = df['status'].isin(DNS_STATUSES)
df['finished'] = ~df['dnf'] & ~df['dns']

print(f"\nNew columns added: finished, is_redbull, positions_gained, points_finish, dnf")

print(f"\nNull counts after cleaning:\n{df.isnull().sum()}")

print(f"\nFinal shape: {df.shape}")
print(f"\nSample rows:\n{df.head(10).to_string()}")

df.to_csv("data/cleaned/master_results_cleaned.csv", index=False)
print(f"\nCleaned data saved to data/cleaned/master_results_cleaned.csv")

print("\n" + "="*50)
print("SANITY CHECK")
print("="*50)
print(f"Total races  — 2023: {df[df['year']==2023]['round'].nunique()} | 2024: {df[df['year']==2024]['round'].nunique()}")
print(f"Total drivers: {df['driver_name'].nunique()}")
print(f"Total teams  : {df['team'].nunique()}")
print(f"Red Bull rows: {df[df['is_redbull']==True].shape[0]}")