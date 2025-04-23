import streamlit as st
import openai
import time
import random

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

# Optional known issue matching
known_issues = {
    "failed to connect to database": {
        "fix": "Check database credentials, connectivity, and firewall rules.",
        "component": "Database",
        "severity": "Critical",
        "rollback": "Yes",
        "command": "kubectl rollout undo deployment payment-service"
    },
    "401 unauthorized": {
        "fix": "Validate authentication service config or revert the latest patch.",
        "component": "Auth Service",
        "severity": "Warning",
        "rollback": "Yes",
        "command": "kubectl rollout undo deployment auth-service"
    },
    "high cpu usage": {
        "fix": "Scale the service or optimize CPU-intensive tasks.",
        "component": "Node-1",
        "severity": "Warning",
        "rollback": "No",
        "command": "kubectl top nodes && kubectl scale deployment"
    }
}

def match_known_issues(log):
    for pattern, issue in known_issues.items():
        if pattern in log.lower():
            return issue
    return None

def analyze_log(log_text, industry):
    matched = match_known_issues(log_text)
    if matched:
        return f"""
Severity: {matched['severity']}
Root Cause: Pattern matched: '{log_text}'
Affected Component: {matched['component']}
Suggested Fix: {matched['fix']}
Should Rollback Deployment: {matched['rollback']}
Suggested Remediation Command: {matched['command']}
"""

    prompt = f"""
You are AIOps Guardian, an AI assistant for DevOps teams.
Context: {industry} industry.

Analyze this log and return:
- Severity (Critical, Warning, Info)
- Root Cause:
- Affected Component:
- Suggested Fix:
- Should Rollback Deployment (Yes/No):
- Suggested Remediation Command:

Log: {log_text}
"""
    response = client.chat.completions.create(
        model="gpt-4",
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

def get_real_time_logs(source):
    return random.choice(sample_logs[source])

# --- Streamlit UI ---
st.set_page_config(page_title="AIOps Guardian", layout="centered")
st.title("🛡️ AIOps Guardian – Log Insight Assistant")

st.markdown("Analyze logs and receive AI-powered diagnosis, root cause, and mitigation suggestions.")

log_source = st.selectbox("Choose a Log Source", list(sample_logs.keys()))
industry = st.selectbox("Industry Context", ["SaaS", "FinTech", "eCommerce"])
model_choice = st.radio("Choose LLM Model", ["GPT-4", "LLaMA-3 (Simulated)"])

log_type = st.radio("Log Mode", ["Manual Selection", "Real-Time Simulation"])

if log_type == "Manual Selection":
    selected_logs = st.multiselect("Select Logs to Analyze", sample_logs[log_source])
else:
    selected_logs = [get_real_time_logs(log_source)]
    st.markdown(f"**Real-time Log**: `{selected_logs[0]}`")

if st.button("🧠 Run AI Analysis"):
    if not selected_logs:
        st.warning("Please select at least one log.")
    else:
        st.markdown("### 📊 Analysis Results")
        for idx, log_entry in enumerate(selected_logs, 1):
            with st.spinner(f"Analyzing log {idx} using {model_choice}..."):
                analysis = analyze_log(log_entry, industry)
                severity = extract_severity(analysis)
                color = get_color(severity)

                st.markdown(f"""
                <div style=\"border-left: 6px solid {color}; padding: 1em; margin-bottom: 1em; background-color: #f9f9f9; border-radius: 6px;\">
                    <h4 style=\"margin: 0 0 0.5em 0;\">📝 Log Entry {idx}</h4>
                    <p><strong>Raw Log:</strong> {log_entry}</p>
                    <p style=\"color: {color};\"><strong>🚦 Severity:</strong> {severity}</p>
                    <pre style=\"white-space: pre-wrap; background-color: #fff; padding: 0.5em; border-radius: 4px;\">{analysis}</pre>
                </div>
                """, unsafe_allow_html=True)

                if "rollback" in analysis.lower():
                    st.button(f"🔁 Rollback Deployment for Entry {idx}")
