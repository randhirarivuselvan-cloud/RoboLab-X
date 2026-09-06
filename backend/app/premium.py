from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Plan:
    id: str
    name: str
    price: int
    interval: str
    currency: str
    features: tuple[str, ...]

FREE = Plan("free", "RoboLab Free", 0, "none", "INR", (
    "core_generation", "basic_verification", "project_drafts", "offline_drafts"
))
PRO_MONTHLY = Plan("pro_monthly", "RoboLab Pro", 99, "month", "INR", (
    "advanced_generation", "48_specialist_fleet", "multi_pass_consensus", "adversarial_verification",
    "power_analysis", "firmware_review", "cad_spec", "simulation_plan", "project_export", "priority_generation"
))
PRO_ANNUAL = Plan("pro_annual", "RoboLab Pro", 799, "year", "INR", PRO_MONTHLY.features)

PLANS = {p.id: p for p in (FREE, PRO_MONTHLY, PRO_ANNUAL)}
PRO_FEATURES = frozenset(PRO_MONTHLY.features)

def plan_catalog() -> list[dict]:
    return [{"id": p.id, "name": p.name, "price": p.price, "interval": p.interval, "currency": p.currency, "features": list(p.features)} for p in PLANS.values()]

def entitlements(plan_id: str) -> dict:
    plan = PLANS.get(plan_id, FREE)
    return {"plan": plan.id, "pro": plan.id.startswith("pro_"), "features": list(plan.features)}
