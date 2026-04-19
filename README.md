# AI Self-Healing Microservices System (Kubernetes + ML)

An autonomous system that detects failures, predicts system degradation, and recovers services without human intervention.

Built during a 36-hour hackathon at Tech Solstice, this project demonstrates a real-world AIOps pipeline using microservices, machine learning, chaos engineering, and Kubernetes.

---

## Overview

Modern distributed systems often fail under unpredictable conditions such as high load, latency spikes, or service crashes.

This project implements a self-healing architecture that:

- Monitors system health in real time
- Detects anomalies using ML
- Predicts potential failures
- Identifies root causes
- Automatically recovers the system

---

## Architecture

User / Load (k6)
↓
API Gateway
↓
Microservices (Product, Order, Auth, etc.)
↓
Monitoring System (Python + ML)
↓
Decision Engine
↓
Recovery (Restart / Scaling)
↓
Dashboard (Streamlit)

---

## Features

### Monitoring
- Real-time response time tracking
- Status code monitoring
- Multi-sample averaging for stability

### Machine Learning
- Isolation Forest for anomaly detection
- Trend-based prediction (moving average + slope)
- Continuous retraining on live data

### Chaos Engineering
- Random failure injection (503 errors)
- Latency spikes simulation
- Load testing using k6

### Decision Engine
- Root cause analysis:
  - Latency spike
  - Overload
  - Service failure
- Smart recovery strategy selection

### Self-Healing
- Automatic container restart
- Cooldown mechanism to prevent over-triggering
- Load-aware scaling decisions

### Kubernetes Integration
- Deployment of services as pods
- Service-based communication
- Horizontal scaling support (HPA)

### Dashboard
- Glass-style UI (Streamlit)
- Real-time system health
- AI insights and predictions
- Clean activity logs

---

## Example Behavior

Under high load:

- System detects rising latency
- ML model flags anomaly
- Prediction engine forecasts failure
- Root cause identified (overload)
- Recovery triggered (restart / scale)
- System stabilizes automatically

---

## Tech Stack

- Backend: Node.js (Express)
- ML / Monitoring: Python (scikit-learn, requests)
- Frontend / Dashboard: Streamlit
- Load Testing: k6
- Containerization: Docker
- Orchestration: Kubernetes (Minikube)

---

## Project Structure

├── api-gateway/
├── product-service/
├── order-service/
├── auth-service/
├── frontend/
├── monitor1.py
├── dashboard.py
├── load.js
├── docker-compose.yml
├── k8s/
└── status.json

---

## Getting Started

### 1. Clone the repo

git clone [YOUR_REPO_LINK]
cd self-healing-system

---

### 2. Run using Docker

docker-compose up --build

---

### 3. Start monitoring system

python monitor1.py

---

### 4. Run dashboard

streamlit run dashboard.py

---

### 5. Simulate load

k6 run load.js

---

## Kubernetes Setup (Optional)

minikube start
kubectl apply -f k8s/
minikube service api-gateway

---

## Key Concepts

- AIOps (AI for IT Operations)
- Self-healing systems
- Chaos engineering
- Microservices architecture
- Predictive failure detection

---

## Team

- Tanmay Das  
- Arin Pattnaik
- Dhruv Agarwal 
- Ansh Jain

---

## Credentials

- GitHub: [Add Link]
- Demo: [Add Link]
- Certificate ID: [Add ID]
- Credential URL: [Add Link]

---

## Key Takeaway

Instead of reacting to failures after they occur, systems can proactively predict, adapt, and heal themselves, improving reliability and reducing downtime in distributed environments.

---

## Future Improvements

- Full Kubernetes-native recovery (pod-level actions)
- Advanced ML models (LSTM)
- Prometheus + Grafana integration
- Traffic rerouting strategies
- Multi-region deployment

---

## License

This project is for educational and hackathon purposes.
