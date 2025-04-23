import streamlit as st
import openai

# Replace with your OpenAI key
client = openai.OpenAI(api_key="sk-...")  # paste your real key here

# Enhanced sample logs with multiple categories like error, warning, and info
sample_logs = {
    "ELK": {
        "error": [
            "ERROR: Payment service failed to connect to database at 10.0.0.4:5432",
            "ERROR: NullPointerException in OrderService at line 234",
            "ERROR: Database timeout occurred on order-service database"
        ],
        "warning": [
            "WARNING: Auth microservice returned 401 Unauthorized after patch deployment",
            "WARNING: Login endpoint response time exceeded threshold (2.5s > 1.0s)"
        ],
        "info": [
            "INFO: Scheduled job inventory-refresh completed in 1203ms",
            "INFO: User 'john.doe' successfully logged in from IP 192.168.1.10"
        ]
    },
    "Prometheus": {
        "error": [
            "ALERT: High CPU usage detected on node-1, threshold 85%",
            "ALERT: 5xx error rate spike on checkout-service > 30% over 5m window"
        ],
        "warning": [
            "ALERT: Disk space low on /dev/sda1 - 92% used",
            "ALERT: pod/web-api restarted 3 times in last 10 minutes"
        ],
        "info": [
            "ALERT: Memory usage > 80% on node-3"
        ]
    },
    "Datadog": {
        "error": [
            "Service 'inventory-api' crashed with exit code 137",
            "Container 'nginx-proxy' OOMKilled"
        ],
        "warning": [
            "Timeout connecting to Redis cache in product-service",
            "High latency detected for endpoint /api/user/12345"
        ],
        "info": [
            "Database query took 4500ms for SELECT on transactions table"
        ]
    }
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

st.markdown("Choose a log source, log type, and let the AI diagnose issues from realistic logs.")

# Log source selection
log_source = st.selectbox("Select Log Source", list(sample_logs.keys()))

# Log type selection (error, warning, info)
log_type = st.selectbox("Select Log Type", list(sample_logs[log_source].keys()))

# Select a log from the chosen source and type
selected_log = st.selectbox("Choose a Sample Log", sample_logs[log_source][log_type])

if st.button("🧠 Analyze Selected Log"):
    with st.spinner("Analyzing with AIOps Guardian..."):
        result = analyze_log(selected_log)
    st.success("Analysis Complete")
    st.text_area("💡 AI Response", result, height=180)
