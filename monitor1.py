import requests
import time
import os
import json
from sklearn.ensemble import IsolationForest
import numpy as np

# =========================
# CONFIGURATIONS
# =========================
API = "http://localhost:4000/products"

CHECK_INTERVAL = 5
TIMEOUT = 6
REQUEST_SAMPLES = 3

FAILURE_THRESHOLD = 3
COOLDOWN = 15

# =========================
# ML MODEL
# =========================
model = IsolationForest(contamination=0.1, random_state=42)

ml_data = []
model_trained = False

# =========================
# SYSTEM STATE
# =========================
failure_count = 0
last_fix_time = 0

status_data = {
    "health": "healthy",
    "response_time": 0,
    "status_code": 200,

    "anomaly": False,
    "anomaly_score": 0,
    "normalized_score": 1,

    "prediction": "stable",
    "prediction_score": 0,
    "trend_slope": 0,

    "root_cause": "normal",
    "scaling": "normal",

    "ai_reason": "",

    "logs": []
}

# =========================
# LOGGING
# =========================
def log(msg):
    print(msg)
    status_data["logs"].append(msg)

    if len(status_data["logs"]) > 120:
        status_data["logs"].pop(0)

# =========================
# STABLE RESPONSE
# =========================
def get_response():
    times = []
    status_code = 200

    for _ in range(REQUEST_SAMPLES):
        start = time.time()
        res = requests.get(API, timeout=TIMEOUT)
        times.append(time.time() - start)
        status_code = res.status_code

    rt = sum(times) / len(times)

    if rt < 0.3:
        rt = 0.3

    return rt, status_code

# =========================
# TRAIN MODEL (FIXED)
# =========================
def train_model():
    global model_trained

    # train only on "normal" low latency data
    clean = [x for x in ml_data if x[0] < 1.2]

    if len(clean) < 10:
        clean = ml_data[:25]

    clean = clean[:25]

    model.fit(clean)
    model_trained = True

    log("[ML] model trained")

# =========================
# ANOMALY DETECTION (FIXED)
# =========================
def detect_anomaly(features, rt):
    score = 0
    anomaly = False

    if model_trained:
        score = model.decision_function([features])[0]

        if score < -0.05:
            anomaly = True

    # hard rule fallback
    if rt >= 2.2:
        anomaly = True

    return anomaly, float(score)

# =========================
# PREDICTION ENGINE
# =========================
def predict_failure():
    if len(ml_data) < 6:
        return "stable", 0, 0

    recent = [x[0] for x in ml_data[-6:]]

    avg = sum(recent) / len(recent)

    x = np.arange(len(recent))
    y = np.array(recent)

    slope = np.polyfit(x, y, 1)[0]

    risk = (avg / 2.5) + (slope * 2)

    risk = max(0, min(1, risk))

    if risk > 0.6:
        return "failure likely", risk, slope
    else:
        return "stable", risk, slope

# =========================
# ROOT CAUSE ANALYSIS
# =========================
def find_root_cause(rt, status_code):
    if rt >= 2.2:
        return "latency spike"
    elif status_code == 503 and rt > 1.2:
        return "overload"
    elif status_code != 200:
        return "service failure"
    return "normal"

# =========================
# SCALING DECISION
# =========================
def decide_scaling(root_cause, rt):
    if root_cause == "overload" and rt > 1.5:
        return "scaled up"
    return "normal"

# =========================
# MAIN CHECK LOOP
# =========================
def check_system():
    global ml_data, model_trained

    try:
        rt, status_code = get_response()
        failure_flag = 1 if status_code != 200 else 0

        status_data["response_time"] = rt
        status_data["status_code"] = status_code

        log(f"[CHECK] RT={rt:.2f}s")

        # 🔥 FIXED: only response time used
        features = [rt]
        ml_data.append(features)

        # retrain periodically
        if len(ml_data) > 25 and len(ml_data) % 10 == 0:
            train_model()

        # anomaly detection
        anomaly, score = detect_anomaly(features, rt)

        status_data["anomaly"] = anomaly
        status_data["anomaly_score"] = score
        status_data["normalized_score"] = max(0, min(1, 1 + score))

        # prediction
        prediction, pred_score, slope = predict_failure()

        status_data["prediction"] = prediction
        status_data["prediction_score"] = pred_score
        status_data["trend_slope"] = slope

        if prediction == "failure likely":
            log("[AI] predicted failure")

        # root cause
        root_cause = find_root_cause(rt, status_code)
        status_data["root_cause"] = root_cause

        # scaling
        status_data["scaling"] = decide_scaling(root_cause, rt)

        # explanation
        status_data["ai_reason"] = (
            f"cause={root_cause}, trend={slope:.3f}, risk={pred_score:.2f}"
        )

        # health classification (FIXED thresholds)
        if anomaly or rt >= 2.2:
            status_data["health"] = "unhealthy"
            return False
        elif rt >= 1.5:
            status_data["health"] = "stress"
            return True
        else:
            status_data["health"] = "healthy"
            return True

    except Exception as e:
        log(f"[ERROR] {e}")
        status_data["health"] = "unhealthy"
        return False

# =========================
# SELF-HEALING FIX
# =========================
def fix():
    global last_fix_time

    if time.time() - last_fix_time < COOLDOWN:
        log("[FIX] cooldown")
        return

    cause = status_data["root_cause"]

    if cause == "latency spike":
        os.system("docker restart self-healing-system-product-service-1")
    elif cause == "service failure":
        os.system("docker restart self-healing-system-product-service-1")
        time.sleep(5)
        os.system("docker restart self-healing-system-api-gateway-1")
    elif cause == "overload":
        log("[FIX] scaling handles")
    else:
        os.system("docker restart self-healing-system-product-service-1")

    last_fix_time = time.time()
    log("[FIX] done")

# =========================
# MAIN LOOP
# =========================
while True:

    ok = check_system()

    if not ok:
        failure_count += 1
        if failure_count >= FAILURE_THRESHOLD:
            fix()
            failure_count = 0
    else:
        failure_count = 0

    try:
        with open("status.json", "w") as f:
            json.dump(status_data, f)
    except:
        pass

    time.sleep(CHECK_INTERVAL)
