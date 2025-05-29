import os
import requests
import csv
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Endpoint and headers
API_KEY = os.getenv("FINDWORK_API_KEY")
API_URL = "https://findwork.dev/api/jobs/"
HEADERS = {
    "Authorization": f"Token {API_KEY}"
}

# Get all jobs posted in the last 48 hours
def fetch_recent_jobs():
    print("📡 Fetching jobs from Findwork.dev...")
    response = requests.get(API_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=48)

    recent_jobs = []
    for job in data.get("results", []):
        job_date = datetime.fromisoformat(job["date_posted"].replace("Z", "+00:00"))
        if job_date >= cutoff:
            recent_jobs.append({
                "title": job.get("role", "Unknown"),
                "company": job.get("company_name", "Unknown"),
                "location": job.get("location", "Unknown"),
                "date_posted": job.get("date_posted", ""),
                "url": job.get("url", ""),
                "tags": ", ".join(job.get("tags", [])),
                "description": job.get("text", "")[:200]  # Truncated
            })

    return recent_jobs

# Save jobs to CSV
def save_jobs_to_csv(jobs, filename="scraped_jobs/findwork.csv"):
    keys = ["title", "company", "location", "date_posted", "url", "tags", "description"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(jobs)
    print(f"✅ Found and Saved {len(jobs)} jobs to {filename}")

# Main execution
if __name__ == "__main__":
    try:
        jobs = fetch_recent_jobs()
        save_jobs_to_csv(jobs)
    except Exception as e:
        print(f"❌ Error: {e}")
