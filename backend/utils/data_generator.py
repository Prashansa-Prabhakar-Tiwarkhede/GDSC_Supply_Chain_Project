"""
Data Generator — Simulated live supply chain data
Provides realistic fleet positions, KPIs, warehouse data, and analytics
"""

import random, math
from datetime import datetime, timedelta

ROUTES = {
    "Trans-Continental Alpha": [(52.52,13.40),(53.08,12.01),(54.32,10.13)],
    "Coastal Express North":   [(51.51,-0.12),(52.48,-1.89),(53.80,-1.55)],
    "Southern Trade Corridor": [(48.85,2.35), (47.90,1.90), (47.22,1.57)],
    "Eastern Freight Lane":    [(50.06,19.94),(51.11,17.03),(52.23,21.01)],
    "Western Supply Chain":    [(40.71,-74.00),(39.95,-75.17),(39.29,-76.61)],
    "Pacific Route Beta":      [(34.05,-118.24),(33.45,-117.60),(32.72,-117.16)],
}

VEHICLES   = [f"V-{str(i).zfill(3)}" for i in range(1, 9)]
PRODUCTS   = ["Electronics","Apparel","Groceries","Pharmaceuticals","FMCG","Cold Chain","Industrial","Automotive"]
ORIGINS    = ["Hub Alpha","Hub Beta","Central Depot","Port Terminal","Rail Head","Regional Centre"]
DESTS      = ["Dist. Centre A","Dist. Centre B","Fulfilment East","Fulfilment West","Retail Node 1","Retail Node 2","End Hub","Metro Depot"]


def _lerp(a, b, t):
    return a + (b - a) * t


def _jitter(lat, lng, r=0.03):
    ang = random.uniform(0, 2 * math.pi)
    d   = random.uniform(0, r)
    return round(lat + d * math.sin(ang), 5), round(lng + d * math.cos(ang), 5)


