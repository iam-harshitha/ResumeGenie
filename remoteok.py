import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

def scrape_remoteok():
    print("📡 Fetching RemoteOK jobs...")
    url = "https://remoteok.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []

    for tr in soup.find_all('tr', class_='job'):
        try:
            title = tr.find('h2').get_text(strip=True)
            company = tr.find('h3').get_text(strip=True)
            location = tr.find('div', class_='location').get_text(strip=True)
            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "source": "RemoteOK"
            })
        except:
            continue

    if jobs:
        df = pd.DataFrame(jobs)
        Path("scraped_jobs").mkdir(exist_ok=True)
        df.to_csv("scraped_jobs/remoteok.csv", index=False)
        print(f"✅ Found and saved {len(df)} jobs to remoteok.csv")
    else:
        print("⚠️ No jobs found.")

if __name__ == "__main__":
    scrape_remoteok()
