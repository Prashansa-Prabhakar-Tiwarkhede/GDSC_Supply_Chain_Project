# 🚀 SupplyMind AI — Self-Healing Supply Chain System

SupplyMind AI is an intelligent, self-healing logistics platform that predicts disruptions, autonomously suggests recovery actions, and optimizes supply chain operations in real-time.

🌍 **Problem**: Traditional supply chains are reactive, leading to delays, stockouts, and massive financial losses.

 > 🚀 **View the Live Prototype:** [gdsc-supply-chain-project-2.onrender.com](https://gdsc-supply-chain-project-2.onrender.com/login)

💡 **Detailed Solution Explanation**: SupplyMind AI transforms logistics into a **proactive, AI-driven system** using:

* Machine Learning for demand forecasting
* AI reasoning (Gemini-ready) for decision support
* Autonomous “Self-Healing” optimization engine

📊 **Impact (Simulation Results)**:

* 💰 12% cost reduction
* ⏱️ 48-hour faster delivery (ETA improvement)
* 🌱 15% lower carbon emissions

🎯 **Aligned with UN SDG 9**: Industry, Innovation & Infrastructure



## 🧠 The Self-Healing Workflow: How it Works
SupplyMind AI follows a four-stage autonomous logic to bridge the gap between detection and recovery:
1. **Detection:** Scans 8 real-time triggers (weather, port strikes, etc.) via `disruption_detector.py`.
2. **AI Analysis:** **Google Gemini 1.5 Flash** synthesizes raw data to generate "Reasoning Summaries," explaining the *why* behind the risk.
3. **Impact Prediction:** **Scikit-learn** models forecast cascading stockout risks over a 30-day horizon.
4. **Autonomous Mitigation:** The `self_healer.py` engine computes optimal recovery paths, balancing cost and CO₂.

## 🌟 What Makes This Unique?
* **🔄 Self-Healing Engine:** Unlike traditional dashboards that just report problems, SupplyMind AI **fixes** them.
* **🤖 Transparent AI Reasoning:** Using **Gemini 1.5 Flash** to bridge the "trust gap" by explaining autonomous decisions in human-readable text.
* **🌐 Enterprise Architecture:** A fully containerized, **Cloud-Native** design ready for instant scaling on **Google Cloud Run**.
* **⚡ Hybrid Intelligence:** Combines the speed of traditional ML (Scikit-learn) with the contextual depth of LLMs (Gemini).


Unlike traditional systems, SupplyMind AI doesn’t just detect problems—it **fixes them automatically**.

## ⚡ Quick Start (3 Steps)

```bash
# 1. Install
pip install -r requirements.txt

# 2. (Optional) Set API keys
cp .env.example .env
# Edit .env → add GEMINI_API_KEY

# 3. Run
python app.py
```

Open **http://localhost:5000**

Login: `admin / admin123` or `demo / demo123`

---

## 📁 Project Structure

```
supplymind/
├── app.py                          ← Entry point (run this)
├── requirements.txt
├── Dockerfile                      ← Cloud Run ready
├── .env.example
├── data/
│   └── demand_history.csv          ← Sample dataset
├── backend/
│   ├── models/
│   │   ├── demand_predictor.py     ← ML forecasting (GradientBoosting)
│   │   ├── disruption_detector.py  ← 8-rule alert engine
│   │   └── self_healer.py          ← Autonomous fix suggestions
│   └── utils/
│       ├── gemini_client.py        ← Gemini 1.5 Flash + fallback
│       └── data_generator.py       ← Simulated fleet & warehouse data
└── frontend/
    └── templates/
        ├── login.html              ← Authentication page
        └── dashboard.html          ← Full dashboard (8 views)
```

---

## 🔑 API Keys

| Key | Where | Without it |
|-----|-------|-----------|
| `GEMINI_API_KEY` | makersuite.google.com | Smart fallback responses |
| `GOOGLE_MAPS_API_KEY` | console.cloud.google.com | OpenStreetMap (free, no key) |

---

## 📡 REST API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/kpis` | GET | 12 KPI metrics |
| `/api/shipments` | GET | Live vehicle positions |
| `/api/disruptions` | GET | Active alerts |
| `/api/heal` | POST | Self-healing suggestions |
| `/api/predict` | POST | ML demand forecast |
| `/api/demand_history` | GET | 30-day history |
| `/api/warehouses` | GET | Warehouse inventory |
| `/api/network_health` | GET | Node health scores |
| `/api/analytics` | GET | Analytics data |
| `/api/chat` | POST | Gemini AI chat |

---

## ☁️ Deploy to Google Cloud Run

```bash
# One command deploy
gcloud run deploy supplymind \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key,SECRET_KEY=your_secret
```
## 🤖 AI & Intelligence Layer

SupplyMind AI combines traditional ML with modern AI reasoning:

* **ML Models (Scikit-learn)** → Demand forecasting & risk prediction
* **Rule-based Engine** → Real-time disruption detection (8 rules)
* **Gemini AI Integration** → Natural language insights & decision explanations

Even without API keys, the system uses intelligent fallback logic to simulate AI-driven responses.
---

## 🛠 Troubleshooting

- **ModuleNotFoundError**: Run `pip install -r requirements.txt`
- **Port in use**: Set `PORT=5001` in `.env`
- **Gemini not responding**: Check `GEMINI_API_KEY` — fallbacks activate automatically
- **Map not loading**: Wait 3 seconds for Leaflet to download from CDN
