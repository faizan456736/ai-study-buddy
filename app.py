import streamlit as st
import google.generativeai as genai
import PyPDF2

# Configure Gemini API (from Streamlit Cloud Secrets)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="📚 AI Study Buddy", layout="wide")

st.title("📚 AI Study Buddy")
st.markdown("Learn smarter with Topic Explainer, Summarizer & Quiz Generator 🚀")

# Sidebar menu
menu = st.sidebar.radio("Choose a feature:", ["Topic Explainer", "Note Summarizer", "Quiz Generator"])

# Topic Explainer
if menu == "Topic Explainer":
    topic = st.text_input("Enter a topic:")
    if st.button("Explain"):
        if topic:
            with st.spinner("Explaining..."):
                response = model.generate_content(f"Explain {topic} in simple terms for students.")
                st.success(response.text)
        else:
            st.warning("Please enter a topic.")

# Note Summarizer
elif menu == "Note Summarizer":
    file = st.file_uploader("Upload a PDF or Text file", type=["pdf", "txt"])
    if file:
        text = ""
        if file.type == "application/pdf":
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        else:
            text = file.read().decode("utf-8")

        if st.button("Summarize"):
            with st.spinner("Summarizing..."):
                response = model.generate_content(f"Summarize these notes:\n\n{text}")
                st.success(response.text)

# Quiz Generator
elif menu == "Quiz Generator":
    notes = st.text_area("Paste notes here:")
    if st.button("Generate Quiz"):
        if notes:
            with st.spinner("Generating quiz..."):
                response = model.generate_content(
                    f"Create 5 multiple-choice questions with answers from these notes:\n\n{notes}"
                )
                st.info(response.text)
        else:
            st.warning("Please paste notes first.")