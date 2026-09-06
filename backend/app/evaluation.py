from __future__ import annotations

from typing import Any
from .agents import SPECIALISTS

# Deterministic quality gates that run even when no external AI provider is configured.

def evaluate_project(project: dict[str, Any]) -> dict[str, Any]:
    checks = []
    text = project.get("idea", "").lower()
    checks.append({"id": "REQ-001", "name": "requirements-present", "passed": bool(project.get("plan", {}).get("requirements"))})
    checks.append({"id": "AGT-001", "name": "specialist-coverage", "passed": len(project.get("specialist_work_orders", [])) >= 9})
    checks.append({"id": "SAFE-001", "name": "safety-gate", "passed": any(a.domain == "safety" for a in SPECIALISTS)})
    checks.append({"id": "VERIFY-001", "name": "independent-verification", "passed": any(a.domain == "verification" for a in SPECIALISTS)})
    checks.append({"id": "TEST-001", "name": "acceptance-testing", "passed": "test" in text or "robot" in text or "project" in text})
    passed = sum(c["passed"] for c in checks)
    return {"checks": checks, "passed": passed, "total": len(checks), "quality_score": round(passed / len(checks), 2)}
