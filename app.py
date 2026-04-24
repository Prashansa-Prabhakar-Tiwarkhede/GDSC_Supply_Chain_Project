"""
SupplyMind AI — Self-Healing Supply Chain System
Main Flask application entry point
Run: python app.py
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
import os, json, hashlib
from dotenv import load_dotenv

load_dotenv()

from backend.models.demand_predictor import DemandPredictor
from backend.models.disruption_detector import DisruptionDetector
from backend.models.self_healer import SelfHealer
from backend.utils.gemini_client import GeminiClient
from backend.utils.data_generator import DataGenerator

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)
app.secret_key = os.environ.get("SECRET_KEY", "supplymind-secret-2024")
CORS(app)

# ── Initialise all AI modules ─────────────────────────────────────────────────
predictor = DemandPredictor()
detector  = DisruptionDetector()
healer    = SelfHealer()
gemini    = GeminiClient()
datagen   = DataGenerator()

predictor.train()   # train ML model once at startup (~2 seconds)

# ── Demo users (no DB needed) ─────────────────────────────────────────────────
USERS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "demo":  hashlib.sha256("demo123".encode()).hexdigest(),
}

# ── Auth helpers ──────────────────────────────────────────────────────────────
def logged_in():
    return session.get("user") is not None

# ══════════════════════════════════════════════════════════════════════════════
# PAGE ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/")
def root():
    if logged_in():
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        hashed   = hashlib.sha256(password.encode()).hexdigest()
        if USERS.get(username) == hashed:
            session["user"] = username
            return redirect(url_for("dashboard"))
        error = "Invalid username or password."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if not logged_in():
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session.get("user"))

# ══════════════════════════════════════════════════════════════════════════════
# API ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/api/kpis")
def api_kpis():
    return jsonify(datagen.get_kpis())

@app.route("/api/shipments")
def api_shipments():
    return jsonify(datagen.get_live_shipments())

@app.route("/api/disruptions")
def api_disruptions():
    ships = datagen.get_live_shipments()
    return jsonify(detector.scan(ships))

@app.route("/api/heal", methods=["POST"])
def api_heal():
    issue = request.get_json(force=True)
    return jsonify(healer.suggest(issue))

@app.route("/api/warehouses")
def api_warehouses():
    return jsonify(datagen.get_warehouses())

@app.route("/api/predict", methods=["POST"])
def api_predict():
    body    = request.get_json(force=True)
    product = body.get("product", "Electronics")
    days    = int(body.get("days", 7))
    return jsonify(predictor.predict(product, days))

@app.route("/api/demand_history")
def api_demand_history():
    product = request.args.get("product", "Electronics")
    return jsonify(datagen.get_demand_history(product))

@app.route("/api/network_health")
def api_network_health():
    return jsonify(datagen.get_network_health())

@app.route("/api/analytics")
def api_analytics():
    return jsonify(datagen.get_analytics())

@app.route("/api/chat", methods=["POST"])
def api_chat():
    body    = request.get_json(force=True)
    message = body.get("message", "")
    context = body.get("context", {})
    return jsonify({"reply": gemini.ask(message, context)})

@app.route("/api/products")
def api_products():
    return jsonify(DemandPredictor.list_products())

# ── Health check for Cloud Run ────────────────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "supplymind-ai"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n🚀 SupplyMind AI running at http://localhost:{port}")
    print("   Login: admin / admin123  or  demo / demo123\n")
    app.run(debug=True, host="0.0.0.0", port=port)
