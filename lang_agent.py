# lang_agent.py

from langchain_core.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from pathlib import Path
import pandas as pd

# === 1. LangChain Resume Tailoring Tool ===

@tool
def tailor_resume_with_llm(original_resume_path: str, selected_jobs_path: str, tone: str) -> str:
    """
    Tailor the resume to selected jobs using LLM (Groq).
    """
    resume_text = Path(original_resume_path).read_text(encoding="utf-8")
    jobs_df = pd.read_csv(selected_jobs_path)

    job_descriptions = "\n\n".join(
        f"Role: {row['title']}, Company: {row['company']}, Location: {row['location']}, Description: {row.get('description', '')}"
        for _, row in jobs_df.iterrows()
    )

    prompt = f"""
You are a resume expert. Rewrite the following resume to highlight relevance to these jobs:

TONE: {tone}

RESUME:
{resume_text}

RELEVANT JOB DESCRIPTIONS:
{job_descriptions}
"""

    llm = ChatGroq(temperature=0.4, model_name="mixtral-8x7b-32768")
    response = llm.invoke(prompt)

    # Save the tailored resume
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    tailored_resume_path = output_dir / "tailored_resume.txt"
    tailored_resume_path.write_text(response.content.strip(), encoding="utf-8")

    return str(tailored_resume_path)

# === 2. LangChain Agent (Optional) ===

def get_langchain_agent():
    return initialize_agent(
        tools=[tailor_resume_with_llm],
        llm=ChatGroq(temperature=0.3, model_name="mixtral-8x7b-32768"),
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

# === 3. LangGraph Flow ===

def build_langgraph_flow():
    from langgraph.graph import StateGraph

    def start_node(state):
        print("Starting LangGraph flow...")
        return {"status": "started", **state}

    def tailor_node(state):
        print("Tailoring resume via LangChain tool...")
        result = tailor_resume_with_llm(
            original_resume_path=state["resume_path"],
            selected_jobs_path=state["selected_jobs_csv"],
            tone=state["tone"]
        )
        return {"tailored_resume_path": result, **state}

    def end_node(state):
        print("LangGraph flow complete.")
        return state

    workflow = StateGraph()
    workflow.add_node("start", start_node)
    workflow.add_node("tailor_resume", tailor_node)
    workflow.set_entry_point("start")
    workflow.add_edge("start", "tailor_resume")
    workflow.add_edge("tailor_resume", END)

    return workflow.compile()
