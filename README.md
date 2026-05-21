# F1 Red Bull Dominance Analysis

A complete end-to-end Python data analytics project analyzing Red Bull Racing's historic 2023 dominance and the rise of multi-team competition in the 2024 Formula 1 season.

## Core Question

> How did Formula 1 transition from Red Bull's historic dominance in 2023 to a balanced multi-team championship fight in 2024?

## Key Findings

| Metric | 2023 | 2024 |
|--------|------|------|
| Red Bull Win Rate | 95.5% (21/22) | 37.5% (9/24) |
| Red Bull Points | 790 | 537 (3rd place) |
| Red Bull Points Share | 35.2% | 22.0% |
| Verstappen Avg Finish | 1.27 | 3.63 |
| Verstappen Points/Race | 24.1 | 16.6 |
| Race-Winning Teams | 2 | 4 |
| McLaren DNF Rate | 9.1% | 0% |

## Analytics Pipeline

**Phase 1 — Data Collection**
- Connected to the official F1 live timing API using FastF1
- Enabled local disk caching to avoid repeat API calls
- Collected race results for all 22 rounds of 2023 and 24 rounds of 2024
- Built resume-safe collection loop with per-race CSV backups
- Handled rate limits using `time.sleep()` delays
- Final dataset: 919 rows across 46 races

**Phase 2 — Data Cleaning**
- Dropped 8 fully null columns
- Renamed all columns to snake_case
- Fixed data types for numeric and integer fields
- Standardised team names across seasons (Alfa Romeo → Sauber, AlphaTauri → RB F1 Team)
- Fixed DNF detection — separated retirements from lapped finishers

**Phase 3 — Feature Engineering**
- `is_redbull` boolean flag
- `positions_gained` = grid minus finish position
- `dnf`, `dns`, `finished` boolean flags from status values
- `points_finish` flag for top 10 finishes
- Derived KPIs: win rate, podium rate, points per race, points share

**Phase 4 — EDA**
- Wins per team by season
- Constructor points comparison
- Red Bull dominance metrics (win % and points share)
- Cumulative constructor points race by race

**Phase 5 — Advanced Analysis**
- Cumulative driver points — Verstappen vs top rivals
- Points gap to championship leader round by round
- Verstappen finishing position heatmap
- Win distribution pie charts
- Grid vs finish position scatter
- Driver consistency boxplot

## Visualizations

| # | Chart | Key Insight |
|---|-------|-------------|
| 1 | Race Wins by Team | 21 Red Bull wins in 2023 vs 9 in 2024 |
| 2 | Constructor Points | Red Bull 790 in 2023, 3rd with 537 in 2024 |
| 3 | Dominance Metrics | Win rate dropped from 95.5% to 37.5% |
| 4 | Cumulative Constructor Points | Red Bull ran away in 2023, tight all season in 2024 |
| 5 | Driver Championship Battle | Rivals stayed close to Verstappen in 2024 |
| 6 | Points Gap to Leader | Gap collapsed from 2023 to 2024 |
| 7 | Verstappen Heatmap | Near-perfect 2023, visible dips in 2024 |
| 8 | Win Distribution Pie | From one-team show to four-team fight |
| 9 | Grid vs Finish Scatter | Red Bull isolated in top-left in 2023, merged with field in 2024 |
| 10 | Driver Consistency Boxplot | Pérez collapse visible — key reason Red Bull lost constructors title |

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10 | Core language |
| FastF1 | F1 API data collection |
| Pandas | Data cleaning and analysis |
| Matplotlib | Primary charting library |
| Seaborn | Statistical visualizations |
| NumPy | Numerical operations |

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/your-username/f1-redbull-analysis.git
cd f1-redbull-analysis
```

**2. Install dependencies**
```bash
pip install fastf1 pandas matplotlib seaborn numpy
```

**3. Run the scripts in order**
```bash
python notebooks/01_data_collection.py
python notebooks/02_data_cleaning.py
python notebooks/03_eda.py
python notebooks/04_advanced_analysis.py
```

> Note: Data collection requires a stable internet connection. The `cache/` folder will be created automatically and speeds up any subsequent runs significantly.

## Data

The cleaned dataset (`master_results_cleaned.csv`) contains 919 rows and 23 columns covering:
- Driver and team information
- Finishing and grid positions
- Points scored
- Race status (Finished, Retired, Lapped, etc.)
- Engineered features (DNF flags, positions gained, points share)

Raw data sourced from the official F1 live timing API via FastF1.

## Portfolio Page

A full interactive portfolio webpage for this project is included in the `web/` folder. Open `web/index.html` in any browser to view it locally.

## Author

**Shounak Mukherjee**
Aspiring Data & Business Analyst — B.Tech CSE, IEM Kolkata

- LinkedIn: [linkedin.com/in/check-out-shounak-mukherjee](https://linkedin.com/in/check-out-shounak-mukherjee)
- Email: mukherjeeshounak05@gmail.com
- GitHub: [github.com/codenak](https://github.com/codenak)
