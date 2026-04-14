import streamlit as st
import json
import time
import pandas as pd

st.set_page_config(layout="wide")

# =========================
# GLASS STYLE
# =========================
st.markdown("""
<style>
html, body, [class*="css"] {
    color: white;
}

.block-container {
    background: linear-gradient(135deg, #0f172a, #020617);
    padding: 20px;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 16px;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 20px rgba(0,0,0,0.4);
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-5px) scale(1.02);
}

.metric-label {
    font-size: 14px;
    opacity: 0.7;
}

.metric-value {
    font-size: 26px;
    font-weight: bold;
}

.log-box {
    height: 260px;
    overflow-y: auto;
    background: rgba(0,0,0,0.4);
    padding: 12px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("AI Self-Healing System Dashboard")

# placeholders
graph_placeholder = st.empty()
main_placeholder = st.empty()
logs_placeholder = st.empty()

# session state
if "history" not in st.session_state:
    st.session_state.history = []

while True:

    try:
        with open("status.json", "r") as f:
            data = json.load(f)
    except:
        st.warning("Waiting for system data...")
        time.sleep(2)
        continue

    # =========================
    # GRAPH
    # =========================
    st.session_state.history.append(data["response_time"])

    if len(st.session_state.history) > 80:
        st.session_state.history.pop(0)

    df = pd.DataFrame(st.session_state.history, columns=["Response Time"])
    df["Smooth"] = df["Response Time"].rolling(5).mean()

    with graph_placeholder.container():
        st.subheader("System Performance")
        st.line_chart(df["Smooth"].fillna(df["Response Time"]))

    # =========================
    # MAIN DASHBOARD CARDS
    # =========================
    with main_placeholder.container():

        col1, col2, col3, col4 = st.columns(4)

        # STATUS CARD
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("System Status")

            if data["health"] == "healthy":
                st.success("Healthy")
            elif data["health"] == "stress":
                st.warning("Under Stress")
            else:
                st.error("Unhealthy")

            st.markdown('</div>', unsafe_allow_html=True)

        # METRICS CARD
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Metrics")

            st.markdown(f'<div class="metric-label">Response Time</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{data["response_time"]:.2f}s</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="metric-label">Status Code</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{data.get("status_code", 0)}</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        # AI INSIGHTS CARD
        with col3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("AI Insights")

            if data.get("anomaly"):
                st.error("Anomaly detected")
            else:
                st.success("Normal behavior")

            st.write("Prediction:", data.get("prediction"))

            # risk bar (clean visualization)
            risk = data.get("prediction_score", 0)
            st.progress(min(max(risk, 0), 1))

            st.caption(f"Trend slope: {round(data.get('trend_slope', 0), 3)}")

            st.markdown('</div>', unsafe_allow_html=True)

        # DECISION ENGINE CARD
        with col4:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Decision Engine")

            st.write("Root Cause:", data.get("root_cause"))
            st.write("Scaling:", data.get("scaling"))

            st.info(data.get("ai_reason", "No explanation"))

            st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # LOGS (CLEAN + READABLE)
    # =========================
    with logs_placeholder.container():
        st.subheader("Activity Log")

        log_html = "<div class='log-box'>"

        for log in reversed(data["logs"][-15:]):

            if "healthy" in log.lower():
                log_html += f"<p style='color:#22c55e;'>System stable</p>"

            elif "stress" in log.lower():
                log_html += f"<p style='color:#f59e0b;'>Moderate load detected</p>"

            elif "unhealthy" in log.lower():
                log_html += f"<p style='color:#ef4444;'>High load detected</p>"

            elif "anomaly" in log.lower():
                log_html += f"<p style='color:#a855f7;'>AI detected anomaly</p>"

            elif "fix" in log.lower():
                log_html += f"<p style='color:#38bdf8;'>Recovery action triggered</p>"

            else:
                log_html += f"<p style='color:#94a3b8;'>Monitoring...</p>"

        log_html += "</div>"

        st.markdown(log_html, unsafe_allow_html=True)

    time.sleep(2)