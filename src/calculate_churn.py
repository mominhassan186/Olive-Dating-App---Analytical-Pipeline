import pandas as pd


# ==========================================
# LOAD DATA
# ==========================================

users = pd.read_csv(
    "data/processed/users_retention.csv"
)

sessions = pd.read_csv(
    "data/processed/sessions_clean.csv"
)


# ==========================================
# CONVERT DATES
# ==========================================

users["signup_date"] = pd.to_datetime(
    users["signup_date"]
)

sessions["session_date"] = pd.to_datetime(
    sessions["session_date"]
)


# ==========================================
# LAST ACTIVITY PER USER
# ==========================================

last_activity = (
    sessions
    .groupby("user_id")
    .agg(
        last_active_date=("session_date", "max")
    )
    .reset_index()
)


# ==========================================
# JOIN WITH USERS
# ==========================================

users = users.merge(
    last_activity,
    on="user_id",
    how="left"
)


# ==========================================
# ANALYSIS DATE
# ==========================================

analysis_date = sessions["session_date"].max()


# ==========================================
# DAYS SINCE LAST ACTIVITY
# ==========================================

users["days_since_last_activity"] = (
    analysis_date
    - users["last_active_date"]
).dt.days


# ==========================================
# CHURN FLAG
# ==========================================

users["churned"] = (
    users["days_since_last_activity"] >= 30
)


# Users with no recorded activity
# are also considered churned.
users["churned"] = users["churned"].fillna(True)


# ==========================================
# CHURN SUMMARY
# ==========================================

total_users = len(users)

churned_users = users["churned"].sum()

churn_rate = (
    churned_users
    / total_users
    * 100
)


# ==========================================
# CHURN BY COHORT
# ==========================================

users["cohort_month"] = (
    users["signup_date"]
    .dt.to_period("M")
    .astype(str)
)


cohort_churn = (
    users
    .groupby("cohort_month")
    .agg(
        users=("user_id", "nunique"),
        churned_users=("churned", "sum"),
    )
    .reset_index()
)


cohort_churn["churn_rate_pct"] = (
    cohort_churn["churned_users"]
    / cohort_churn["users"]
    * 100
)


# ==========================================
# SAVE USER-LEVEL CHURN DATA
# ==========================================

users.to_csv(
    "data/processed/users_churn.csv",
    index=False
)


# ==========================================
# SAVE COHORT CHURN
# ==========================================

cohort_churn.to_csv(
    "data/processed/cohort_churn.csv",
    index=False
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n========================================")
print("CHURN ANALYSIS")
print("========================================")

print(
    f"Analysis date: "
    f"{analysis_date.date()}"
)

print(
    f"Total users: "
    f"{total_users:,}"
)

print(
    f"Churned users: "
    f"{churned_users:,}"
)

print(
    f"Churn rate: "
    f"{churn_rate:.2f}%"
)

print("\nCohort churn:")

print(
    cohort_churn.to_string(
        index=False
    )
)

print("\nFiles created:")

print(
    "data/processed/users_churn.csv"
)

print(
    "data/processed/cohort_churn.csv"
)