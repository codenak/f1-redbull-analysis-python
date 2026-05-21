import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import os

df = pd.read_csv("data/cleaned/master_results_cleaned.csv")
os.makedirs("outputs/charts", exist_ok=True)

COLORS = {
    'Red Bull'      : '#3671C6',
    'Ferrari'       : '#E8002D',
    'Mercedes'      : '#27F4D2',
    'McLaren'       : '#FF8000',
    'Aston Martin'  : '#229971',
    'Alpine F1 Team': '#FF87BC',
    'Williams'      : '#64C4FF',
    'RB F1 Team'    : '#6692FF',
    'Haas F1 Team'  : '#B6BABD',
    'Sauber'        : '#52E252',
}

YEAR_COLORS = {2023: '#3671C6', 2024: '#E8002D'}

print("Data loaded successfully")
print(f"Shape: {df.shape}")

winners = df[df['finish_position'] == 1]
wins_by_team = winners.groupby(['year', 'team']).size().reset_index(name='wins')

print("\n" + "="*50)
print("WINS PER TEAM")
print("="*50)
print(wins_by_team.sort_values(['year', 'wins'], ascending=[True, False]).to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Race Wins by Team — 2023 vs 2024', fontsize=16, fontweight='bold')

for i, year in enumerate([2023, 2024]):
    data = wins_by_team[wins_by_team['year'] == year].sort_values('wins', ascending=True)
    colors = [COLORS.get(t, '#888888') for t in data['team']]
    axes[i].barh(data['team'], data['wins'], color=colors)
    axes[i].set_title(f'{year} Season', fontsize=13)
    axes[i].set_xlabel('Number of Wins')
    axes[i].xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    for j, (val, name) in enumerate(zip(data['wins'], data['team'])):
        axes[i].text(val + 0.1, j, str(val), va='center', fontsize=10)

plt.tight_layout()
plt.savefig('outputs/charts/01_wins_by_team.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved: 01_wins_by_team.png")

team_points = df.groupby(['year', 'team'])['points'].sum().reset_index()
team_points = team_points.sort_values(['year', 'points'], ascending=[True, False])

print("\n" + "="*50)
print("TOTAL POINTS PER TEAM")
print("="*50)
print(team_points.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Constructor Points — 2023 vs 2024', fontsize=16, fontweight='bold')

for i, year in enumerate([2023, 2024]):
    data = team_points[team_points['year'] == year].sort_values('points', ascending=True)
    colors = [COLORS.get(t, '#888888') for t in data['team']]
    axes[i].barh(data['team'], data['points'], color=colors)
    axes[i].set_title(f'{year} Season', fontsize=13)
    axes[i].set_xlabel('Total Points')
    for j, val in enumerate(data['points']):
        axes[i].text(val + 2, j, str(int(val)), va='center', fontsize=9)

plt.tight_layout()
plt.savefig('outputs/charts/02_constructor_points.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved: 02_constructor_points.png")

total_races = df.groupby('year')['round'].nunique()
rb_wins     = df[(df['is_redbull']==True) & (df['finish_position']==1)].groupby('year').size()
rb_points   = df[df['is_redbull']==True].groupby('year')['points'].sum()
total_points= df.groupby('year')['points'].sum()

dominance = pd.DataFrame({
    'total_races'     : total_races,
    'rb_wins'         : rb_wins,
    'rb_win_pct'      : (rb_wins / total_races * 100).round(1),
    'rb_points'       : rb_points,
    'total_points'    : total_points,
    'rb_points_share' : (rb_points / total_points * 100).round(1),
}).reset_index()

print("\n" + "="*50)
print("RED BULL DOMINANCE METRICS")
print("="*50)
print(dominance.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Red Bull Dominance — 2023 vs 2024', fontsize=16, fontweight='bold')

axes[0].bar(dominance['year'].astype(str), dominance['rb_win_pct'],
            color=['#3671C6', '#E8002D'], width=0.4)
axes[0].set_title('Win Rate (%)', fontsize=13)
axes[0].set_ylabel('Win %')
axes[0].set_ylim(0, 100)
for i, (val, yr) in enumerate(zip(dominance['rb_win_pct'], dominance['year'])):
    axes[0].text(i, val + 1, f'{val}%', ha='center', fontsize=12, fontweight='bold')

axes[1].bar(dominance['year'].astype(str), dominance['rb_points_share'],
            color=['#3671C6', '#E8002D'], width=0.4)
axes[1].set_title('Points Share (%)', fontsize=13)
axes[1].set_ylabel('Points Share %')
axes[1].set_ylim(0, 100)
for i, val in enumerate(dominance['rb_points_share']):
    axes[1].text(i, val + 1, f'{val}%', ha='center', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('outputs/charts/03_redbull_dominance.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved: 03_redbull_dominance.png")

ver = df[df['driver_code'] == 'VER'].copy()

ver_stats = ver.groupby('year').agg(
    races       = ('round', 'count'),
    wins        = ('finish_position', lambda x: (x == 1).sum()),
    podiums     = ('finish_position', lambda x: (x <= 3).sum()),
    poles       = ('grid_position',   lambda x: (x == 1).sum()),
    total_points= ('points', 'sum'),
    avg_finish  = ('finish_position', 'mean'),
    dnfs        = ('dnf', 'sum'),
).reset_index()

ver_stats['points_per_race'] = (ver_stats['total_points'] / ver_stats['races']).round(1)
ver_stats['win_rate']        = (ver_stats['wins'] / ver_stats['races'] * 100).round(1)
ver_stats['podium_rate']     = (ver_stats['podiums'] / ver_stats['races'] * 100).round(1)

print("\n" + "="*50)
print("VERSTAPPEN STATS")
print("="*50)
print(ver_stats.to_string(index=False))

top_teams = team_points[team_points['year']==2023].nlargest(5, 'points')['team'].tolist()

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Cumulative Constructor Points Race by Race', fontsize=16, fontweight='bold')

for i, year in enumerate([2023, 2024]):
    year_df = df[df['year'] == year]
    
    for team in top_teams:
        team_df = year_df[year_df['team'] == team]
        round_points = team_df.groupby('round')['points'].sum().reset_index()
        round_points = round_points.sort_values('round')
        round_points['cumulative'] = round_points['points'].cumsum()
        
        axes[i].plot(round_points['round'], round_points['cumulative'],
                     marker='o', markersize=3,
                     color=COLORS.get(team, '#888888'),
                     label=team, linewidth=2)
    
    axes[i].set_title(f'{year} Season', fontsize=13)
    axes[i].set_xlabel('Round')
    axes[i].set_ylabel('Cumulative Points')
    axes[i].legend(fontsize=8)
    axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/charts/04_cumulative_points.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved: 04_cumulative_points.png")

dnf_stats = df.groupby(['year', 'team']).agg(
    total_starts = ('round', 'count'),
    total_dnfs   = ('dnf', 'sum')
).reset_index()

dnf_stats['dnf_rate'] = (dnf_stats['total_dnfs'] / dnf_stats['total_starts'] * 100).round(1)

print("\n" + "="*50)
print("DNF RATES BY TEAM")
print("="*50)
print(dnf_stats.sort_values(['year', 'dnf_rate'], ascending=[True, False]).to_string(index=False))

driver_points = df.groupby(['year', 'driver_name', 'team'])['points'].sum().reset_index()
driver_points = driver_points.sort_values(['year', 'points'], ascending=[True, False])

print("\n" + "="*50)
print("DRIVER POINTS — TOP 10 PER SEASON")
print("="*50)
for year in [2023, 2024]:
    print(f"\n{year}:")
    top10 = driver_points[driver_points['year']==year].head(10)
    print(top10[['driver_name', 'team', 'points']].to_string(index=False))

print("\n" + "="*50)
print("EDA COMPLETE — CHARTS SAVED")
print("="*50)
print("outputs/charts/01_wins_by_team.png")
print("outputs/charts/02_constructor_points.png")
print("outputs/charts/03_redbull_dominance.png")
print("outputs/charts/04_cumulative_points.png")