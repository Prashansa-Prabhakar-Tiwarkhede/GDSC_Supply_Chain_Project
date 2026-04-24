"""
Disruption Detector — Real-time supply chain anomaly detection
Scans all vehicles against 8 rule types and generates severity-sorted alerts
"""

from datetime import datetime
import random

RULES = [
    {
        "id":       "SEVERE_DELAY",
        "check":    lambda s: s.get("delay_min", 0) > 90,
        "severity": "critical",
        "title":    "Severe Delivery Delay",
        "msg":      "Vehicle {id} is {delay_min} min behind schedule on {route}. SLA breach imminent.",
        "category": "delay",
        "icon":     "🕐",
    },
    {
        "id":       "MODERATE_DELAY",
        "check":    lambda s: 30 < s.get("delay_min", 0) <= 90,
        "severity": "high",
        "title":    "Delivery Delay",
        "msg":      "Vehicle {id} running {delay_min} min late on {route}.",
        "category": "delay",
        "icon":     "⏱",
    },
    {
        "id":       "ROUTE_BLOCKED",
        "check":    lambda s: s.get("route_blocked", False),
        "severity": "critical",
        "title":    "Route Obstruction Detected",
        "msg":      "Primary route blocked for vehicle {id}. Immediate rerouting required.",
        "category": "route",
        "icon":     "🚧",
    },
    {
        "id":       "CRITICAL_STOCK",
        "check":    lambda s: s.get("cargo_pct", 100) < 12,
        "severity": "critical",
        "title":    "Critical Inventory Level",
        "msg":      "Vehicle {id} cargo at {cargo_pct}% — stockout risk at destination.",
        "category": "inventory",
        "icon":     "📦",
    },
    {
        "id":       "LOW_STOCK",
        "check":    lambda s: 12 <= s.get("cargo_pct", 100) < 25,
        "severity": "high",
        "title":    "Low Inventory Warning",
        "msg":      "Vehicle {id} cargo at {cargo_pct}%. Restock recommended.",
        "category": "inventory",
        "icon":     "📉",
    },
    {
        "id":       "LOW_FUEL",
        "check":    lambda s: s.get("fuel_pct", 100) < 18,
        "severity": "high",
        "title":    "Low Fuel Alert",
        "msg":      "Vehicle {id} fuel at {fuel_pct}%. Operational range at risk.",
        "category": "operational",
        "icon":     "⛽",
    },
    {
        "id":       "TEMP_BREACH",
        "check":    lambda s: s.get("temp_breach", False),
        "severity": "critical",
        "title":    "Cold Chain Temperature Breach",
        "msg":      "Refrigeration failure on vehicle {id}. Perishable cargo at risk.",
        "category": "quality",
        "icon":     "🌡",
    },
    {
        "id":       "SPEED_ANOMALY",
        "check":    lambda s: s.get("speed_kmh", 60) < 8 and s.get("status") not in ("Idle", "On Time"),
        "severity": "medium",
        "title":    "Speed Anomaly",
        "msg":      "Vehicle {id} moving at {speed_kmh} km/h — possible breakdown or obstruction.",
        "category": "operational",
        "icon":     "🐢",
    },
]

SEV_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


class DisruptionDetector:
    def scan(self, shipments: list) -> list:
        alerts = []
        for s in shipments:
            for rule in RULES:
                if rule["check"](s):
                    msg = rule["msg"].format(
                        id        = s.get("id", "—"),
                        delay_min = s.get("delay_min", 0),
                        route     = s.get("route", "Unknown"),
                        cargo_pct = s.get("cargo_pct", 0),
                        fuel_pct  = s.get("fuel_pct", 0),
                        speed_kmh = s.get("speed_kmh", 0),
                    )
                    alerts.append({
                        "alert_id":   f"{rule['id']}_{s['id']}_{int(datetime.now().timestamp())}",
                        "rule":       rule["id"],
                        "severity":   rule["severity"],
                        "category":   rule["category"],
                        "icon":       rule["icon"],
                        "title":      rule["title"],
                        "message":    msg,
                        "vehicle_id": s["id"],
                        "route":      s.get("route", ""),
                        "product":    s.get("product", ""),
                        "timestamp":  datetime.now().strftime("%H:%M:%S"),
                        "shipment":   s,
                    })

        alerts.sort(key=lambda a: SEV_RANK.get(a["severity"], 9))
        return alerts
