import pandas as pd


# ==========================================
# LOAD CLEAN DATA
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
# DETERMINE ANALYSIS PERIOD
# ==========================================

start_date = users["signup_date"].min()
end_date = users["signup_date"].max()

print("Analysis period:")
print(start_date.date(), "to", end_date.date())


# ==========================================
# CREATE MONTHLY USER METRICS
# ==========================================

users["month"] = (
    users["signup_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_new_users = (
    users.groupby("month")
    .agg(
        new_users=("user_id", "nunique")
    )
    .reset_index()
)


# ==========================================
# MONTHLY ACTIVE USERS
# ==========================================

sessions["month"] = (
    sessions["session_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_active_users = (
    sessions.groupby("month")
    .agg(
        active_users=("user_id", "nunique")
    )
    .reset_index()
)


# ==========================================
# MONTHLY SESSIONS
# ==========================================

monthly_sessions = (
    sessions.groupby("month")
    .agg(
        sessions=("session_id", "count")
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
        matches=("match_id", "count")
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
        messages=("message_id", "count")
    )
    .reset_index()
)


# ==========================================
# MONTHLY PROFILE COMPLETION
# ==========================================

users["profile_month"] = (
    users["signup_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_profile_completion = (
    users.groupby("profile_month")
    .agg(
        profile_completion=(
            "profile_completion_pct",
            "mean"
        )
    )
    .reset_index()
)

monthly_profile_completion = (
    monthly_profile_completion
    .rename(columns={"profile_month": "month"})
)


# ==========================================
# COMBINE ALL MONTHLY METRICS
# ==========================================

monthly_kpis = monthly_new_users.merge(
    monthly_active_users,
    on="month",
    how="outer"
)

monthly_kpis = monthly_kpis.merge(
    monthly_sessions,
    on="month",
    how="outer"
)

monthly_kpis = monthly_kpis.merge(
    monthly_matches,
    on="month",
    how="outer"
)

monthly_kpis = monthly_kpis.merge(
    monthly_messages,
    on="month",
    how="outer"
)

monthly_kpis = monthly_kpis.merge(
    monthly_profile_completion,
    on="month",
    how="outer"
)


# ==========================================
# SORT + FILL MISSING VALUES
# ==========================================

monthly_kpis = (
    monthly_kpis
    .sort_values("month")
    .reset_index(drop=True)
)

numeric_columns = [
    "new_users",
    "active_users",
    "sessions",
    "matches",
    "messages",
]

monthly_kpis[numeric_columns] = (
    monthly_kpis[numeric_columns]
    .fillna(0)
)


# ==========================================
# DERIVED METRICS
# ==========================================

monthly_kpis["sessions_per_active_user"] = (
    monthly_kpis["sessions"]
    / monthly_kpis["active_users"]
    .replace(0, pd.NA)
)


monthly_kpis["matches_per_active_user"] = (
    monthly_kpis["matches"]
    / monthly_kpis["active_users"]
    .replace(0, pd.NA)
)


monthly_kpis["messages_per_active_user"] = (
    monthly_kpis["messages"]
    / monthly_kpis["active_users"]
    .replace(0, pd.NA)
)


# ==========================================
# SAVE
# ==========================================

monthly_kpis.to_csv(
    "data/processed/monthly_kpis.csv",
    index=False
)


# ==========================================
# DISPLAY
# ==========================================

print("\n========================================")
print("MONTHLY KPI DATASET")
print("========================================")

print(monthly_kpis.to_string(index=False))

print("\nSaved to:")
print("data/processed/monthly_kpis.csv")