from typing import Any
from .agents import specialist_directory

PRO_FEATURES = {
    "advanced_generation", "consensus", "power_analysis", "firmware_review",
    "cad_spec", "simulation_plan", "project_export", "priority_generation"
}

def build_project(idea: str, pro: bool = False) -> dict[str, Any]:
    idea = idea.strip()
    if not idea:
        raise ValueError("idea must not be empty")

    active = ["systems", "electronics", "power", "embedded", "robotics", "verification"]
    if pro:
        active = [a["domain"] for a in specialist_directory()]

    return {
        "schema_version": "1.0",
        "product": "RoboLab-X",
        "idea": idea,
        "plan": {
            "requirements": ["Define inputs, outputs, constraints and acceptance tests"],
            "architecture": "Pending specialist synthesis",
            "circuit": "Pending circuit synthesis",
            "firmware": "Pending firmware synthesis",
            "validation": "Independent checks required before build",
        },
        "specialists": active,
        "pro": pro,
        "warnings": [
            "Generated engineering artifacts must be reviewed and tested before physical deployment."
        ],
    }


def validate_project(project: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not project.get("idea"):
        findings.append({"severity": "error", "code": "EMPTY_IDEA", "message": "Project idea is empty."})
    if not project.get("plan", {}).get("requirements"):
        findings.append({"severity": "warning", "code": "NO_REQUIREMENTS", "message": "Requirements are not defined."})
    findings.append({"severity": "info", "code": "REVIEW_REQUIRED", "message": "Human review and physical testing are required before deployment."})
    return findings


def synthesize_consensus(project: dict[str, Any], findings: list[dict[str, str]]) -> dict[str, Any]:
    blocking = [f for f in findings if f["severity"] == "error"]
    return {
        "status": "blocked" if blocking else "review",
        "confidence": 0.0 if blocking else 0.75,
        "blocking_findings": blocking,
        "recommendation": "Resolve blocking findings, then run verification and hardware tests." if blocking else "Proceed to detailed specialist generation and verification.",
    }
