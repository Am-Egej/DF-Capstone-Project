# DF-Capstone-Project
This project extracts, transforms, and loads professional tennis match data (ATP and WTA) using Python scripts and PostgreSQL. 
It is designed to help analyze player performance, tournament trends, and match outcomes.

## 📁 Folder structure:
<pre>
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
</pre>

---

# 🎾 Data Engineering - Tennis Project

Welcome to the Data Engineering - Tennis project! This repository contains the full pipeline for extracting, transforming, loading, testing, and visualizing professional tennis match data. Whether you're a data engineer, analyst, or tennis enthusiast, this project offers a hands-on look at building a real-world data product from scratch. 

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

## 🚀 Getting Started

To run the project locally:

```bash
# Clone the repo
git clone https://github.com/Am-Egej/DF-Capstone-Project.git
cd df-capstone-project

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run tennis_streamlit.py
```

---

## 🧠 Contributing

Beginner-friendly contributions are welcome! Feel free to open issues, suggest improvements, or submit pull requests. 

---

