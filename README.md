# SupplyMind AI — Self-Healing Supply Chain System

> AI-powered supply chain intelligence with real-time disruption detection, autonomous self-healing, ML demand forecasting, and Gemini-powered AI assistant.

---

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

---

## 🛠 Troubleshooting

- **ModuleNotFoundError**: Run `pip install -r requirements.txt`
- **Port in use**: Set `PORT=5001` in `.env`
- **Gemini not responding**: Check `GEMINI_API_KEY` — fallbacks activate automatically
- **Map not loading**: Wait 3 seconds for Leaflet to download from CDN
