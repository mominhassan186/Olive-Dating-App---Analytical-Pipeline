# Olive Dating Data Platform

An end-to-end data engineering and analytics portfolio project for a fictional dating app. It demonstrates how raw application events can be turned into validated datasets, product KPIs, retention and churn analysis, and an interactive management dashboard.

> **All included data is synthetic.** It is generated for demonstration purposes and does not describe a real company or its users.

## What it does

1. Generates sample users, sessions, matches, messages, and profile events.
2. Validates data quality and cleans the raw CSV files.
3. Calculates 7-day and 30-day point-in-time retention, 30-day inactivity churn, and monthly engagement metrics.
4. Compares selected KPIs with example targets and produces findings and recommendations.
5. Presents the results in a Streamlit dashboard.

```text
Synthetic CSVs -> validation and cleaning -> analysis -> KPI/M&E outputs -> Streamlit dashboard
```

Retention means a user had a session **exactly** 7 or 30 days after signup. Churn means no session in the 30 days before the latest recorded session date. The targets and recommendations are illustrative, not business guidance.

## Technology

- Python
- pandas and NumPy for data preparation and analysis
- Faker for synthetic user data
- Streamlit for the interactive dashboard

The project is a local, CSV-based demonstration. It does not use a production database, cloud storage, or a scheduled orchestration service.

## Run it

From the project root, create and activate a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The repository includes processed sample data, so you can view the dashboard right away:

```bash
streamlit run dashboard/app.py
```

Streamlit prints a local URL (usually `http://localhost:8501`) and opens the dashboard in your browser.

## Rebuild the data

Run these commands from the project root to generate fresh synthetic data and rebuild the dashboard metrics:

```bash
python src/generate_data.py
python src/generate_sessions.py
python src/generate_matches.py
python src/generate_messages.py
python src/generate_profile_events.py
python src/validate_data.py
python src/clean_data.py
python src/generate_metrics.py
streamlit run dashboard/app.py
```

`generate_metrics.py` runs the analysis scripts in dependency order: retention, churn, executive metrics, and the M&E evaluation. It stops with an error if its cleaned input files are missing. `validate_data.py` exits with a failure status when any data-quality check fails.

Raw input files are in [`data/raw/`](data/raw/); cleaned data and analysis outputs are in [`data/processed/`](data/processed/). The dashboard has Executive Overview, Engagement Monitoring, Retention & Churn, and Evaluation & Matrix views.
