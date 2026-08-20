import pandas as pd


# -----------------------------
# File paths
# -----------------------------

RAW_PATH = "data/raw/"
PROCESSED_PATH = "data/processed/"


# -----------------------------
# Load raw data
# -----------------------------

users = pd.read_csv(
    RAW_PATH + "users.csv"
)

sessions = pd.read_csv(
    RAW_PATH + "sessions.csv"
)

matches = pd.read_csv(
    RAW_PATH + "matches.csv"
)

messages = pd.read_csv(
    RAW_PATH + "messages.csv"
)

profile_events = pd.read_csv(
    RAW_PATH + "profile_events.csv"
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

profile_events["event_date"] = pd.to_datetime(
    profile_events["event_date"]
)


# -----------------------------
# Remove duplicates
# -----------------------------

users = users.drop_duplicates(
    subset=["user_id"]
)

sessions = sessions.drop_duplicates(
    subset=["session_id"]
)

matches = matches.drop_duplicates(
    subset=["match_id"]
)

messages = messages.drop_duplicates(
    subset=["message_id"]
)

profile_events = profile_events.drop_duplicates(
    subset=["event_id"]
)


# -----------------------------
# Standardize text columns
# -----------------------------

users["country"] = (
    users["country"]
    .str.strip()
)

users["city"] = (
    users["city"]
    .str.strip()
)

users["gender"] = (
    users["gender"]
    .str.strip()
)

users["acquisition_channel"] = (
    users["acquisition_channel"]
    .str.strip()
)


# -----------------------------
# Validate profile completion
# -----------------------------

users["profile_completion_pct"] = (
    users["profile_completion_pct"]
    .clip(0, 100)
)


# -----------------------------
# Save cleaned datasets
# -----------------------------

users.to_csv(
    PROCESSED_PATH + "users_clean.csv",
    index=False
)

sessions.to_csv(
    PROCESSED_PATH + "sessions_clean.csv",
    index=False
)

matches.to_csv(
    PROCESSED_PATH + "matches_clean.csv",
    index=False
)

messages.to_csv(
    PROCESSED_PATH + "messages_clean.csv",
    index=False
)

profile_events.to_csv(
    PROCESSED_PATH + "profile_events_clean.csv",
    index=False
)


# -----------------------------
# Summary
# -----------------------------

print("================================")
print("DATA CLEANING COMPLETE")
print("================================")

print(f"Users: {len(users):,}")
print(f"Sessions: {len(sessions):,}")
print(f"Matches: {len(matches):,}")
print(f"Messages: {len(messages):,}")
print(f"Profile events: {len(profile_events):,}")

print("\nCleaned files saved to:")
print("data/processed/")