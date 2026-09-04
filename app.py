import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Internship Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Code & Internship Task Assistant")
st.write("Log daily tasks, generate clean code snippets, and debug errors instantly using Groq LLM.")

# Secure API Key handling (Streamlit Secrets or Local Env)
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")

if not api_key:
    api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
    if not api_key:
        st.info("Please provide a Groq API key in the sidebar or via Streamlit Secrets to continue.")
        st.stop()

# Initialize Groq Client
client = Groq(api_key=api_key)

# Helper function to query Groq model
def query_groq(prompt):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error connecting to Groq API: {str(e)}"

# Sidebar Navigation
app_mode = st.sidebar.radio(
    "Choose Feature",
    ["Daily Task Log Summarizer", "Code Snippet Generator", "Bug & Error Debugger"]
)

# Feature 1: Daily Task Log Summarizer
if app_mode == "Daily Task Log Summarizer":
    st.subheader("📝 Daily Task Log Summarizer")
    st.write("Convert your rough notes into a polished report for your manager or mentor.")

    rough_notes = st.text_area(
        "Enter your rough notes from today:",
        placeholder="e.g., fixed login button bug, designed database table for users, attended daily standup",
        height=150
    )

    if st.button("Generate Summary", type="primary"):
        if not rough_notes.strip():
            st.warning("Please enter some task notes first.")
        else:
            prompt = f"""
            You are an assistant helping an intern write a professional daily status update.
            Convert these rough task notes into a clean, well-structured daily summary.

            Notes:
            {rough_notes}

            Include:
            1. Key Achievements Today (Bullet points)
            2. Impact/Outcome
            3. Proposed Next Steps
            """
            with st.spinner("Summarizing daily tasks..."):
                summary = query_groq(prompt)
                st.markdown(summary)

# Feature 2: Code Snippet Generator
elif app_mode == "Code Snippet Generator":
    st.subheader("⚡ Code Snippet Generator")
    st.write("Quickly generate clean, commented code snippets for specific tasks.")

    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox("Programming Language", ["Python", "JavaScript", "SQL", "HTML/CSS", "Dart/Flutter", "Java", "C++"])
    with col2:
        task_type = st.selectbox("Snippet Type", ["Function/Utility", "API Endpoint", "Database Query", "Data Processing", "UI Component"])

    task_description = st.text_area(
        "Describe what the code should do:",
        placeholder="e.g., Read a CSV file, drop missing values, and calculate average salary per department.",
        height=120
    )

    if st.button("Generate Code", type="primary"):
        if not task_description.strip():
            st.warning("Please provide a task description.")
        else:
            prompt = f"""
            Write a clean, production-ready {language} snippet for the following task.
            Task Type: {task_type}
            Description: {task_description}

            Requirements:
            - Provide clear inline comments explaining key lines.
            - Follow best practices and standard naming conventions.
            - Keep the code concise and error-free.
            """
            with st.spinner("Generating code snippet..."):
                code_response = query_groq(prompt)
                st.markdown(code_response)

# Feature 3: Bug & Error Debugger
elif app_mode == "Bug & Error Debugger":
    st.subheader("🛠️ Bug & Error Debugger")
    st.write("Paste your broken code or error stack trace to get plain-English explanations and fixes.")

    code_or_error = st.text_area(
        "Paste Code or Stack Trace:",
        placeholder="Paste your error log or faulty code snippet here...",
        height=200
    )

    if st.button("Explain & Debug", type="primary"):
        if not code_or_error.strip():
            st.warning("Please paste your code or error message first.")
        else:
            prompt = f"""
            You are a senior software developer helping an intern debug an issue.
            Analyze the following code or error trace:

            {code_or_error}

            Provide a response with the following sections:
            1. **Root Cause**: Explain why this error happens in simple terms.
            2. **The Fix**: Provide the exact corrected code snippet.
            3. **Prevention Tip**: How to avoid this issue in the future.
            """
            with st.spinner("Analyzing code..."):
                debug_response = query_groq(prompt)
                st.markdown(debug_response)