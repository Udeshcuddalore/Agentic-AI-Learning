"""
app.py
------
Streamlit entrypoint for "Hello Agent - CSV FAQ Agent".
This file is intentionally thin: it only wires together the UI and calls
into src/ modules. No prompt text, no pandas/LangChain logic lives here.
"""

import streamlit as st

from config import settings
from src.data_loader import load_csv_files, get_preview, get_dataframes_dict
from src.agent import build_agent, ask_question

st.set_page_config(page_title="Hello Agent - CSV FAQ Agent", page_icon="📄", layout="centered")

st.title("📄 Hello Agent")
st.caption("Upload FAQ / policy CSV files, then ask questions in plain English.")

# ---------------------------------------------------------------------------
# Sidebar: API key (falls back to env var if already set in config)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Setup")
    api_key_input = st.text_input(
        "OpenAI API Key",
        value=settings.OPENAI_API_KEY or "",
        type="password",
        help="Not stored anywhere — used only for this session.",
    )
    st.markdown("---")
    st.markdown(
        "**How to use**\n"
        "1. Upload one or more CSV files\n"
        "2. Type your question\n"
        "3. Get an answer sourced only from your files"
    )

# ---------------------------------------------------------------------------
# Step 1: File upload + preview
# ---------------------------------------------------------------------------
st.subheader("1. Upload CSV files")
uploaded_files = st.file_uploader(
    "Drop one or more CSV files here",
    type=["csv"],
    accept_multiple_files=True,
)

dataframes = {}

if uploaded_files:
    loaded_files = load_csv_files(uploaded_files)

    for lf in loaded_files:
        with st.expander(f"Preview: {lf.name}", expanded=False):
            if lf.error:
                st.error(f"Could not read this file: {lf.error}")
            else:
                st.dataframe(get_preview(lf.dataframe, settings.MAX_PREVIEW_ROWS))

    dataframes = get_dataframes_dict(loaded_files)

    if dataframes:
        st.success(f"{len(dataframes)} file(s) loaded and ready.")

# ---------------------------------------------------------------------------
# Step 2: Question input + answer
# ---------------------------------------------------------------------------
st.subheader("2. Ask a question")
with st.form("question_form"):
    question = st.text_input(
        "e.g. What is the return policy for electronics?",
        placeholder="Type your question here...",
    )
    ask_clicked = st.form_submit_button("Get Answer", type="primary", use_container_width=True)

if ask_clicked:
    if not api_key_input:
        st.warning("Please enter your OpenAI API key in the sidebar first.")
    elif not dataframes:
        st.warning("Please upload at least one valid CSV file first.")
    elif not question.strip():
        st.warning("Please type a question first.")
    else:
        with st.spinner("Reading the uploaded data..."):
            agent = build_agent(dataframes, api_key=api_key_input)
            answer = ask_question(agent, question)

        st.subheader("Answer")
        st.write(answer)