import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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

# ─────────────────────────────────────────
# CHART 5 — VERSTAPPEN vs TOP RIVALS
# Points per race across the season
# Shows when rivals started catching up
# ─────────────────────────────────────────

top_drivers = ['VER', 'NOR', 'LEC', 'HAM', 'PER']
driver_labels = {
    'VER': 'Verstappen',
    'NOR': 'Norris',
    'LEC': 'Leclerc',
    'HAM': 'Hamilton',
    'PER': 'Pérez'
}
driver_colors = {
    'VER': '#3671C6',
    'NOR': '#FF8000',
    'LEC': '#E8002D',
    'HAM': '#27F4D2',
    'PER': '#9B59B6'
}

fig, axes = plt.subplots(1, 2, figsize=(18, 7))
fig.suptitle('Cumulative Driver Points — Verstappen vs Top Rivals',
             fontsize=16, fontweight='bold')

for i, year in enumerate([2023, 2024]):
    year_df = df[df['year'] == year]
    
    for drv in top_drivers:
        drv_df = year_df[year_df['driver_code'] == drv].sort_values('round')
        if len(drv_df) == 0:
            continue
        drv_df['cumulative_pts'] = drv_df['points'].cumsum()
        axes[i].plot(drv_df['round'], drv_df['cumulative_pts'],
                     marker='o', markersize=3, linewidth=2,
                     color=driver_colors[drv],
                     label=driver_labels[drv])
    
    axes[i].set_title(f'{year} Season', fontsize=13)
    axes[i].set_xlabel('Round', fontsize=11)
    axes[i].set_ylabel('Cumulative Points', fontsize=11)
    axes[i].legend(fontsize=9)
    axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/charts/05_driver_points_race_by_race.png', dpi=150, bbox_inches='tight')
print("Chart saved: 05_driver_points_race_by_race.png")

# ─────────────────────────────────────────
# CHART 6 — POINTS GAP TO LEADER
# How far behind was everyone from the leader
# each round — shows when Red Bull's gap closed
# ─────────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(18, 7))
fig.suptitle('Points Gap to Championship Leader by Round',
             fontsize=16, fontweight='bold')

for i, year in enumerate([2023, 2024]):
    year_df = df[df['year'] == year]
    
    # Get cumulative points per driver per round
    pivot = year_df.groupby(['driver_code', 'round'])['points'].sum().unstack(fill_value=0)
    pivot = pivot.cumsum(axis=1)
    
    # Only keep top 5 drivers by end of season
    top5 = pivot[pivot.columns[-1]].nlargest(5).index.tolist()
    pivot = pivot.loc[top5]
    
    # Gap to leader each round
    leader_points = pivot.max(axis=0)
    gap = pivot.subtract(leader_points, axis=1) * -1  # negative = behind leader
    
    driver_name_map = df[['driver_code', 'driver_name']].drop_duplicates()
    name_map = dict(zip(driver_name_map['driver_code'], driver_name_map['driver_name']))
    
    for drv in top5:
        color = driver_colors.get(drv, '#888888')
        label = driver_labels.get(drv, name_map.get(drv, drv))
        axes[i].plot(gap.columns, gap.loc[drv],
                     marker='o', markersize=3, linewidth=2,
                     color=color, label=label)
    
    axes[i].axhline(y=0, color='black', linestyle='--', alpha=0.4, linewidth=1)
    axes[i].set_title(f'{year} Season', fontsize=13)
    axes[i].set_xlabel('Round', fontsize=11)
    axes[i].set_ylabel('Points Behind Leader', fontsize=11)
    axes[i].legend(fontsize=9)
    axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/charts/06_points_gap_to_leader.png', dpi=150, bbox_inches='tight')
print("Chart saved: 06_points_gap_to_leader.png")

# ─────────────────────────────────────────
# CHART 7 — FINISHING POSITION HEATMAP
# Verstappen's finishing positions every race
# Dark = win, light = lower finish
# ─────────────────────────────────────────

fig, axes = plt.subplots(2, 1, figsize=(18, 8))
fig.suptitle('Verstappen Finishing Position — Every Race',
             fontsize=16, fontweight='bold')

for i, year in enumerate([2023, 2024]):
    ver_df = df[(df['driver_code']=='VER') & (df['year']==year)].sort_values('round')
    
    positions = ver_df['finish_position'].values.reshape(1, -1)
    race_labels = [f"R{r}" for r in ver_df['round'].values]
    
    im = axes[i].imshow(positions, cmap='RdYlGn_r', aspect='auto',
                         vmin=1, vmax=20)
    axes[i].set_xticks(range(len(race_labels)))
    axes[i].set_xticklabels(race_labels, fontsize=8)
    axes[i].set_yticks([])
    axes[i].set_title(f'{year} — Green = Win, Red = Lower Finish', fontsize=11)
    
    # Add position numbers inside cells
    for j, pos in enumerate(ver_df['finish_position'].values):
        axes[i].text(j, 0, str(int(pos)), ha='center', va='center',
                    fontsize=9, fontweight='bold',
                    color='white' if pos <= 3 else 'black')

