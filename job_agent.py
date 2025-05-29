# job_agent.py

import os
import subprocess
import pandas as pd
from pathlib import Path
import sys

SCRAPER_SCRIPTS = [
    "scrapers/remoteok.py",
    "scrapers/weworkremotely.py",
    "scrapers/findworkdev.py"
]

def run_all_scrapers():
    print("🚀 Running all job scrapers...")

    for script in SCRAPER_SCRIPTS:
        print(f"\n▶️ Running {script}...")
        try:
            subprocess.run([sys.executable, script], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running {script}: {e}")
        except Exception as e:
            print(f"⚠️ Unexpected error with {script}: {e}")

def combine_csv_files(output_path="scraped_jobs/job_combined.csv"):
    csv_files = [
        "scraped_jobs/remoteok.csv",
        "scraped_jobs/weworkremotely.csv",
        "scraped_jobs/findwork.csv"
    ]

    combined_jobs = []

    for csv in csv_files:
        csv_path = Path(csv)
        if csv_path.exists():
            try:
                df = pd.read_csv(csv_path)
                combined_jobs.append(df)
                print(f"✅ Loaded {csv_path} with {len(df)} jobs.")
            except Exception as e:
                print(f"❌ Error reading {csv_path}: {e}")
        else:
            print(f"⚠️ Missing file: {csv_path}")

    if not combined_jobs:
        print("❌ No job data to combine.")
        return None

    combined_df = pd.concat(combined_jobs, ignore_index=True)

    output_path = Path(output_path)
    output_path.parent.mkdir(exist_ok=True)
    combined_df.to_csv(output_path, index=False)
    print(f"✅ Combined CSV saved to: {output_path}")

    return str(output_path)
