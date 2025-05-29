import streamlit as st
from pathlib import Path
import pandas as pd

from job_agent import run_all_scrapers, combine_csv_files
from llm import tailor_resume

# --- Page Config ---
st.set_page_config(page_title="ResumeGenie", layout="wide")
st.markdown("""
    <h2 style='text-align: center; color: #4A4A4A; font-family: "Segoe UI", sans-serif;'>
        🤖 ResumeGenie – Discover Jobs. Tailor Resumes. Get Hired.
    </h2>
""", unsafe_allow_html=True)

# --- Step 1: Upload Resume ---
st.subheader("1. Upload Your Resume")
resume_file = st.file_uploader("Upload your resume (TXT or PDF)", type=["txt", "pdf"])
resume_text = ""

if resume_file is not None:
    file_path = Path(f"uploads/{resume_file.name}")
    file_path.parent.mkdir(exist_ok=True)
    file_path.write_bytes(resume_file.read())

    # Read text
    if file_path.suffix == ".pdf":
        import PyPDF2
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            resume_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    else:
        resume_text = file_path.read_text(encoding="utf-8")

    st.success("✅ Resume uploaded successfully.")

# --- Step 2: Run Scrapers ---
st.subheader("2. Scrape Latest Jobs")
if st.button("🚀 Run Scrapers and Load Jobs"):
    run_all_scrapers()
    combined_csv = combine_csv_files()

    if combined_csv and Path(combined_csv).exists():
        st.success("✅ All scrapers ran successfully!")
        st.session_state["csv_path"] = combined_csv
    else:
        st.error("❌ Failed to combine scraped job CSVs.")

# --- Step 3: Select Jobs from Table ---
if "csv_path" in st.session_state and Path(st.session_state["csv_path"]).exists():
    st.subheader("3. Select Jobs of Interest")
    jobs_df = pd.read_csv(st.session_state["csv_path"])

    jobs_df["select"] = False
    edited_df = st.data_editor(jobs_df, num_rows="dynamic", use_container_width=True)

    selected_jobs = edited_df[edited_df["select"] == True]

    if not selected_jobs.empty:
        selected_roles = selected_jobs["title"].tolist()
        st.success(f"✅ You selected {len(selected_roles)} job(s).")
    else:
        selected_roles = []
        st.info("ℹ️ Select jobs to tailor your resume.")

    # --- Step 4: Tailor Resume ---
    st.subheader("4. Generate Tailored Resume")
    if resume_text and selected_roles:
        if st.button("✂️ Tailor Resume Now"):
            tailored_resume_path = tailor_resume(
                roles=selected_roles,
                resume_text=resume_text
            )
            st.success("🎯 Tailored resume generated!")

            # Show resume
            tailored_text = Path(tailored_resume_path).read_text(encoding="utf-8")
            st.download_button(
                label="📄 Download Tailored Resume",
                data=tailored_text,
                file_name="tailored_resume.txt",
                mime="text/plain"
            )

            # Also allow download of selected jobs
            selected_jobs_csv = "selected_jobs.csv"
            selected_jobs.drop(columns=["select"]).to_csv(selected_jobs_csv, index=False)
            st.download_button(
                label="📂 Download Selected Jobs CSV",
                data=Path(selected_jobs_csv).read_text(encoding="utf-8"),
                file_name="selected_jobs.csv",
                mime="text/csv"
            )
    elif resume_text and not selected_roles:
        st.warning("⚠️ Please select at least one job to tailor your resume.")
    elif not resume_text:
        st.warning("⚠️ Please upload your resume first.")
