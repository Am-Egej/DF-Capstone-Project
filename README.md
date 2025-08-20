# 🎾 Data Engineering - Tennis Project

Welcome to the Data Engineering - Tennis project! This repository contains the full pipeline for extracting, transforming, loading, testing, and visualizing professional tennis match data. Whether you're a data engineer, analyst, or tennis enthusiast, this project offers a hands-on look at building a real-world data product from scratch. 

---

## 🎯 Project Goals

- Build a robust ETL pipeline for tennis match data
- Store and query data efficiently using PostgreSQL
- Create interactive visualizations for player insights and comparisons
- Practice production-grade data engineering workflows

---

## 🛠️ Tech Stack

- **Python**
  - `pandas` – Data manipulation and preprocessing  
  - `SQLAlchemy` – ORM for PostgreSQL integration  
  - `psycopg2` / `psycopg2-binary` – PostgreSQL connectivity  
  - `Streamlit` – Interactive web app for visualizing tennis stats  
  - `Altair` & `Plotly` – Declarative and interactive visualizations  
  - `kagglehub` – Seamless access to Kaggle datasets via API  

- **PostgreSQL** – Relational database for storing and querying tennis data  
- **Kaggle API** – Programmatic access to tennis datasets  
- **Git & GitHub** – Version control and collaboration

---

## 📦 Project Overview

This project is organized into four main epics, each representing a key phase in the data pipeline:

1. **Extract** tennis data from Kaggle
2. **Transform** and clean the raw data
3. **Load** the processed data into PostgreSQL
4. **Visualize** player stats using a Streamlit app

---

## 🧩 Epics, User Stories & Tasks

### 🟢 EPIC 1: Extract Tennis Data

#### User Stories
- As a data engineer, I want to programmatically download tennis datasets from Kaggle so I can begin preprocessing.


#### Tasks
- ✅ Set up Kaggle API credentials securely
- ✅ Write a Python script to download the dataset using the Kaggle API
- ✅ Unzip and store the dataset in a local or cloud directory
- ✅ Validate the integrity and completeness of the downloaded files

---

### 🟡 EPIC 2: Transform and Clean Tennis Data

#### User Stories
- As a data engineer, I want to clean and standardize the dataset so it’s ready for analysis and visualization.
- As an analyst, I want consistent player names and match formats to ensure accurate comparisons.
- As a data engineer, I want to extract tour results to analyze tour-specific performance.

#### Tasks
- ✅ Handle missing or null values
- ✅ Normalize player names (e.g., "GAUFF C." → "Coco Gauff")
- ✅ Convert date strings to datetime objects and sort matches chronologically
- ✅ Engineer new features (e.g., set-level scores)
- ✅ Drop irrelevant or redundant columns
- ✅ Merge multiple datasets into a unified schema
- ✅ Write tests to verify transformation accuracy

---

### 🔵 EPIC 3: Load Transformed Data into PostgreSQL

#### User Stories
- As a data engineer, I want to load the cleaned dataset into PostgreSQL so it can be queried efficiently.

#### Tasks
- ✅ Design PostgreSQL schema for tennis data
- ✅ Write ETL functions using `psycopg2` or SQLAlchemy
- ✅ Apply data types and constraints where relevant
- ✅ Validate successful data load with sample queries
- ✅ Document the database schema

---

### 🟣 EPIC 4: Visualize Player Stats via Streamlit

#### User Stories
- As a tennis fan, I want to select a player and view their performance trends over time.
- As a user, I want to compare two players side-by-side across key metrics.
- As a user, I want to explore leaderboards and current standings.
- As a user, I want to filter data by tour type, surface, etc.

#### Tasks
- ✅ Build Streamlit UI components for player selection and comparison
- ✅ Create time-series visualizations (e.g., win/loss trends, ranking progression)
- ✅ Generate leaderboard tables based on selected metrics
- ✅ Implement filters (e.g for tour type, surface, etc)
- ✅ Apply responsive design and styling
- ✅ Add tooltips and hover effects for charts
- ✅ Verify app functionality and performance

---
## 📁 Folder structure - ETL Branch (etl_branch):
<pre>
df-capstone-project/
├── data/
│   ├── raw/                                # Unprocessed files from Kaggle
│   │   └── transformed_tennis_data.csv
│   └── processed/                          # Cleaned CSVs or intermediate outputs
│       ├── atp_tennis.csv           
│       └── wta.csv     
├── notebooks/                              # Data exploration notebook(s)
│   └── capstone_analysis.ipynb 
├── scripts/
│   ├── __init__.py                         
│   ├── config.py                           # DB credentials and constants
│   ├── extract.py                          # Download and unzip Kaggle data                       
│   ├── load.py                             # Load into PostgreSQL
│   └── transform.py                        # Clean and enrich data
├── tests/
│   ├── test_extract.py                     # Tests for successful data extraction                     
│   ├── load.py                             # Tests for successful data loading 
│   └── transform.py                        # Tests for successful data transformation 
├── README.md                               # Project overview
├── requirements.txt                        # Python dependencies
└── run_etl.py                              # End to end run of ETL pipeline
</pre>

---

## 📁 Folder structure - Streamlit Branch (main):
<pre>
df-capstone-project/
├── .streamlit/          
│   └── secrets.toml                        # DB credentials and constants for local running of streamlit app
├── data/     
│   ├── updates/    
│   │   ├── postgreSQL_tennis_data.csv      # Table from PostgreSQL - Updated every run               
│   └── postgreSQL_tennis_data.csv          # Local CSV data for users without credentials (not updated)
├── streamlit_scripts/
│   ├── __init__.py                         
│   ├── compare.py                          # Creates Player Comparisons visualisation
│   ├── player.py                           # Creates Player insights visualiisation                  
│   ├── rankings.py                         # Creates Rankings visualisation
│   ├── sql_to_csv.py                       # Extarcts data from PostgreSQL and loads to CSV
│   └── welcome.py                          # Creates welcome visualisation 
├── README.md                               # Project overview
├── requirements.txt                        # Python dependencies
└── tennis_streamlit.py                     # Creates full Streamlit app with all visualisations
</pre>
---

## 🚀 Getting Started

To run the project locally:

```bash
# Clone the repo
git clone https://github.com/Am-Egej/DF-Capstone-Project.git
cd df-capstone-project

# For ETL Pipeline
git switch etl_branch

# For Streamlit app
git switch main

# Install dependencies
pip install -r requirements.txt

# Run the ETL Pipeline
python run_etl.py

# Run the Streamlit app
streamlit run tennis_streamlit.py
```

---

## 🧠 Contributing

Beginner-friendly contributions are welcome! Feel free to open issues, suggest improvements, or submit pull requests. 

---

