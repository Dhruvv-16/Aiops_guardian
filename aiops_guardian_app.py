import streamlit as st
import openai

# Initialize OpenAI client
client = openai.OpenAI(api_key="sk-...")  # Replace with your actual key

# Simulated logs from ELK, Prometheus, Datadog
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
    Analyze this log and return:
    - Severity: (Critical, Warning, Info)
    - Issue:
    - Suggested Fix:

    Log: {log_text}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful DevOps AI assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def extract_severity(ai_response):
    for line in ai_response.splitlines():
        if "Severity" in line:
            return line.split(":")[1].strip()
    return "Unknown"

def get_color(severity):
    severity = severity.lower()
    if severity == "critical":
        return "#FF4B4B"
    elif severity == "warning":
        return "#FFA500"
    elif severity == "info":
        return "#1E90FF"
    else:
        return "#888888"

# --- Streamlit UI ---
st.set_page_config(page_title="AIOps Guardian", layout="centered")
st.title("🛡️ AIOps Guardian – Log Insight Assistant")

st.markdown("Analyze multiple logs simultaneously and get AI-powered diagnosis with severity tagging.")

log_source = st.selectbox("Choose a Log Source", list(sample_logs.keys()))
selected_logs = st.multiselect("Select Logs to Analyze", sample_logs[log_source])

if st.button("🧠 Run AI Analysis on Selected Logs"):
    if not selected_logs:
        st.warning("Please select at least one log.")
    else:
        st.markdown("### 📊 Analysis Results")
        for idx, log_entry in enumerate(selected_logs, 1):
            with st.spinner(f"Analyzing log {idx}..."):
                analysis = analyze_log(log_entry)
                severity = extract_severity(analysis)
                color = get_color(severity)

                st.markdown(f"""
                <div style="border-left: 6px solid {color}; padding: 1em; margin-bottom: 1em; background-color: #f9f9f9; border-radius: 6px;">
                    <h4 style="margin: 0 0 0.5em 0;">📝 Log Entry {idx}</h4>
                    <p><strong>Raw Log:</strong> {log_entry}</p>
                    <p style="color: {color};"><strong>🚦 Severity:</strong> {severity}</p>
                    <pre style="white-space: pre-wrap; background-color: #fff; padding: 0.5em; border-radius: 4px;">{analysis}</pre>
                </div>
                """, unsafe_allow_html=True)
