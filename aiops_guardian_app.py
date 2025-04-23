import streamlit as st
import openai

# Replace with your OpenAI key
client = openai.OpenAI(api_key="sk-...")  # paste your real key here

# Sample log datasets (simulated from ELK, Prometheus, Datadog)
sample_logs = {
    "ELK": [
        "ERROR: Payment service failed to connect to database at 10.0.0.4:5432",
        "WARNING: Auth microservice returned 401 Unauthorized after patch deployment"
    ],
    "Prometheus": [
        "ALERT: High CPU usage detected on node-1, threshold 85%",
        "ALERT: 5xx error rate spike on checkout-service > 30% over 5m window"
    ],
    "Datadog": [
        "Service 'inventory-api' crashed with exit code 137",
        "Timeout connecting to Redis cache in product-service"
    ]
}

def analyze_log(log_text):
    prompt = f"""
    You are AIOps Guardian, an AI assistant for DevOps teams.
    Analyze this log entry and provide:
    1. Root cause of the issue
    2. Suggested action to fix it

    Log: {log_text}

    Respond in this format:
    - Issue:
    - Suggested Fix:
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if supported
        messages=[
            {"role": "system", "content": "You are a helpful DevOps AI assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

# --- Streamlit UI ---
st.set_page_config(page_title="AIOps Guardian", layout="centered")
st.title("🛡️ AIOps Guardian – Real Log Analyzer")

st.markdown("Choose a log source and let the AI diagnose issues from realistic logs.")

log_source = st.selectbox("Select Log Source", list(sample_logs.keys()))
selected_log = st.selectbox("Choose a Sample Log", sample_logs[log_source])

if st.button("🧠 Analyze Selected Log"):
    with st.spinner("Analyzing with AIOps Guardian..."):
        result = analyze_log(selected_log)
    st.success("Analysis Complete")
    st.text_area("💡 AI Response", result, height=180)
