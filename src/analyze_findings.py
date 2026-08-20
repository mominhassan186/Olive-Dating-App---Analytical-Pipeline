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

matches = pd.read_csv(
    "data/processed/matches_clean.csv"
)

messages = pd.read_csv(
    "data/processed/messages_clean.csv"
)


# ==========================================
# PROFILE COMPLETION GROUPS
# ==========================================

users["profile_group"] = pd.cut(
    users["profile_completion_pct"],
    bins=[0, 50, 80, 100],
    labels=[
        "Low (0-50%)",
        "Medium (51-80%)",
        "High (81-100%)",
    ],
    include_lowest=True
)


# ==========================================
# SESSION COUNTS
# ==========================================

user_sessions = (
    sessions
    .groupby("user_id")
    .agg(
        total_sessions=("session_id", "count")
    )
    .reset_index()
)


# ==========================================
# MATCH COUNTS
# ==========================================

# Count matches for BOTH users involved
matches_sent = (
    matches
    .groupby("user_id")
    .size()
    .reset_index(name="matches_sent")
)

matches_received = (
    matches
    .groupby("matched_user_id")
    .size()
    .reset_index()
    .rename(
        columns={
            "matched_user_id": "user_id",
            0: "matches_received"
        }
    )
)


user_matches = matches_sent.merge(
    matches_received,
    on="user_id",
    how="outer"
)

user_matches = user_matches.fillna(0)

user_matches["total_matches"] = (
    user_matches["matches_sent"]
    + user_matches["matches_received"]
)


# ==========================================
# MESSAGE COUNTS
# ==========================================

messages_sent = (
    messages
    .groupby("sender_id")
    .size()
    .reset_index()
    .rename(
        columns={
            "sender_id": "user_id",
            0: "messages_sent"
        }
    )
)

messages_received = (
    messages
    .groupby("receiver_id")
    .size()
    .reset_index()
    .rename(
        columns={
            "receiver_id": "user_id",
            0: "messages_received"
        }
    )
)


user_messages = messages_sent.merge(
    messages_received,
    on="user_id",
    how="outer"
)

user_messages = user_messages.fillna(0)

user_messages["total_messages"] = (
    user_messages["messages_sent"]
    + user_messages["messages_received"]
)


# ==========================================
# COMBINE USER BEHAVIOR
# ==========================================

analysis = users.merge(
    user_sessions,
    on="user_id",
    how="left"
)

analysis = analysis.merge(
    user_matches[
        ["user_id", "total_matches"]
    ],
    on="user_id",
    how="left"
)

analysis = analysis.merge(
    user_messages[
        ["user_id", "total_messages"]
    ],
    on="user_id",
    how="left"
)


# ==========================================
# USERS WITH NO ACTIVITY
# ==========================================

activity_columns = [
    "total_sessions",
    "total_matches",
    "total_messages",
]

analysis[activity_columns] = (
    analysis[activity_columns]
    .fillna(0)
)


# ==========================================
# PROFILE COMPLETION ANALYSIS
# ==========================================

profile_analysis = (
    analysis
    .groupby(
        "profile_group",
        observed=True
    )
    .agg(
        users=("user_id", "count"),

        avg_sessions=(
            "total_sessions",
            "mean"
        ),

        avg_matches=(
            "total_matches",
            "mean"
        ),

        avg_messages=(
            "total_messages",
            "mean"
        ),

        retention_7_day=(
            "returned_day_7",
            "mean"
        ),

        retention_30_day=(
            "returned_day_30",
            "mean"
        ),
    )
    .reset_index()
)


profile_analysis[
    "retention_7_day"
] *= 100

profile_analysis[
    "retention_30_day"
] *= 100


# ==========================================
# ENGAGEMENT GROUPS
# ==========================================

analysis["engagement_group"] = pd.cut(
    analysis["total_sessions"],
    bins=[
        -1,
        1,
        5,
        10,
        float("inf")
    ],
    labels=[
        "Low (0-1 sessions)",
        "Medium (2-5 sessions)",
        "High (6-10 sessions)",
        "Very High (10+ sessions)",
    ],
)


# ==========================================
# ENGAGEMENT ANALYSIS
# ==========================================

engagement_analysis = (
    analysis
    .groupby(
        "engagement_group",
        observed=True
    )
    .agg(
        users=("user_id", "count"),

        avg_profile_completion=(
            "profile_completion_pct",
            "mean"
        ),

        avg_matches=(
            "total_matches",
            "mean"
        ),

        avg_messages=(
            "total_messages",
            "mean"
        ),

        retention_7_day=(
            "returned_day_7",
            "mean"
        ),

        retention_30_day=(
            "returned_day_30",
            "mean"
        ),
    )
    .reset_index()
)


engagement_analysis[
    "retention_7_day"
] *= 100

engagement_analysis[
    "retention_30_day"
] *= 100


# ==========================================
# ROUND RESULTS
# ==========================================

profile_analysis = profile_analysis.round(2)

engagement_analysis = engagement_analysis.round(2)


# ==========================================
# SAVE RESULTS
# ==========================================

profile_analysis.to_csv(
    "data/processed/profile_completion_analysis.csv",
    index=False
)

engagement_analysis.to_csv(
    "data/processed/engagement_analysis.csv",
    index=False
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n==========================================")
print("PROFILE COMPLETION ANALYSIS")
print("==========================================")

print(
    profile_analysis.to_string(
        index=False
    )
)


print("\n==========================================")
print("ENGAGEMENT ANALYSIS")
print("==========================================")

print(
    engagement_analysis.to_string(
        index=False
    )
)


print("\n==========================================")
print("FILES CREATED")
print("==========================================")

print(
    "✓ data/processed/profile_completion_analysis.csv"
)

print(
    "✓ data/processed/engagement_analysis.csv"
)