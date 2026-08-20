import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker


# -----------------------------
# Configuration
# -----------------------------

NUM_USERS = 10000
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)

fake = Faker()

random.seed(42)
np.random.seed(42)
Faker.seed(42)


# -----------------------------
# Generate users
# -----------------------------

users = []

locations = {
    "United Arab Emirates": [
        "Dubai",
        "Abu Dhabi",
    ],
    "Saudi Arabia": [
        "Riyadh",
        "Jeddah",
    ],
    "Qatar": [
        "Doha",
    ],
    "Kuwait": [
        "Kuwait City",
    ],
    "Bahrain": [
        "Manama",
    ],
    "Oman": [
        "Muscat",
    ],
    "Jordan": [
        "Amman",
    ],
    "Lebanon": [
        "Beirut",
    ],
    "Egypt": [
        "Cairo",
    ],
    "United States": [
        "New York",
        "Los Angeles",
        "Chicago",
        "Houston",
        "Miami",
        "San Francisco",
        "Dallas",
        "Washington DC",
        "Boston",
    ],
}

genders = ["Male", "Female"]

acquisition_channels = [
    "Organic",
    "Instagram",
    "Facebook",
    "TikTok",
    "Google",
    "Referral",
]


for i in range(1, NUM_USERS + 1):

    signup_date = fake.date_time_between(
        start_date=START_DATE,
        end_date=END_DATE
    )

    age = random.randint(18, 45)

    gender = random.choice(genders)

    country = random.choice(list(locations.keys()))

    city = random.choice(locations[country])

    acquisition_channel = random.choice(acquisition_channels)

    # Some users complete their profiles more than others.
    profile_completion = int(
        np.clip(
            np.random.normal(loc=72, scale=20),
            10,
            100
        )
    )

    users.append(
        {
            "user_id": f"U{i:05d}",
            "signup_date": signup_date.date(),
            "age": age,
            "gender": gender,
            "country": country,
            "city": city,
            "acquisition_channel": acquisition_channel,
            "profile_completion_pct": profile_completion,
            "account_status": "Active",
        }
    )


# -----------------------------
# Convert to DataFrame
# -----------------------------

users_df = pd.DataFrame(users)


# -----------------------------
# Save raw data
# -----------------------------

output_path = "data/raw/users.csv"

users_df.to_csv(output_path, index=False)


# -----------------------------
# Print summary
# -----------------------------

print("Users dataset created successfully!")
print(f"Number of users: {len(users_df)}")
print(f"Saved to: {output_path}")

print("\nFirst 5 users:")
print(users_df.head())

print("\nDataset information:")
print(users_df.info())

print("\nAverage profile completion:")
print(
    round(users_df["profile_completion_pct"].mean(), 2),
    "%"
)