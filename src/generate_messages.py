import random

import numpy as np
import pandas as pd


# -----------------------------
# Configuration
# -----------------------------

random.seed(42)
np.random.seed(42)

MATCHES_FILE = "data/raw/matches.csv"
OUTPUT_FILE = "data/raw/messages.csv"


# -----------------------------
# Load matches
# -----------------------------

matches = pd.read_csv(MATCHES_FILE)

matches["match_date"] = pd.to_datetime(
    matches["match_date"]
)


# -----------------------------
# Generate messages
# -----------------------------

messages = []

message_id = 1


for _, match in matches.iterrows():

    match_date = match["match_date"]

    # Some matches lead to conversations,
    # while others do not.
    conversation_probability = 0.55

    if random.random() < conversation_probability:

        number_of_messages = random.randint(1, 15)

        for message_number in range(number_of_messages):

            message_date = (
                match_date
                + pd.Timedelta(
                    days=random.randint(0, 14)
                )
            )

            # Alternate sender.
            if message_number % 2 == 0:
                sender_id = match["user_id"]
                receiver_id = match["matched_user_id"]
            else:
                sender_id = match["matched_user_id"]
                receiver_id = match["user_id"]

            messages.append(
                {
                    "message_id": f"MSG{message_id:08d}",
                    "match_id": match["match_id"],
                    "sender_id": sender_id,
                    "receiver_id": receiver_id,
                    "message_date": message_date.date(),
                }
            )

            message_id += 1


# -----------------------------
# Create DataFrame
# -----------------------------

messages_df = pd.DataFrame(messages)


# -----------------------------
# Save
# -----------------------------

messages_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# -----------------------------
# Summary
# -----------------------------

print("Messages dataset created successfully!")

print(f"Number of messages: {len(messages_df)}")

print(f"Saved to: {OUTPUT_FILE}")

print("\nFirst 5 messages:")
print(messages_df.head())