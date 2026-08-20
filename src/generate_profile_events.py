import random

import numpy as np
import pandas as pd


# -----------------------------
# Configuration
# -----------------------------

random.seed(42)
np.random.seed(42)

USERS_FILE = "data/raw/users.csv"
OUTPUT_FILE = "data/raw/profile_events.csv"


# -----------------------------
# Load users
# -----------------------------

users = pd.read_csv(USERS_FILE)

users["signup_date"] = pd.to_datetime(users["signup_date"])


# -----------------------------
# Generate profile events
# -----------------------------

events = []

event_id = 1

profile_fields = [
    "profile_photo",
    "bio",
    "interests",
    "occupation",
    "education",
]


for _, user in users.iterrows():

    signup_date = user["signup_date"]

    completion = user["profile_completion_pct"]

    # Higher completion means more fields
    # are likely to have been completed.
    number_of_fields = max(
        1,
        round(
            len(profile_fields) * completion / 100
        ),
    )

    completed_fields = random.sample(
        profile_fields,
        min(number_of_fields, len(profile_fields)),
    )

    for field in completed_fields:

        event_date = signup_date + pd.Timedelta(
            days=random.randint(0, 14)
        )

        events.append(
            {
                "event_id": f"PE{event_id:07d}",
                "user_id": user["user_id"],
                "event_date": event_date.date(),
                "field_name": field,
                "event_type": "completed",
            }
        )

        event_id += 1


# -----------------------------
# Create DataFrame
# -----------------------------

profile_events_df = pd.DataFrame(events)


# -----------------------------
# Save
# -----------------------------

profile_events_df.to_csv(
    OUTPUT_FILE,
    index=False,
)


# -----------------------------
# Summary
# -----------------------------

print("Profile events dataset created successfully!")

print(
    f"Number of profile events: "
    f"{len(profile_events_df)}"
)

print(f"Saved to: {OUTPUT_FILE}")

print("\nFirst 5 events:")
print(profile_events_df.head())

print("\nEvents by profile field:")
print(
    profile_events_df["field_name"]
    .value_counts()
)