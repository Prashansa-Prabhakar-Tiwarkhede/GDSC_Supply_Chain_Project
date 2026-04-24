"""
Gemini AI Client — Google Gemini 1.5 Flash integration
Falls back to expert pre-written responses if no API key is set
"""

import os, json, random

try:
    import google.generativeai as genai
    GEMINI_OK = True
except ImportError:
    GEMINI_OK = False

SYSTEM_PROMPT = """You are SupplyMind, an elite AI operations assistant for a self-healing supply chain platform.

Your expertise covers:
- Real-time delivery delay analysis and root-cause identification
- Demand forecasting interpretation and procurement recommendations
- Route optimization and traffic/logistics intelligence
- Warehouse inventory strategy and redistribution
- Supplier risk assessment and alternative sourcing
- Supply chain KPI analysis and improvement recommendations

Response rules:
- Always be concise: 80-130 words maximum unless asked for detail
- Use bullet points for multi-part answers
- Always end with a bold "**Recommended Action:**" section
- Be data-driven and specific — mention numbers when relevant
- Refer to the live system context if provided
- Tone: professional, confident, decisive — like a senior supply chain director"""

FALLBACKS = {
    "delay": [
        "**Delay Root Cause Analysis:**\n- Primary cause: traffic congestion or road incident on active corridor\n- Secondary factor: sub-optimal departure timing from origin hub\n- Compounding: vehicle speed reduced to ~42 km/h\n\n**Impact:** SLA breach projected by ~40 minutes\n\n**Recommended Action:** Approve the alternate route from the self-healing panel immediately. Simultaneously notify the destination of the revised ETA and update the customer record.",
        "**Delay Analysis:**\n- Weather disruption detected near the active route\n- Vehicle operating at 60% of optimal speed\n- No backup vehicle currently en route\n\n**Impact:** 2+ hour SLA breach projected\n\n**Recommended Action:** Dispatch backup vehicle from nearest hub (ETA 1.5 hrs). Reroute primary vehicle to bypass affected zone. Escalate to operations manager if delay exceeds 3 hours.",
    ],
    "demand": [
        "**Demand Forecast Insight:**\n- Current trend: +18% above baseline — driven by seasonal uplift\n- Stockout risk: 34% probability within 36 hours at current levels\n- Weekly pattern shows peak demand on weekends\n\n**Recommended Action:** Pre-position 600 additional units at primary distribution hub before tomorrow morning. Trigger a purchase order with your Tier-1 supplier today.",
        "**Forecast Summary:**\n- Demand trending upward: +12% week-on-week\n- Model confidence: 91% based on 6 months of training data\n- No stockout risk in the next 7 days\n\n**Recommended Action:** Standard replenishment order is sufficient. Schedule delivery for mid-week to avoid weekend congestion.",
    ],
    "route": [
        "**Route Comparison:**\n- Current route: ~158 km, 3.2 hrs ETA — partially congested\n- Express Corridor A: 92 km, 1.9 hrs — fastest, +12% cost\n- Alternate Route B: 118 km, 2.4 hrs — best balance, +5% cost\n\n**Recommended Action:** Switch to Alternate Route B for the optimal time-cost balance. Reserve Express Corridor A for time-critical SLA breaches only.",
    ],
    "inventory": [
        "**Inventory Analysis:**\n- Alpha Hub: 94% stocked — ideal dispatch point\n- Delta Depot: 88% stocked — strong secondary option\n- Echo Centre: 65% — approaching reorder threshold\n\n**Recommended Action:** Dispatch from Alpha Hub for fastest resolution. Simultaneously trigger a replenishment order for Echo Centre — current trajectory hits critical level in 4 days.",
    ],
    "supplier": [
        "**Supplier Assessment:**\n- Primary supplier lead time: 48 hrs — too slow for current disruption\n- Apex FastSupply: 2 hrs lead time, 99% reliability — premium cost\n- Prime Logistics Group: 3 hrs, 97% reliability — balanced option\n\n**Recommended Action:** Activate Prime Logistics Group for this incident (best reliability/cost ratio). Document primary supplier performance for quarterly review.",
    ],
    "default": [
        "**Supply Chain Health Summary:**\n- Overall network health: 84% (Good)\n- 3 active disruptions require attention\n- Demand predictions within normal variance\n- 2 warehouses approaching reorder thresholds\n\n**Recommended Action:** Review the critical alerts panel and approve the top self-healing recommendations. Priority: address the route blockage first, then the inventory shortage.",
        "**System Status:**\n- Fleet: 8 vehicles active, 2 with active alerts\n- Demand forecast accuracy: 91% this week\n- 1 self-healing action auto-applied in the last hour\n\n**Recommended Action:** No immediate action required. Schedule a warehouse inventory review for the West Hub — stock trending below optimal threshold.",
    ],
}


class GeminiClient:
    def __init__(self):
        self.key   = os.environ.get("GEMINI_API_KEY", "")
        self.model = None
        if GEMINI_OK and self.key:
            try:
                genai.configure(api_key=self.key)
                self.model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=SYSTEM_PROMPT,
                )
            except Exception:
                pass

    def ask(self, message: str, context: dict = {}) -> str:
        # Try real Gemini first
        if self.model:
            try:
                ctx_str = json.dumps(context, indent=2) if context else ""
                full    = f"{message}\n\nLive system context:\n{ctx_str}" if ctx_str else message
                return self.model.generate_content(full).text
            except Exception:
                pass

        # Smart keyword fallback
        m = message.lower()
        if any(w in m for w in ["delay", "late", "slow", "stuck", "behind", "not arrived"]):
            return random.choice(FALLBACKS["delay"])
        if any(w in m for w in ["demand", "predict", "forecast", "stock out", "units needed"]):
            return random.choice(FALLBACKS["demand"])
        if any(w in m for w in ["route", "road", "path", "direction", "fastest way"]):
            return random.choice(FALLBACKS["route"])
        if any(w in m for w in ["inventory", "warehouse", "stock", "storage", "shortage"]):
            return random.choice(FALLBACKS["inventory"])
        if any(w in m for w in ["supplier", "vendor", "source", "procurement"]):
            return random.choice(FALLBACKS["supplier"])
        return random.choice(FALLBACKS["default"])
