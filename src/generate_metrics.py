import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REQUIRED_INPUTS = [
    "users_clean.csv",
    "sessions_clean.csv",
    "matches_clean.csv",
    "messages_clean.csv",
]
ANALYSIS_SCRIPTS = [
    "calculate_retention.py",
    "calculate_churn.py",
    "build_executive_metrics.py",
    "build_me_dashboard.py",
]


def main():
    missing_inputs = [
        filename
        for filename in REQUIRED_INPUTS
        if not (PROCESSED_DIR / filename).exists()
    ]
    if missing_inputs:
        missing_list = ", ".join(missing_inputs)
        raise FileNotFoundError(
            f"Missing processed input files: {missing_list}. "
            "Run `python src/clean_data.py` from the project root first."
        )

    for script_name in ANALYSIS_SCRIPTS:
        script_path = PROJECT_ROOT / "src" / script_name
        subprocess.run(
            [sys.executable, str(script_path)],
            cwd=PROJECT_ROOT,
            check=True,
        )


if __name__ == "__main__":
    main()
