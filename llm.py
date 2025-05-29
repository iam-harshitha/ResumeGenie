# llm.py

from pathlib import Path
import os
from typing import List
import pandas as pd
from groq import Groq
from dotenv import load_dotenv 

# Load your Groq API key from environment variable
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

from groq import Groq
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def tailor_resume(roles: list, resume_text: str, output_path="tailored_resume.txt"):
    roles_str = ', '.join(roles)
    
    prompt = f"""
You are a resume rewriting assistant. Rewrite the following resume with improved, concise, and professional language, tailoring it to these roles: {roles_str}.
Resume:
{resume_text}
"""

    print("🧠 Sending resume to Groq LLM for tailoring...")
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2048

    )
    tailored_text = response.choices[0].message.content.strip()

    Path(output_path).write_text(tailored_text, encoding="utf-8")
    print(f"✅ Tailored resume saved to {output_path}")
    return output_path
