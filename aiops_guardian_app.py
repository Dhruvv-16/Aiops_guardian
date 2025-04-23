import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Sample logs, replace with real data ingestion from Prometheus, Datadog, ELK, etc.
logs = [
    {'timestamp': '2025-04-23 10:00', 'metric_value': 200, 'message': 'Service A started', 'severity': 'INFO', 'component': 'Service A'},
    {'timestamp': '2025-04-23 10:05', 'metric_value': 1000, 'message': 'Error connecting to DB', 'severity': 'ERROR', 'component': 'DB'},
    {'timestamp': '2025-04-23 10:10', 'metric_value': 500, 'message': 'Service A response time high', 'severity': 'WARNING', 'component': 'Service A'},
    {'timestamp': '2025-04-23 10:15', 'metric_value': 300, 'message': 'Service A finished successfully', 'severity': 'INFO', 'component': 'Service A'},
]

# Simulated log ingestion
def ingest_logs():
    # Replace with API calls to real-time data sources like Prometheus, Datadog, or ELK
    return logs

# Understanding log type and severity, and classifying incidents
def analyze_log(log):
    if log['severity'] == 'ERROR':
        return "Critical Error: Immediate attention required."
    elif log['severity'] == 'WARNING':
        return "Warning: Potential issue detected, monitor closely."
    elif log['severity'] == 'INFO':
        return "Info: All systems operational."
    else:
        return "Unknown severity level."

# Predicting incidents (Using simple anomaly detection as a placeholder for predictive modeling)
def predict_incidents(logs_data):
    # Use IsolationForest to detect anomalies in the metrics (metric_value)
    model = IsolationForest(contamination=0.1)
    metric_values = [log['metric_value'] for log in logs_data]
    scaler = StandardScaler()
    metric_values_scaled = scaler.fit_transform(np.array(metric_values).reshape(-1, 1))
    model.fit(metric_values_scaled)
    
    predictions = model.predict(metric_values_scaled)
    incident_indices = [i for i, pred in enumerate(predictions) if pred == -1]
    
    incidents = []
    for i in incident_indices:
        incidents.append(logs_data[i])
    
    return incidents

# Suggesting mitigations based on log severity and content
def suggest_mitigation(log):
    if log['severity'] == 'ERROR':
        if 'DB' in log['component']:
            return "Check database health, connection pool, and scaling."
        elif 'Deployment' in log['message']:
            return "Rollback to stable version, investigate deployment pipeline."
    elif log['severity'] == 'WARNING':
        if 'Service A' in log['component']:
            return "Service A response time is high. Scale or optimize."
    elif log['severity'] == 'INFO':
        return "System is running normally. No action needed."
    return "No mitigation available."

# Visualizing metric trends with anomalies
def plot_metric_trends(log_data, anomalies):
    timestamps = [log['timestamp'] for log in log_data]
    metric_values = [log['metric_value'] for log in log_data]
    
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, metric_values, label='Metric Value', color='blue', marker='o')
    
    # Highlight anomalies
    anomaly_times = [timestamps[i] for i in range(len(anomalies)) if anomalies[i] == -1]
    anomaly_values = [metric_values[i] for i in range(len(anomalies)) if anomalies[i] == -1]
    
    plt.scatter(anomaly_times, anomaly_values, color='red', label='Anomalies', zorder=5)
    plt.xlabel('Timestamp')
    plt.ylabel('Metric Value')
    plt.title('Metric Trends with Anomalies')
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(plt)

# Main Streamlit app
def main():
    st.title("AIOps Guardian - Real-Time Log Monitoring")

    # Step 1: Ingest logs
    logs_data = ingest_logs()

    # Step 2: Analyze logs and understand their type
    st.subheader("Log Analysis")
    analyzed_logs = [analyze_log(log) for log in logs_data]
    for i, analysis in enumerate(analyzed_logs):
        st.write(f"Log {i+1}: {analysis}")

    # Step 3: Predict potential incidents based on log data
    st.subheader("Incident Prediction")
    incidents = predict_incidents(logs_data)
    if incidents:
        st.write("Predicted Incidents:")
        for incident in incidents:
            st.write(f"Incident: {incident['message']} | Component: {incident['component']}")
    else:
        st.success("No incidents predicted.")

    # Step 4: Suggest mitigations based on log severity
    st.subheader("Suggested Mitigations")
    for i, log in enumerate(logs_data):
        mitigation = suggest_mitigation(log)
        st.write(f"Log {i+1} Mitigation: {mitigation}")

    # Step 5: Visualize metric trends and anomalies
    st.subheader("Metric Trend Visualization")
    anomalies = [1 if log['severity'] == 'INFO' else -1 for log in logs_data]
    plot_metric_trends(logs_data, anomalies)

# Run the app
if __name__ == "__main__":
    main()
