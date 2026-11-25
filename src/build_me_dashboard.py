import pandas as pd


# ==========================================
# LOAD EXECUTIVE DATA
# ==========================================

df = pd.read_csv(
    "data/processed/executive_metrics.csv"
)


# ==========================================
# GET LATEST MONTH
# ==========================================

cohort_metrics = df.dropna(
    subset=[
        "profile_completion",
        "retention_7_day_pct",
        "retention_30_day_pct",
    ]
)

if cohort_metrics.empty:
    raise ValueError("Executive metrics do not contain a complete user cohort.")

latest = cohort_metrics.iloc[-1]


# ==========================================
# TARGETS
# ==========================================

TARGET_7_DAY_RETENTION = 25.0
TARGET_30_DAY_RETENTION = 15.0
TARGET_PROFILE_COMPLETION = 80.0
TARGET_SESSION_FREQUENCY = 5.0


# ==========================================
# ACTUAL VALUES
# ==========================================

actual_7_day = latest["retention_7_day_pct"]

actual_30_day = latest["retention_30_day_pct"]

actual_profile = latest["profile_completion"]

actual_session_frequency = (
    latest["sessions_per_active_user"]
)


# ==========================================
# BUILD M&E TABLE
# ==========================================

me = pd.DataFrame({

    "indicator": [
        "7-Day Retention",
        "30-Day Retention",
        "Profile Completion",
        "Session Frequency",
    ],

    "target": [
        TARGET_7_DAY_RETENTION,
        TARGET_30_DAY_RETENTION,
        TARGET_PROFILE_COMPLETION,
        TARGET_SESSION_FREQUENCY,
    ],

    "actual": [
        actual_7_day,
        actual_30_day,
        actual_profile,
        actual_session_frequency,
    ],
})


# ==========================================
# CALCULATE GAP
# ==========================================

me["gap"] = (
    me["actual"] - me["target"]
)


# ==========================================
# FINDINGS
# ==========================================

def retention_finding(actual, target):

    if actual >= target:
        return "Retention is meeting or exceeding target."

    return "Retention is below target and requires improvement."


def profile_finding(actual, target):

    if actual >= target:
        return "Profile completion is meeting target."

    return "Profile completion is below target."


def engagement_finding(actual, target):

    if actual >= target:
        return "User engagement is meeting target."

    return "Session frequency is below target."


me["finding"] = [

    retention_finding(
        actual_7_day,
        TARGET_7_DAY_RETENTION
    ),

    retention_finding(
        actual_30_day,
        TARGET_30_DAY_RETENTION
    ),

    profile_finding(
        actual_profile,
        TARGET_PROFILE_COMPLETION
    ),

    engagement_finding(
        actual_session_frequency,
        TARGET_SESSION_FREQUENCY
    ),
]


# ==========================================
# RECOMMENDATIONS
# ==========================================

me["recommendation"] = [

    "Improve early-user onboarding and provide stronger reasons to return during the first week.",

    "Introduce stronger re-engagement journeys for users who become inactive.",

    "Simplify profile completion and clearly communicate the benefits of completing a profile.",

    "Increase meaningful in-app interactions through improved match discovery and messaging experiences.",
]


# ==========================================
# INTERVENTIONS
# ==========================================

me["intervention"] = [

    "Redesign onboarding flow and add profile-completion guidance.",

    "Introduce personalized reminders and re-engagement prompts.",

    "Improve profile UI with progress indicators and clearer completion steps.",

    "Improve match recommendations and make messaging easier to initiate.",
]


# ==========================================
# FOLLOW-UP
# ==========================================

me["follow_up"] = [

    "Measure 7-day retention after the onboarding intervention.",

    "Monitor 30-day retention and returning-user rate.",

    "Track profile completion before and after UI changes.",

    "Track sessions per active user and messaging activity.",
]


# ==========================================
# ROUND VALUES
# ==========================================

me["target"] = me["target"].round(2)

me["actual"] = me["actual"].round(2)

me["gap"] = me["gap"].round(2)


# ==========================================
# SAVE
# ==========================================

me.to_csv(
    "data/processed/me_evaluation.csv",
    index=False
)


# ==========================================
# DISPLAY
# ==========================================

print("\n==========================================")
print("M&E EVALUATION")
print("==========================================")

print(
    me.to_string(index=False)
)

print("\nSaved:")
print(
    "data/processed/me_evaluation.csv"
)