import random
from datetime import timedelta

import numpy as np
import pandas as pd


# -----------------------------
# Configuration
# -----------------------------

random.seed(42)
np.random.seed(42)

USERS_FILE = "data/raw/users.csv"
OUTPUT_FILE = "data/raw/sessions.csv"


# -----------------------------
# Load users
# -----------------------------

users = pd.read_csv(USERS_FILE)

users["signup_date"] = pd.to_datetime(users["signup_date"])


# -----------------------------
# Generate sessions
# -----------------------------

sessions = []

session_id = 1

for _, user in users.iterrows():

    signup_date = user["signup_date"]

    profile_completion = user["profile_completion_pct"]

    # Users with better profile completion
    # are more likely to be engaged.
    engagement_score = profile_completion / 100

    # Generate activity for the first 90 days
    # after signup.
    for day in range(90):

        activity_date = signup_date + timedelta(days=day)

        # Probability of using the app.
        probability = 0.10 + (engagement_score * 0.35)

        if random.random() < probability:

            # Some users have multiple sessions.
            number_of_sessions = np.random.poisson(
                1 + (engagement_score * 2)
            )

            for _ in range(number_of_sessions):

                duration = max(
                    1,
                    int(
                        np.random.normal(
                            15 + profile_completion * 0.15,
                            8
                        )
                    )
                )

                sessions.append(
                    {
                        "session_id": f"S{session_id:07d}",
                        "user_id": user["user_id"],
                        "session_date": activity_date.date(),
                        "session_duration_minutes": duration,
                        "device_type": random.choice(
                            ["iOS", "Android", "Web"]
                        ),
                    }
                )

                session_id += 1


# -----------------------------
# Create DataFrame
# -----------------------------

sessions_df = pd.DataFrame(sessions)


# -----------------------------
# Save raw data
# -----------------------------

sessions_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# -----------------------------
# Summary
# -----------------------------

print("Sessions dataset created successfully!")

print(f"Number of sessions: {len(sessions_df)}")

print(f"Saved to: {OUTPUT_FILE}")

print("\nFirst 5 sessions:")
print(sessions_df.head())

print("\nSessions by device:")
print(sessions_df["device_type"].value_counts())

print("\nAverage session duration:")
print(
    round(
        sessions_df["session_duration_minutes"].mean(),
        2
    ),
    "minutes"
)