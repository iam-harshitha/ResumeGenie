import feedparser
from datetime import datetime, timedelta, timezone
import csv

def scrape_wwr_rss():
    feed_url = "https://weworkremotely.com/remote-jobs.rss"
    feed = feedparser.parse(feed_url)

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=48)

    jobs = []
    for entry in feed.entries:
        # Skip if no published date
        if not hasattr(entry, "published_parsed"):
            continue

        # Convert to timezone-aware datetime
        pub_dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        if pub_dt < cutoff:
            continue

        # Parse company/title from entry.title
        # Typical format: "Company Name – Job Title"
        raw = entry.title
        if "–" in raw:
            company, title = map(str.strip, raw.split("–", 1))
        else:
            # fallback
            company, title = "Unknown", raw.strip()

        jobs.append({
            "title": title,
            "company": company,
            "posted_at": pub_dt.strftime("%Y-%m-%d %H:%M"),
            "url": entry.link
        })

    return jobs

def save_to_csv(jobs, filename="scraped_jobs/weworkremotely.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["title", "company", "posted_at", "url"]
        )
        writer.writeheader()
        writer.writerows(jobs)

if __name__ == "__main__":
    jobs = scrape_wwr_rss()
    save_to_csv(jobs)
    print(f"✅ Found and saved {len(jobs)} jobs to weworkremotely.csv")
    