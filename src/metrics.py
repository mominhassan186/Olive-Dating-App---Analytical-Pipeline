import pandas as pd


# -----------------------------
# Load cleaned data
# -----------------------------

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


# -----------------------------
# Convert dates
# -----------------------------

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


# -----------------------------
# KPI 1 — New Users
# -----------------------------

new_users = len(users)


# -----------------------------
# KPI 2 — Active Users
# -----------------------------

active_users = sessions["user_id"].nunique()


# -----------------------------
# KPI 3 — Sessions
# -----------------------------

total_sessions = len(sessions)


# -----------------------------
# KPI 4 — Matches
# -----------------------------

total_matches = len(matches)


# -----------------------------
# KPI 5 — Messages
# -----------------------------

total_messages = len(messages)


# -----------------------------
# KPI 6 — Profile Completion
# -----------------------------

average_profile_completion = (
    users["profile_completion_pct"].mean()
)


# -----------------------------
# KPI 7 — Session Frequency
# -----------------------------

session_frequency = (
    total_sessions / active_users
)


# -----------------------------
# Print KPIs
# -----------------------------

print("\n================================")
print("OLIVE DATING — KPI SUMMARY")
print("================================")

print(
    f"New Users: "
    f"{new_users:,}"
)

print(
    f"Active Users: "
    f"{active_users:,}"
)

print(
    f"Total Sessions: "
    f"{total_sessions:,}"
)

print(
    f"Total Matches: "
    f"{total_matches:,}"
)

print(
    f"Total Messages: "
    f"{total_messages:,}"
)

print(
    f"Average Profile Completion: "
    f"{average_profile_completion:.1f}%"
)

print(
    f"Session Frequency: "
    f"{session_frequency:.2f}"
)