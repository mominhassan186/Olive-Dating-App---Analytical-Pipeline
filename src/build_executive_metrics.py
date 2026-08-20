import pandas as pd


# ==========================================
# LOAD CLEANED DATA
# ==========================================

users = pd.read_csv(
    "data/processed/users_clean.csv"
)

sessions = pd.read_csv(
    "data/processed/sessions_clean.csv"
)

matches = pd.read_csv(
    "data/processed/matches_clean.csv"
)

messages = pd.read_csv(
    "data/processed/messages_clean.csv"
)

cohort_retention = pd.read_csv(
    "data/processed/cohort_retention.csv"
)

cohort_churn = pd.read_csv(
    "data/processed/cohort_churn.csv"
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

matches["match_date"] = pd.to_datetime(
    matches["match_date"]
)

messages["message_date"] = pd.to_datetime(
    messages["message_date"]
)


# ==========================================
# MONTHLY NEW USERS
# ==========================================

users["month"] = (
    users["signup_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_users = (
    users.groupby("month")
    .agg(
        new_users=("user_id", "nunique"),
        profile_completion=(
            "profile_completion_pct",
            "mean"
        )
    )
    .reset_index()
)


# ==========================================
# MONTHLY ACTIVE USERS + SESSIONS
# ==========================================

sessions["month"] = (
    sessions["session_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_sessions = (
    sessions.groupby("month")
    .agg(
        active_users=("user_id", "nunique"),
        sessions=("session_id", "nunique")
    )
    .reset_index()
)


# ==========================================
# MONTHLY MATCHES
# ==========================================

matches["month"] = (
    matches["match_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_matches = (
    matches.groupby("month")
    .agg(
        matches=("match_id", "nunique")
    )
    .reset_index()
)


# ==========================================
# MONTHLY MESSAGES
# ==========================================

messages["month"] = (
    messages["message_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_messages = (
    messages.groupby("month")
    .agg(
        messages=("message_id", "nunique")
    )
    .reset_index()
)


# ==========================================
# COMBINE MONTHLY DATA
# ==========================================

executive = monthly_users.merge(
    monthly_sessions,
    on="month",
    how="outer"
)

executive = executive.merge(
    monthly_matches,
    on="month",
    how="outer"
)

executive = executive.merge(
    monthly_messages,
    on="month",
    how="outer"
)


# ==========================================
# ADD RETENTION
# ==========================================

retention = cohort_retention[
    [
        "cohort_month",
        "retention_7_day_pct",
        "retention_30_day_pct"
    ]
].rename(
    columns={
        "cohort_month": "month"
    }
)

executive = executive.merge(
    retention,
    on="month",
    how="left"
)


# ==========================================
# ADD CHURN
# ==========================================

churn = cohort_churn[
    [
        "cohort_month",
        "churn_rate_pct"
    ]
].rename(
    columns={
        "cohort_month": "month"
    }
)

executive = executive.merge(
    churn,
    on="month",
    how="left"
)


# ==========================================
# DERIVED ENGAGEMENT METRICS
# ==========================================

executive["sessions_per_active_user"] = (
    executive["sessions"]
    / executive["active_users"]
)


executive["matches_per_active_user"] = (
    executive["matches"]
    / executive["active_users"]
)


executive["messages_per_active_user"] = (
    executive["messages"]
    / executive["active_users"]
)


# ==========================================
# CLEAN UP
# ==========================================

executive = (
    executive
    .sort_values("month")
    .reset_index(drop=True)
)


# ==========================================
# SAVE MONTHLY KPI DATASET
# ==========================================

executive.to_csv(
    "data/processed/monthly_kpis.csv",
    index=False
)


# ==========================================
# SAVE EXECUTIVE DATASET
# ==========================================

executive.to_csv(
    "data/processed/executive_metrics.csv",
    index=False
)


# ==========================================
# DISPLAY
# ==========================================

print("\n==========================================")
print("EXECUTIVE METRICS CREATED")
print("==========================================")

print(
    executive.to_string(index=False)
)

print("\nCreated files:")

print(
    "✓ data/processed/monthly_kpis.csv"
)

print(
    "✓ data/processed/executive_metrics.csv"
)