class DataGenerator:

    # ── Live shipments ──────────────────────────────────────────────────────────
    def get_live_shipments(self):
        route_keys = list(ROUTES.keys())
        now        = datetime.now()
        ships      = []

        for i, vid in enumerate(VEHICLES):
            rk  = route_keys[i % len(route_keys)]
            wps = ROUTES[rk]
            t   = ((now.second + i * 8) / 60 + i * 0.13) % 1.0
            idx = int(t * (len(wps) - 1))
            fr  = t * (len(wps) - 1) - idx

            if idx + 1 < len(wps):
                lat = _lerp(wps[idx][0], wps[idx+1][0], fr)
                lng = _lerp(wps[idx][1], wps[idx+1][1], fr)
            else:
                lat, lng = wps[-1]
            lat, lng = _jitter(lat, lng, 0.025)

            # Deterministic issues on specific vehicles for demo
            delay, blocked, t_breach, status = 0, False, False, "On Time"

            if i == 2:
                delay  = random.randint(95, 145)
                status = "Delayed"
            elif i == 4:
                delay   = random.randint(38, 72)
                blocked = random.random() > 0.42
                status  = "Blocked" if blocked else "Delayed"
            elif i == 6:
                delay  = random.randint(12, 29)
                status = "Minor Delay"
            elif i == 0:
                t_breach = random.random() > 0.58
                status   = "At Risk" if t_breach else "On Time"

            on_time_prob = round(random.uniform(0.28 if delay > 60 else 0.55, 0.99), 2)

            ships.append({
                "id":            vid,
                "route":         rk,
                "lat":           lat,
                "lng":           lng,
                "status":        status,
                "product":       PRODUCTS[i % len(PRODUCTS)],
                "delay_min":     delay,
                "route_blocked": blocked,
                "temp_breach":   t_breach,
                "cargo_pct":     random.randint(7 if i == 3 else 22, 97),
                "fuel_pct":      random.randint(11 if i == 1 else 28, 96),
                "speed_kmh":     0 if blocked else random.randint(26, 84),
                "eta":           (now + timedelta(hours=random.uniform(0.5, 5.5))).strftime("%H:%M"),
                "origin":        ORIGINS[i % len(ORIGINS)],
                "destination":   DESTS[i % len(DESTS)],
                "distance_km":   random.randint(85, 440),
                "on_time_prob":  on_time_prob,
                "driver":        f"Driver {chr(65 + i)}",
            })
        return ships

    # ── Warehouses ─────────────────────────────────────────────────────────────
    def get_warehouses(self):
        configs = [
            ("WH-ALPHA",   "Alpha Regional Hub",       53.55, 10.00, 6000),
            ("WH-BRAVO",   "Bravo Distribution Centre",48.85,  2.35, 4800),
            ("WH-CHARLIE", "Charlie Fulfillment Hub",  52.23, 21.01, 5200),
            ("WH-DELTA",   "Delta Logistics Depot",    40.71,-74.00, 3900),
            ("WH-ECHO",    "Echo Express Centre",      47.37,  8.54, 4200),
            ("WH-FOXTROT", "Foxtrot Port Terminal",    51.51, -0.12, 5500),
        ]
        return [
            {
                "id":              c[0],
                "name":            c[1],
                "lat":             c[2],
                "lng":             c[3],
                "capacity":        c[4],
                "stock_pct":       random.randint(35, 96),
                "inbound_today":   random.randint(2, 14),
                "outbound_today":  random.randint(3, 18),
                "utilisation":     round(random.uniform(0.48, 0.93), 2),
                "temp_ok":         random.random() > 0.08,
            }
            for c in configs
        ]

    # ── KPIs ───────────────────────────────────────────────────────────────────
    def get_kpis(self):
        return {
            "active_vehicles":     len(VEHICLES),
            "on_time_rate":        round(random.uniform(70, 89), 1),
            "alerts_open":         random.randint(2, 9),
            "demand_accuracy":     round(random.uniform(85, 96), 1),
            "auto_healed_today":   random.randint(1, 8),
            "avg_delay_min":       random.randint(5, 42),
            "cost_saved_usd":      random.randint(2800, 22000),
            "sla_compliance":      round(random.uniform(76, 95), 1),
            "network_health":      round(random.uniform(72, 93), 1),
            "vehicles_at_risk":    random.randint(1, 4),
            "orders_today":        random.randint(124, 380),
            "fulfilment_rate":     round(random.uniform(88, 99), 1),
        }

    # ── 30-day demand history ──────────────────────────────────────────────────
    def get_demand_history(self, product):
        bases = {
            "Electronics":820,"Apparel":540,"Groceries":1200,
            "Pharmaceuticals":380,"FMCG":960,"Cold Chain":310,
            "Industrial":450,"Automotive":210,
        }
        base  = bases.get(product, 500)
        today = datetime.today()
        rows  = []
        prev  = base
        for i in range(30, 0, -1):
            d   = today - timedelta(days=i)
            val = max(0, round(prev * random.gauss(1.0, 0.07)))
            prev = val
            rows.append({
                "date":   d.strftime("%b %d"),
                "demand": val,
                "day_name": d.strftime("%A"),
            })
        return rows

    # ── Network health ─────────────────────────────────────────────────────────
    def get_network_health(self):
        nodes = [
            "Supplier Tier 1","Supplier Tier 2","Manufacturing",
            "Distribution","Last Mile","Retail"
        ]
        return [
            {
                "node":   n,
                "health": round(random.uniform(58, 98), 1),
                "risk":   random.choice(["Low","Low","Medium","High"]),
                "trend":  random.choice(["up","up","stable","down"]),
            }
            for n in nodes
        ]

    # ── Analytics (for analytics view) ────────────────────────────────────────
    def get_analytics(self):
        today = datetime.today()
        # weekly shipment volumes
        weekly = []
        for i in range(7, 0, -1):
            d = today - timedelta(days=i)
            weekly.append({
                "day": d.strftime("%a"),
                "delivered": random.randint(18, 52),
                "delayed":   random.randint(2, 9),
                "cancelled": random.randint(0, 3),
            })
        # category breakdown
        categories = [
            {"name": "Electronics",  "pct": 28},
            {"name": "Groceries",    "pct": 22},
            {"name": "FMCG",         "pct": 18},
            {"name": "Apparel",      "pct": 14},
            {"name": "Pharma",       "pct": 10},
            {"name": "Others",       "pct": 8},
        ]
        return {
            "weekly_shipments": weekly,
            "category_breakdown": categories,
            "total_revenue_usd": random.randint(180000, 320000),
            "avg_delivery_hrs":  round(random.uniform(3.2, 6.8), 1),
            "customer_satisfaction": round(random.uniform(82, 97), 1),
        }
