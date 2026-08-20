import random

import numpy as np
import pandas as pd


# -----------------------------
# Configuration
# -----------------------------

random.seed(42)
np.random.seed(42)

USERS_FILE = "data/raw/users.csv"
OUTPUT_FILE = "data/raw/matches.csv"


# -----------------------------
# Load users
# -----------------------------

users = pd.read_csv(USERS_FILE)

users["signup_date"] = pd.to_datetime(users["signup_date"])


# -----------------------------
# Generate matches
# -----------------------------

matches = []

match_id = 1

user_ids = users["user_id"].tolist()


for _, user in users.iterrows():

    profile_completion = user["profile_completion_pct"]

    # Higher profile completion slightly
    # increases probability of getting matches.
    match_probability = (
        0.02 + (profile_completion / 100) * 0.08
    )

    # Number of possible match opportunities.
    opportunities = random.randint(1, 8)

    for _ in range(opportunities):

        if random.random() < match_probability:

            matched_user_id = random.choice(user_ids)

            # Prevent self-matches.
            if matched_user_id == user["user_id"]:
                continue

            # Generate a match date after signup.
            days_after_signup = random.randint(1, 90)

            match_date = (
                user["signup_date"]
                + pd.Timedelta(days=days_after_signup)
            )

            matches.append(
                {
                    "match_id": f"M{match_id:07d}",
                    "user_id": user["user_id"],
                    "matched_user_id": matched_user_id,
                    "match_date": match_date.date(),
                    "match_status": "Matched",
                }
            )

            match_id += 1


# -----------------------------
# Create DataFrame
# -----------------------------

matches_df = pd.DataFrame(matches)


# -----------------------------
# Remove duplicate pairings
# -----------------------------

matches_df = matches_df.drop_duplicates(
    subset=["user_id", "matched_user_id"]
)


# -----------------------------
# Save
# -----------------------------

matches_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# -----------------------------
# Summary
# -----------------------------

print("Matches dataset created successfully!")

print(f"Number of matches: {len(matches_df)}")

print(f"Saved to: {OUTPUT_FILE}")

print("\nFirst 5 matches:")
print(matches_df.head())

print("\nMatches per user:")
print(
    matches_df["user_id"]
    .value_counts()
    .head(10)
)