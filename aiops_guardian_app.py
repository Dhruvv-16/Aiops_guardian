import streamlit as st
import openai
import random

# Initialize OpenAI client
client = openai.OpenAI(api_key="sk-...")  # Replace with your actual key

# Known issues for quick fixes
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

# Function to match known issues
def match_known_issues(log):
    for pattern, issue in known_issues.items():
        if pattern in log.lower():
            return issue
    return None

# Analyze log function
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

# Extract severity from response
def extract_severity(ai_response):
    for line in ai_response.splitlines():
        if "Severity" in line:
            return line.split(":")[1].strip()
    return "Unknown"

# Get color based on severity
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

st.markdown("Provide a custom log and get AI-powered diagnosis, root cause analysis, and suggested fixes.")

industry = st.selectbox("Industry Context", ["SaaS", "FinTech", "eCommerce"])

# Log input
custom_log = st.text_area("Paste your custom log here")

# Button to run analysis
if st.button("🧠 Run AI Analysis"):
    if not custom_log:
        st.warning("Please paste a log to analyze.")
    else:
        st.markdown("### 📊 Analysis Results")
        with st.spinner(f"Analyzing log..."):
            analysis = analyze_log(custom_log, industry)
            severity = extract_severity(analysis)
            color = get_color(severity)

            st.markdown(f"""
            <div style="border-left: 6px solid {color}; padding: 1em; margin-bottom: 1em; background-color: #f9f9f9; border-radius: 6px;">
                <h4 style="margin: 0 0 0.5em 0;">📝 Log Entry</h4>
                <p><strong>Raw Log:</strong> {custom_log}</p>
                <p style="color: {color};"><strong>🚦 Severity:</strong> {severity}</p>
                <pre style="white-space: pre-wrap; background-color: #fff; padding: 0.5em; border-radius: 4px;">{analysis}</pre>
            </div>
            """, unsafe_allow_html=True)
