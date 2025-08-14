# DF-Capstone-Project
## Folder structure:
df-capstone-project/
├── data/
│   ├── raw/               # Unprocessed files from Kaggle
│   └── processed/         # Cleaned CSVs or intermediate outputs
├── scripts/
│   ├── extract.py         # Download and unzip Kaggle data
│   ├── transform.py       # Clean and enrich data
│   ├── load.py            # Load into PostgreSQL
│   └── config.py          # DB credentials and constants
├── notebooks/             # For exploration and debugging
├── requirements.txt       # Python dependencies
└── README.md              # Project overview


## EPICS, User stories and tasks
### EPIC 1: Extract Tennis Data
#### User Stories
- As a developer, I want to download the ATP tennis dataset from Kaggle so I can begin processing it.
- As a developer, I want to automate the data extraction process so I can keep the dataset up to date.

#### Tasks
- Write a script to download the dataset from Kaggle.
- Unzip and store the dataset in a local or cloud directory.
EBI Task:
- Schedule periodic pulls (e.g., daily or weekly) using a cron job or similar.

### EPIC 2: Transform Tennis Data
#### User Stories
- As a developer, I want to clean and normalize the data so it’s ready for analysis.
- As a user, I want to see consistent player names and match formats so comparisons are accurate.
- As a developer, I want to extract Grand Slam results so I can count wins per tournament.

#### Tasks
- Handle missing values and inconsistent formats.
- Normalize player names (e.g., "R. Nadal" vs "Rafael Nadal").
- Convert dates to datetime format and sort chronologically.
- Create derived columns (e.g., win/loss, tournament type).
- Filter and tag Grand Slam matches (Wimbledon, US Open, Australian Open, Roland Garros).
- Aggregate stats per player (e.g., total wins, Grand Slam wins, win rate over time).

### EPIC 3: Load Data into App
#### User Stories
- As a developer, I want to load the transformed data into the Streamlit app so users can interact with it.
- As a user, I want the app to load quickly and reliably.

#### Tasks
- Choose a data storage format (e.g., CSV, Parquet, SQLite).
- Write functions to load data into memory efficiently.
- Cache data in Streamlit to improve performance.
- Validate data integrity before loading.

### EPIC 4: Visualise Player Stats
#### User Stories
- As a user, I want to select a player and view their performance over time.
- As a user, I want to compare two players side-by-side.
- As a user, I want to see leaderboards and current standings.
- As a user, I want to filter by tournament type (e.g., Wimbledon only).

#### Tasks
- Build UI components for player selection and comparison.
- Create time-series plots for player performance.
- Build leaderboard tables (e.g., most Grand Slam wins).
- Add filters for tournament type, year, surface, etc.
- Style the app for clarity and responsiveness.
- Add tooltips and hover info for charts.
