plt.colorbar(im, ax=axes, label='Finishing Position', shrink=0.6)
plt.tight_layout()
plt.savefig('outputs/charts/07_verstappen_positions_heatmap.png', dpi=150, bbox_inches='tight')
print("Chart saved: 07_verstappen_positions_heatmap.png")

# ─────────────────────────────────────────
# CHART 8 — TEAM WIN SHARE PIE CHARTS
# Visual breakdown of who won what
# ─────────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(14, 7))
fig.suptitle('Race Win Distribution — 2023 vs 2024',
             fontsize=16, fontweight='bold')

for i, year in enumerate([2023, 2024]):
    wins = df[(df['year']==year) & (df['finish_position']==1)]
    win_counts = wins['team'].value_counts()
    colors = [COLORS.get(t, '#888888') for t in win_counts.index]
    
    axes[i].pie(win_counts.values,
                labels=win_counts.index,
                colors=colors,
                autopct='%1.1f%%',
                startangle=90,
                pctdistance=0.85)
    axes[i].set_title(f'{year} Season\n({win_counts.sum()} races)', fontsize=13)

plt.tight_layout()
plt.savefig('outputs/charts/08_win_distribution_pie.png', dpi=150, bbox_inches='tight')
print("Chart saved: 08_win_distribution_pie.png")

# ─────────────────────────────────────────
# CHART 9 — GRID vs FINISH POSITION
# How often did starting position
# translate to finishing position?
# ─────────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Grid Position vs Finish Position — Red Bull vs Field',
             fontsize=16, fontweight='bold')

for i, year in enumerate([2023, 2024]):
    year_df = df[df['year']==year].dropna(subset=['grid_position', 'finish_position'])
    
    rb   = year_df[year_df['is_redbull']==True]
    rest = year_df[year_df['is_redbull']==False]
    
    axes[i].scatter(rest['grid_position'], rest['finish_position'],
                    alpha=0.4, color='#888888', s=30, label='Rest of field')
    axes[i].scatter(rb['grid_position'], rb['finish_position'],
                    alpha=0.9, color='#3671C6', s=60, label='Red Bull', zorder=5)
    
    # Diagonal line = no positions gained or lost
    axes[i].plot([1, 20], [1, 20], 'k--', alpha=0.3, linewidth=1)
    
    axes[i].set_title(f'{year} Season', fontsize=13)
    axes[i].set_xlabel('Grid Position', fontsize=11)
    axes[i].set_ylabel('Finish Position', fontsize=11)
    axes[i].legend(fontsize=9)
    axes[i].set_xlim(0, 21)
    axes[i].set_ylim(0, 21)
    axes[i].grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig('outputs/charts/09_grid_vs_finish.png', dpi=150, bbox_inches='tight')
print("Chart saved: 09_grid_vs_finish.png")

# ─────────────────────────────────────────
# CHART 10 — DRIVER CONSISTENCY
# Box plot of finishing positions
# Lower and tighter = more consistent
# ─────────────────────────────────────────

top_drivers_full = ['Max Verstappen', 'Lando Norris', 'Charles Leclerc',
                    'Carlos Sainz', 'Lewis Hamilton', 'George Russell',
                    'Sergio Pérez', 'Oscar Piastri']

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('Driver Finishing Position Consistency — 2023 vs 2024',
             fontsize=16, fontweight='bold')

for i, year in enumerate([2023, 2024]):
    year_df = df[(df['year']==year) & (df['driver_name'].isin(top_drivers_full))]
    
    # Order by median finish position
    order = year_df.groupby('driver_name')['finish_position'].median().sort_values().index
    
    sns.boxplot(data=year_df,
                x='finish_position',
                y='driver_name',
                order=order,
                ax=axes[i],
                palette='viridis',
                width=0.6)
    
    axes[i].set_title(f'{year} Season', fontsize=13)
    axes[i].set_xlabel('Finishing Position', fontsize=11)
    axes[i].set_ylabel('')
    axes[i].grid(True, alpha=0.2, axis='x')
    axes[i].axvline(x=10.5, color='red', linestyle='--',
                    alpha=0.3, linewidth=1, label='Points boundary')

plt.tight_layout()
plt.savefig('outputs/charts/10_driver_consistency.png', dpi=150, bbox_inches='tight')
print("Chart saved: 10_driver_consistency.png")

print("\n" + "="*50)
print("ADVANCED ANALYSIS COMPLETE")
print("="*50)
print("6 charts saved to outputs/charts/")