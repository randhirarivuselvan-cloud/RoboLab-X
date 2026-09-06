from __future__ import annotations

import re
from typing import Any
from .agents import SPECIALISTS, specialist_directory

PRO_FEATURES = {
    "advanced_generation", "consensus", "power_analysis", "firmware_review",
    "cad_spec", "simulation_plan", "project_export", "priority_generation"
}

DOMAIN_KEYWORDS = {
    "power": ("battery", "voltage", "current", "power", "motor", "servo", "charger"),
    "vision": ("camera", "vision", "image", "opencv", "object detection"),
    "navigation": ("gps", "navigation", "path", "slam", "localization", "obstacle"),
    "communications": ("bluetooth", "wifi", "can", "i2c", "spi", "uart", "radio"),
    "actuators": ("motor", "servo", "stepper", "actuator", "wheel", "gripper"),
    "sensors": ("sensor", "imu", "encoder", "ultrasonic", "lidar", "temperature"),
    "firmware": ("arduino", "esp32", "esp8266", "stm32", "firmware", "microcontroller"),
    "mechanical": ("arm", "chassis", "frame", "gear", "joint", "mechanical", "3d print"),
    "cpp": ("c++", "cpp", "arduino", "embedded"),
    "python": ("python", "raspberry pi", "automation"),
    "mobile": ("android", "app", "phone", "flutter"),
}

def _matched_domains(idea: str) -> set[str]:
    text = idea.lower()
    return {domain for domain, words in DOMAIN_KEYWORDS.items() if any(w in text for w in words)}

def _requirement_extract(idea: str) -> list[str]:
    clauses = [c.strip(" .,!?:;") for c in re.split(r"\n|,|;|\band\b", idea, flags=re.I) if c.strip()]
    base = clauses[:12]
    requirements = [f"R{i+1:02d}: {c}" for i, c in enumerate(base)]
    requirements += [
        "Define measurable inputs, outputs and operating environment.",
        "Define electrical, mechanical, thermal, compute and cost constraints.",
        "Define acceptance tests and failure behavior before physical deployment.",
    ]
    return requirements

def _deliverable(agent, idea: str) -> dict[str, Any]:
    matched = _matched_domains(idea)
    relevant = agent.domain in matched or agent.domain in {"systems", "requirements", "verification", "testing", "safety", "auditor", "lead"}
    priority = "primary" if relevant else "supporting"
    return {
        "agent_id": agent.id,
        "agent": agent.name,
        "domain": agent.domain,
        "priority": priority,
        "mission": agent.mission,
        "required_outputs": list(agent.outputs),
        "risk_level": agent.risk_level,
        "work_order": [
            f"Inspect the project for {agent.responsibility}.",
            "State assumptions and missing information explicitly.",
            "Produce concrete recommendations with measurable checks.",
            "Flag conflicts or unsafe/unsupported conclusions for verification.",
        ],
    }

def build_project(idea: str, pro: bool = False) -> dict[str, Any]:
    idea = idea.strip()
    if not idea:
        raise ValueError("idea must not be empty")
    active = SPECIALISTS if pro else tuple(a for a in SPECIALISTS if a.domain in {"systems", "electronics", "power", "embedded", "robotics", "verification", "testing", "safety", "lead"})
    matched = sorted(_matched_domains(idea))
    return {
        "schema_version": "2.0",
        "product": "RoboLab-X",
        "engine": "RoboLab Engineering Intelligence Pipeline",
        "idea": idea,
        "analysis": {"matched_domains": matched, "requirement_count": len(_requirement_extract(idea)), "specialist_count": len(active)},
        "plan": {
            "requirements": _requirement_extract(idea),
            "architecture": "Systems specialist must define subsystem boundaries, interfaces, data flow and failure states.",
            "circuit": "Electronics/power specialists must produce a pin-aware schematic specification and power budget.",
            "firmware": "Embedded/firmware specialists must define drivers, state machines, timing and recovery behavior.",
            "mechanical": "Mechanical/CAD specialists must define geometry, loads, tolerances and fabrication constraints.",
            "simulation": "Simulation specialist must define scenarios, parameters, metrics and pass/fail thresholds.",
            "validation": "Independent verification, adversarial audit and physical testing are mandatory before deployment.",
        },
        "specialist_work_orders": [_deliverable(a, idea) for a in active],
        "pro": pro,
        "premium_capabilities": sorted(PRO_FEATURES) if pro else [],
        "warnings": [
            "AI-generated engineering artifacts are proposals, not certification.",
            "Do not energize hardware until voltage, current, polarity, thermal and mechanical limits are independently checked.",
            "Unknown component specifications must be verified against manufacturer documentation before use.",
        ],
    }

def validate_project(project: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    idea = project.get("idea", "")
    if not idea.strip():
        findings.append({"severity": "error", "code": "EMPTY_IDEA", "message": "Project idea is empty."})
    if len(project.get("plan", {}).get("requirements", [])) < 3:
        findings.append({"severity": "warning", "code": "WEAK_REQUIREMENTS", "message": "Requirements need measurable acceptance criteria."})
    if not project.get("specialist_work_orders"):
        findings.append({"severity": "error", "code": "NO_SPECIALISTS", "message": "No specialist work orders were created."})
    critical = [a for a in project.get("specialist_work_orders", []) if a["risk_level"] == "critical"]
    if len(critical) < 3:
        findings.append({"severity": "warning", "code": "LOW_CRITICAL_REVIEW", "message": "Add independent critical-domain review before approval."})
    findings.append({"severity": "info", "code": "HUMAN_REVIEW", "message": "Human review and physical testing are required before hardware deployment."})
    return findings

def synthesize_consensus(project: dict[str, Any], findings: list[dict[str, str]]) -> dict[str, Any]:
    blocking = [f for f in findings if f["severity"] == "error"]
    warnings = [f for f in findings if f["severity"] == "warning"]
    score = max(0.0, 1.0 - 0.20 * len(blocking) - 0.05 * len(warnings))
    return {
        "status": "blocked" if blocking else "review",
        "confidence": round(score, 2),
        "method": "adversarial multi-specialist consensus",
        "specialists_considered": len(project.get("specialist_work_orders", [])),
        "blocking_findings": blocking,
        "warnings": warnings,
        "approval_gate": "PASS" if not blocking else "FAIL",
        "recommendation": "Resolve blocking findings, then run independent verification and hardware tests." if blocking else "Run specialist generation, adversarial audit and acceptance tests before physical deployment.",
    }
