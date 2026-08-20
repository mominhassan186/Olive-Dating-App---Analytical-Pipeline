import pandas as pd


# ==========================================
# LOAD DATA
# ==========================================

users = pd.read_csv(
    "data/processed/users_clean.csv"
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
# CREATE USER ACTIVITY LOOKUP
# ==========================================

# We only need user_id + session_date
# to determine whether someone returned.

activity = sessions[
    ["user_id", "session_date"]
].drop_duplicates()


# ==========================================
# 7-DAY RETENTION
# ==========================================

users["day_7"] = (
    users["signup_date"]
    + pd.Timedelta(days=7)
)

retention_7 = users.merge(
    activity,
    on="user_id",
    how="left"
)

retention_7["returned_day_7"] = (
    retention_7["session_date"]
    == retention_7["day_7"]
)


user_retention_7 = (
    retention_7
    .groupby("user_id")
    ["returned_day_7"]
    .max()
    .reset_index()
)


users = users.merge(
    user_retention_7,
    on="user_id",
    how="left"
)


# ==========================================
# 30-DAY RETENTION
# ==========================================

users["day_30"] = (
    users["signup_date"]
    + pd.Timedelta(days=30)
)

retention_30 = users.merge(
    activity,
    on="user_id",
    how="left"
)

retention_30["returned_day_30"] = (
    retention_30["session_date"]
    == retention_30["day_30"]
)


user_retention_30 = (
    retention_30
    .groupby("user_id")
    ["returned_day_30"]
    .max()
    .reset_index()
)


users = users.drop(
    columns=["returned_day_30"],
    errors="ignore"
)

users = users.merge(
    user_retention_30,
    on="user_id",
    how="left"
)


# ==========================================
# COHORT MONTH
# ==========================================

users["cohort_month"] = (
    users["signup_date"]
    .dt.to_period("M")
    .astype(str)
)


# ==========================================
# COHORT RETENTION
# ==========================================

cohort_retention = (
    users
    .groupby("cohort_month")
    .agg(
        users=("user_id", "nunique"),
        retained_7_day=("returned_day_7", "sum"),
        retained_30_day=("returned_day_30", "sum"),
    )
    .reset_index()
)


# ==========================================
# RETENTION RATES
# ==========================================

cohort_retention["retention_7_day_pct"] = (
    cohort_retention["retained_7_day"]
    / cohort_retention["users"]
    * 100
)


cohort_retention["retention_30_day_pct"] = (
    cohort_retention["retained_30_day"]
    / cohort_retention["users"]
    * 100
)


# ==========================================
# SAVE USER RETENTION DATA
# ==========================================

users.to_csv(
    "data/processed/users_retention.csv",
    index=False
)


# ==========================================
# SAVE COHORT RETENTION
# ==========================================

cohort_retention.to_csv(
    "data/processed/cohort_retention.csv",
    index=False
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n========================================")
print("RETENTION ANALYSIS")
print("========================================")

print(
    cohort_retention.to_string(
        index=False
    )
)

print("\nFiles created:")

print(
    "data/processed/users_retention.csv"
)

print(
    "data/processed/cohort_retention.csv"
)