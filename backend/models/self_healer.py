"""
Self-Healer Engine — Autonomous fix suggestion system
Generates ranked solutions based on disruption type
"""

import random

ALT_ROUTES = [
    {"name": "Express Corridor A",  "save_min": 45, "km": 92,  "cost": "+12%", "risk": "Low",    "confidence_base": 94},
    {"name": "Alternate Route B",   "save_min": 28, "km": 118, "cost": "+5%",  "risk": "Low",    "confidence_base": 91},
    {"name": "Bypass Route C",      "save_min": 18, "km": 134, "cost": "+2%",  "risk": "Medium", "confidence_base": 87},
    {"name": "Highway Corridor D",  "save_min": 35, "km": 104, "cost": "+8%",  "risk": "Low",    "confidence_base": 92},
    {"name": "Inland Route E",      "save_min": 12, "km": 148, "cost": "0%",   "risk": "Low",    "confidence_base": 83},
]

WAREHOUSES = [
    {"id": "WH-ALPHA",   "name": "Alpha Regional Hub",      "stock": 94, "eta_hrs": 1.5, "capacity": 6000},
    {"id": "WH-BRAVO",   "name": "Bravo Distribution Centre","stock": 82, "eta_hrs": 2.0, "capacity": 4800},
    {"id": "WH-CHARLIE", "name": "Charlie Fulfillment Hub",  "stock": 71, "eta_hrs": 2.5, "capacity": 5200},
    {"id": "WH-DELTA",   "name": "Delta Logistics Depot",    "stock": 88, "eta_hrs": 1.8, "capacity": 3900},
    {"id": "WH-ECHO",    "name": "Echo Express Centre",      "stock": 65, "eta_hrs": 3.0, "capacity": 4200},
]

SUPPLIERS = [
    {"id": "SUP-01", "name": "Apex FastSupply Co.",       "lead_hrs": 2,  "reliability": 99, "cost": "+10%"},
    {"id": "SUP-02", "name": "Prime Logistics Group",     "lead_hrs": 3,  "reliability": 97, "cost": "+6%"},
    {"id": "SUP-03", "name": "SwiftSource International", "lead_hrs": 4,  "reliability": 94, "cost": "+3%"},
    {"id": "SUP-04", "name": "Global Trade Alliance",     "lead_hrs": 6,  "reliability": 91, "cost": "+1%"},
    {"id": "SUP-05", "name": "Continental Supply Corp.",  "lead_hrs": 8,  "reliability": 87, "cost": "0%"},
]


class SelfHealer:
    def suggest(self, issue: dict) -> dict:
        rule     = issue.get("rule", "")
        vehicle  = issue.get("vehicle_id", "V-001")
        solutions = []

        # ── Delay / Route problems → alternate routes ─────────────────────────
        if rule in ("SEVERE_DELAY", "MODERATE_DELAY", "ROUTE_BLOCKED", "SPEED_ANOMALY"):
            sampled = random.sample(ALT_ROUTES, min(3, len(ALT_ROUTES)))
            sampled.sort(key=lambda r: -r["save_min"])
            badges = ["⚡ Fastest", "💰 Most Economic", "🛡 Safest"]
            for idx, r in enumerate(sampled[:3]):
                conf = r["confidence_base"] + random.randint(-3, 3)
                solutions.append({
                    "type":   "reroute",
                    "icon":   "🗺️",
                    "title":  f"Switch to {r['name']}",
                    "detail": f"Save ~{r['save_min']} min · {r['km']} km · Cost {r['cost']} · Risk: {r['risk']}",
                    "badge":  badges[idx] if idx < len(badges) else "Option",
                    "action": "REROUTE",
                    "payload": {"vehicle_id": vehicle, "new_route": r["name"]},
                    "confidence": conf,
                    "impact": "high",
                })

        # ── Inventory problems → warehouse dispatch ───────────────────────────
        if rule in ("CRITICAL_STOCK", "LOW_STOCK", "TEMP_BREACH"):
            avail = [w for w in WAREHOUSES if w["stock"] > 45]
            avail.sort(key=lambda w: (-w["stock"], w["eta_hrs"]))
            wh_badges = ["✅ Best Stock", "🕐 Fastest ETA"]
            for idx, wh in enumerate(avail[:2]):
                solutions.append({
                    "type":   "warehouse",
                    "icon":   "🏭",
                    "title":  f"Dispatch from {wh['name']}",
                    "detail": f"Stock: {wh['stock']}% · ETA: {wh['eta_hrs']} hrs · Cap: {wh['capacity']:,} units",
                    "badge":  wh_badges[idx] if idx < len(wh_badges) else "Available",
                    "action": "DISPATCH_WAREHOUSE",
                    "payload": {"warehouse_id": wh["id"]},
                    "confidence": round(88 + random.uniform(-4, 6), 1),
                    "impact": "high",
                })

        # ── Fuel problems → nearest station ──────────────────────────────────
        if rule == "LOW_FUEL":
            solutions.append({
                "type":   "fuel",
                "icon":   "⛽",
                "title":  "Navigate to nearest fuel depot",
                "detail": "Auto-routes vehicle to closest certified fuel station en route.",
                "badge":  "🚀 Instant",
                "action": "NAVIGATE_FUEL",
                "payload": {"vehicle_id": vehicle},
                "confidence": 99,
                "impact": "medium",
            })

        # ── Always: offer faster supplier ─────────────────────────────────────
        sup = random.choice(SUPPLIERS[:3])
        solutions.append({
            "type":   "supplier",
            "icon":   "🤝",
            "title":  f"Activate {sup['name']}",
            "detail": f"Lead time: {sup['lead_hrs']} hrs · Reliability: {sup['reliability']}% · Cost: {sup['cost']}",
            "badge":  "📋 Backup",
            "action": "SWITCH_SUPPLIER",
            "payload": {"supplier_id": sup["id"]},
            "confidence": round(78 + random.uniform(-3, 10), 1),
            "impact": "medium",
        })

        solutions.sort(key=lambda s: -s["confidence"])

        return {
            "issue":                issue,
            "solutions":            solutions,
            "top_recommendation":   solutions[0] if solutions else None,
            "estimated_recovery":   random.randint(12, 48),
            "auto_apply_eligible":  solutions[0]["confidence"] >= 90 if solutions else False,
        }
