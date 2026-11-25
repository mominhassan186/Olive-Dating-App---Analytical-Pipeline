import pandas as pd


failures = []


# ==========================================
# LOAD DATA
# ==========================================

users = pd.read_csv("data/raw/users.csv")
sessions = pd.read_csv("data/raw/sessions.csv")
matches = pd.read_csv("data/raw/matches.csv")
messages = pd.read_csv("data/raw/messages.csv")
profile_events = pd.read_csv("data/raw/profile_events.csv")


# Convert dates
users["signup_date"] = pd.to_datetime(users["signup_date"])
sessions["session_date"] = pd.to_datetime(sessions["session_date"])
matches["match_date"] = pd.to_datetime(matches["match_date"])
messages["message_date"] = pd.to_datetime(messages["message_date"])
profile_events["event_date"] = pd.to_datetime(profile_events["event_date"])


# ==========================================
# HELPER FUNCTION
# ==========================================

def check(condition, passed_message, failed_message):

    if condition:
        print(f"✓ PASS: {passed_message}")
    else:
        print(f"✗ FAIL: {failed_message}")
        failures.append(failed_message)


# ==========================================
# 1. PRIMARY KEY CHECKS
# ==========================================

print("\n" + "=" * 50)
print("1. PRIMARY KEY CHECKS")
print("=" * 50)


check(
    users["user_id"].is_unique,
    "User IDs are unique",
    "Duplicate user IDs found",
)

check(
    sessions["session_id"].is_unique,
    "Session IDs are unique",
    "Duplicate session IDs found",
)

check(
    matches["match_id"].is_unique,
    "Match IDs are unique",
    "Duplicate match IDs found",
)

check(
    messages["message_id"].is_unique,
    "Message IDs are unique",
    "Duplicate message IDs found",
)

check(
    profile_events["event_id"].is_unique,
    "Profile event IDs are unique",
    "Duplicate profile event IDs found",
)


# ==========================================
# 2. MISSING VALUE CHECKS
# ==========================================

print("\n" + "=" * 50)
print("2. MISSING VALUE CHECKS")
print("=" * 50)


datasets = {
    "users": users,
    "sessions": sessions,
    "matches": matches,
    "messages": messages,
    "profile_events": profile_events,
}


for name, df in datasets.items():

    missing_values = df.isna().sum().sum()

    check(
        missing_values == 0,
        f"{name}: no missing values",
        f"{name}: {missing_values} missing values found",
    )


# ==========================================
# 3. FOREIGN KEY CHECKS
# ==========================================

print("\n" + "=" * 50)
print("3. FOREIGN KEY / REFERENTIAL INTEGRITY")
print("=" * 50)


user_ids = set(users["user_id"])


# Sessions must belong to real users
invalid_session_users = set(
    sessions["user_id"]
) - user_ids

check(
    len(invalid_session_users) == 0,
    "All session users exist in users table",
    f"{len(invalid_session_users)} invalid session users found",
)


# Matches must belong to real users
match_user_ids = set(
    matches["user_id"]
)

matched_user_ids = set(
    matches["matched_user_id"]
)

invalid_match_users = (
    match_user_ids | matched_user_ids
) - user_ids

check(
    len(invalid_match_users) == 0,
    "All match users exist in users table",
    f"{len(invalid_match_users)} invalid match users found",
)


# Messages must reference real matches
match_ids = set(matches["match_id"])

invalid_message_matches = (
    set(messages["match_id"]) - match_ids
)

check(
    len(invalid_message_matches) == 0,
    "All message matches exist in matches table",
    f"{len(invalid_message_matches)} invalid match IDs found",
)


# Profile events must belong to real users
profile_event_users = set(
    profile_events["user_id"]
)

invalid_profile_users = (
    profile_event_users - user_ids
)

check(
    len(invalid_profile_users) == 0,
    "All profile events belong to real users",
    f"{len(invalid_profile_users)} invalid profile users found",
)


# ==========================================
# 4. RANGE CHECKS
# ==========================================

print("\n" + "=" * 50)
print("4. RANGE CHECKS")
print("=" * 50)


check(
    users["age"].between(18, 80).all(),
    "All ages are between 18 and 80",
    "Invalid ages found",
)


check(
    users["profile_completion_pct"]
    .between(0, 100)
    .all(),
    "Profile completion is between 0 and 100",
    "Invalid profile completion values found",
)


check(
    sessions["session_duration_minutes"]
    .ge(0)
    .all(),
    "Session duration is not negative",
    "Negative session durations found",
)


# ==========================================
# 5. BUSINESS RULE CHECKS
# ==========================================

print("\n" + "=" * 50)
print("5. BUSINESS RULE CHECKS")
print("=" * 50)


# Users cannot match themselves
self_matches = (
    matches["user_id"]
    == matches["matched_user_id"]
).sum()

check(
    self_matches == 0,
    "No self-matches found",
    f"{self_matches} self-matches found",
)


# A session cannot happen before signup
session_users = users[
    ["user_id", "signup_date"]
].merge(
    sessions[
        ["user_id", "session_date"]
    ],
    on="user_id",
    how="inner",
)

invalid_sessions = (
    session_users["session_date"]
    < session_users["signup_date"]
).sum()

check(
    invalid_sessions == 0,
    "No sessions occur before signup",
    f"{invalid_sessions} sessions occur before signup",
)


# A match cannot happen before signup
match_users = users[
    ["user_id", "signup_date"]
].merge(
    matches[
        ["user_id", "match_date"]
    ],
    on="user_id",
    how="inner",
)

invalid_matches = (
    match_users["match_date"]
    < match_users["signup_date"]
).sum()

check(
    invalid_matches == 0,
    "No matches occur before signup",
    f"{invalid_matches} matches occur before signup",
)


# A message should not occur before its match
message_dates = messages[
    ["match_id", "message_date"]
].merge(
    matches[
        ["match_id", "match_date"]
    ],
    on="match_id",
    how="inner",
)

invalid_messages = (
    message_dates["message_date"]
    < message_dates["match_date"]
).sum()

check(
    invalid_messages == 0,
    "No messages occur before matching",
    f"{invalid_messages} messages occur before matching",
)


# ==========================================
# FINAL SUMMARY
# ==========================================

print("\n" + "=" * 50)
print("DATA QUALITY SUMMARY")
print("=" * 50)

print(f"Users:             {len(users):,}")
print(f"Sessions:          {len(sessions):,}")
print(f"Matches:           {len(matches):,}")
print(f"Messages:          {len(messages):,}")
print(f"Profile Events:    {len(profile_events):,}")

print("\nValidation complete.")

if failures:
    raise SystemExit(
        f"Data validation failed: {len(failures)} check(s) did not pass."
    )