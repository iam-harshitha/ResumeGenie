# 🧠 ResumeGenie: Discover Jobs. Tailor Resumes. Get Hired

ResumeGenie is an intelligent, end-to-end job application assistant that scrapes fresh job listings from top remote job boards, filters them based on your preferences, and uses LLMs (like LLaMA-3 via Groq) to tailor your resume — all in one seamless Streamlit interface.

Built with LangChain and LangGraph, it offers an automated pipeline from job discovery to resume customization, helping you apply smarter and faster.

---

## 🚀 How It Works

### 📄 Step 1: Upload Your Resume  
Users upload their base resume (in `.txt` format) directly through the UI.

### 🌐 Step 2: Scrape Remote Job Listings  
With one click, ResumeGenie scrapes recent jobs from platforms like:

- ✅ RemoteOK  
- ✅ We Work Remotely  
- ✅ FindWork.dev  

These are saved as CSV files and merged into one unified list.

### 📋 Step 3: Select Relevant Jobs  
All scraped jobs are displayed in a searchable, filterable table with checkboxes. Users can select roles that match their interests.

### 🧠 Step 4: Tailor the Resume (Groq LLaMA-3 + LangChain)  
The selected jobs are passed into a LangChain pipeline, which sends your resume and job details to a Groq-hosted LLaMA-3 model. The LLM rewrites your resume using enhanced, role-specific language and a professional format.

### 💾 Step 5: Download Results  
- 📝 Download your newly tailored resume (in `.txt` format)  
- 📄 Download selected job listings as a `.csv` file  

Both remain accessible on the UI after generation.

---

## 🛠️ Tech Stack & Purpose

| Technology        | Role                                                           |
|-------------------|----------------------------------------------------------------|
| Streamlit         | 🎋 UI for uploading resumes, viewing job listings, and downloads |
| BeautifulSoup     | 🌐 Web scraping for RemoteOK, WWR, and FindWork.dev             |
| Pandas            | 📊 CSV handling, merging job listings                           |
| LangChain         | 🔗 Orchestrates LLM calls and agent logic                      |
| LangGraph         | 🧩 Modular state machine for job-to-resume transformation       |
| Groq API (LLaMA-3)| 🧠 Tailors resumes to selected jobs via structured prompting     |
| Python            | 🐍 Core backend logic                                           |

---

## 🧰 Source Files

| File                  | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `main.py`             | 🚀 Streamlit UI and app pipeline orchestration                              |
| `scrapers/*.py`       | 🌐 Individual job board scrapers (RemoteOK, WWR, FindWork)                  |
| `job_combiner.py`     | 🧮 Merges all scraped jobs into `all_jobs_combined.csv`                     |
| `llms.py`             | 🧠 LangChain + Groq LLaMA-3 resume tailoring pipeline                        |
| `langchain_agent.py`  | 🤖 LangChain agent configuration for job selection and transformation       |
| `graph.py`            | 🧩 LangGraph implementation for stepwise LLM flow                           |
| `requirements.txt`    | 📦 List of Python dependencies                                               |
| `.env`                | 🔐 Stores `GROQ_API_KEY` for secure LLM access                              |

---

## 🖼️ Flow Diagram

LangChain + LangGraph Flow 
(![Screenshot 2025-05-29 202813](https://github.com/user-attachments/assets/93288449-984e-4ba8-a680-c835d9d90f56))

---


## 📸 Screenshots

> (![Screenshot 2025-05-29 143329](https://github.com/user-attachments/assets/6c34fe17-800a-44f6-afb5-06763c6c21af)
> ![Screenshot 2025-05-29 143432](https://github.com/user-attachments/assets/9509c5f5-3cbf-468d-a820-216c0beaeff9)
> ![Screenshot 2025-05-29 143504](https://github.com/user-attachments/assets/8d698a90-cfa7-4ba9-9e42-4d8068334bf5)
)

---

## 🔮 Future Improvements

- ✨ Resume formatting in PDF with layout and design  
- 📬 Auto-send applications via email/API  
- 🔎 Job filtering based on LLM parsing of job descriptions  
- 🧾 Cover letter generation (optional toggle)  
- 📈 Analytics dashboard for job matches and resume performance  

---
