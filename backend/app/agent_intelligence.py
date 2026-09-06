from __future__ import annotations

# Domain-specific reasoning instructions make each specialist materially different.
# These are orchestration/model instructions, not claims of separately trained neural networks.
REASONING_PACKS: dict[str, dict[str, object]] = {
    "systems": {"focus": ["requirements traceability", "interfaces", "failure states", "architecture tradeoffs"], "checks": ["missing requirements", "single points of failure", "interface ambiguity"]},
    "electronics": {"focus": ["signal integrity", "logic levels", "component ratings", "schematic consistency"], "checks": ["absolute maximum ratings", "pull-ups/pull-downs", "grounding", "decoupling"]},
    "power": {"focus": ["rail sizing", "peak current", "protection", "thermal margin"], "checks": ["startup surge", "brownout", "reverse polarity", "wire/fuse limits"]},
    "embedded": {"focus": ["pin mapping", "interrupts", "timers", "peripheral ownership"], "checks": ["race conditions", "watchdog recovery", "boot behavior", "resource limits"]},
    "firmware": {"focus": ["state machines", "fault handling", "determinism", "regression testing"], "checks": ["timeouts", "invalid inputs", "sensor failure", "safe recovery"]},
    "robotics": {"focus": ["subsystem integration", "robot behavior", "actuation", "environmental constraints"], "checks": ["integration conflicts", "failure modes", "workspace", "operator interaction"]},
    "control": {"focus": ["feedback loops", "sampling", "stability", "saturation"], "checks": ["latency", "noise", "windup", "unstable edge cases"]},
    "mechanical": {"focus": ["loads", "clearances", "fasteners", "tolerances"], "checks": ["stress assumptions", "fatigue", "collision", "assembly access"]},
    "cad": {"focus": ["parametric dimensions", "datums", "manufacturing constraints", "assembly interfaces"], "checks": ["clearance", "wall thickness", "tolerance stack-up", "tool access"]},
    "simulation": {"focus": ["repeatable scenarios", "parameters", "metrics", "pass/fail thresholds"], "checks": ["unrealistic assumptions", "coverage gaps", "sensitivity", "validation against physical tests"]},
    "materials": {"focus": ["strength", "temperature", "chemical/environmental compatibility", "fabrication"], "checks": ["derating", "moisture", "wear", "availability"]},
    "safety": {"focus": ["hazard identification", "protective measures", "operating limits", "test controls"], "checks": ["energy sources", "unexpected motion", "thermal hazards", "fail-safe behavior"]},
    "software": {"focus": ["modularity", "contracts", "error handling", "maintainability"], "checks": ["null/invalid states", "timeouts", "dependency failures", "data validation"]},
    "cpp": {"focus": ["resource constraints", "portable C/C++", "memory safety", "build reproducibility"], "checks": ["buffer boundaries", "lifetime", "concurrency", "undefined behavior"]},
    "mobile": {"focus": ["Android lifecycle", "offline-first behavior", "network resilience", "accessible UX"], "checks": ["reconnection", "state restoration", "secret exposure", "large-project performance"]},
    "backend": {"focus": ["API contracts", "validation", "observability", "scalability"], "checks": ["authentication boundaries", "rate limits", "untrusted input", "timeouts"]},
    "data": {"focus": ["versioned schemas", "integrity", "migrations", "export/import"], "checks": ["backward compatibility", "partial writes", "duplicate records", "corrupt input"]},
    "ai": {"focus": ["routing", "structured output", "model selection", "evaluation"], "checks": ["prompt injection", "schema drift", "hallucinated facts", "fallback behavior"]},
    "verification": {"focus": ["falsification", "independent checks", "counterexamples", "evidence"], "checks": ["unsupported claims", "contradictions", "unverified specifications", "missing tests"]},
    "testing": {"focus": ["unit/integration/system tests", "fixtures", "regression", "hardware-in-loop"], "checks": ["coverage gaps", "flaky tests", "boundary values", "negative cases"]},
    "debugging": {"focus": ["fault isolation", "hypotheses", "instrumentation", "minimal repair"], "checks": ["symptom vs cause", "reproducibility", "regression risk", "new failure modes"]},
    "bom": {"focus": ["part identity", "ratings", "quantities", "alternatives"], "checks": ["obsolete parts", "rating mismatch", "package mismatch", "unavailable assumptions"]},
    "components": {"focus": ["electrical/mechanical/software compatibility", "tradeoffs", "ratings", "availability"], "checks": ["interface mismatch", "derating", "unverified datasheet values", "substitution risk"]},
    "interfaces": {"focus": ["electrical levels", "mechanical connectors", "software contracts", "protocol compatibility"], "checks": ["directionality", "voltage mismatch", "pin conflicts", "timing mismatch"]},
    "communications": {"focus": ["protocol selection", "topology", "throughput", "error handling"], "checks": ["bus contention", "address conflicts", "latency", "loss/retry behavior"]},
    "sensors": {"focus": ["range", "accuracy", "latency", "calibration"], "checks": ["noise", "saturation", "drift", "mounting effects"]},
    "actuators": {"focus": ["torque/force", "speed", "driver compatibility", "thermal limits"], "checks": ["stall current", "startup current", "back-EMF", "mechanical stops"]},
    "kinematics": {"focus": ["coordinate frames", "workspace", "motion geometry", "transform consistency"], "checks": ["singularities", "frame convention errors", "joint limits", "collision"]},
    "dynamics": {"focus": ["forces", "torque", "inertia", "acceleration"], "checks": ["load assumptions", "peak conditions", "stability", "structural margin"]},
    "manufacturing": {"focus": ["process selection", "tolerances", "inspection", "assembly"], "checks": ["unmanufacturable geometry", "tolerance stack", "tool access", "material process compatibility"]},
    "reliability": {"focus": ["failure modes", "derating", "serviceability", "robustness"], "checks": ["common-cause failures", "thermal stress", "connector failure", "maintenance assumptions"]},
    "performance": {"focus": ["latency", "throughput", "memory", "compute and energy budgets"], "checks": ["worst-case load", "contention", "thermal throttling", "scaling limits"]},
    "security": {"focus": ["threat modeling", "secret handling", "authorization", "input validation"], "checks": ["credential leakage", "injection", "over-permission", "sensitive project exposure"]},
    "ux": {"focus": ["workflow clarity", "error recovery", "accessibility", "progressive disclosure"], "checks": ["ambiguous states", "lost work", "confusing errors", "offline transitions"]},
    "product": {"focus": ["user outcome", "feature coherence", "acceptance criteria", "operational constraints"], "checks": ["scope creep", "unclear value", "unmeasurable features", "failure experience"]},
    "requirements": {"focus": ["traceability", "acceptance criteria", "constraints", "ambiguity removal"], "checks": ["vague language", "conflicting requirements", "untestable requirements", "missing priorities"]},
    "optimization": {"focus": ["cost", "mass", "power", "complexity tradeoffs"], "checks": ["constraint violations", "local optimum", "hidden costs", "reliability tradeoffs"]},
    "robotics_software": {"focus": ["robot middleware", "behavior trees/state machines", "deterministic loops", "failsafes"], "checks": ["deadlocks", "message loss", "unsafe transitions", "recovery behavior"]},
    "vision": {"focus": ["camera selection", "calibration", "perception pipeline", "latency"], "checks": ["lighting sensitivity", "false positives", "occlusion", "compute budget"]},
    "navigation": {"focus": ["localization", "mapping", "planning", "recovery"], "checks": ["drift", "dynamic obstacles", "map errors", "loss of localization"]},
    "ai_robotics": {"focus": ["confidence estimation", "bounded autonomy", "fallbacks", "deterministic safety"], "checks": ["low-confidence behavior", "distribution shift", "unsafe actions", "sensor disagreement"]},
    "education": {"focus": ["clear explanations", "prerequisites", "build steps", "verification"], "checks": ["hidden assumptions", "unsafe omissions", "unclear terminology", "missing tests"]},
    "release": {"focus": ["reproducibility", "versioning", "artifact integrity", "rollback"], "checks": ["missing dependencies", "configuration drift", "unsigned artifacts", "rollback gaps"]},
    "auditor": {"focus": ["cross-domain contradiction hunting", "evidence", "risk prioritization", "approval gates"], "checks": ["specialist disagreement", "unsupported confidence", "missing evidence", "unsafe approval"]},
    "lead": {"focus": ["evidence-weighted synthesis", "tradeoff resolution", "requirements coverage", "final approval gate"], "checks": ["critical contradictions", "unresolved high-risk items", "false certainty", "test completeness"]},
}

DEFAULT_PACK = {"focus": ["requirements", "correctness", "testability"], "checks": ["assumptions", "edge cases", "verification"]}

def reasoning_pack(domain: str) -> dict[str, object]:
    return REASONING_PACKS.get(domain, DEFAULT_PACK)


def enhanced_prompt(agent, idea: str, context: str = "") -> str:
    pack = reasoning_pack(agent.domain)
    return f"""You are {agent.name}, a specialist inside RoboLab-X's multi-agent engineering pipeline.\n\nMISSION: {agent.mission}\nRESPONSIBILITY: {agent.responsibility}\nRISK LEVEL: {agent.risk_level}\nREQUIRED OUTPUTS: {', '.join(agent.outputs)}\n\nREASONING FOCUS: {', '.join(pack['focus'])}\nADVERSARIAL CHECKS: {', '.join(pack['checks'])}\n\nRules:\n1. Distinguish user facts, verified facts, assumptions and estimates.\n2. Do not invent datasheet values, measurements, pinouts, certifications or test results.\n3. Identify missing information before making high-confidence decisions.\n4. Check interfaces with adjacent domains.\n5. Give concrete acceptance tests and failure behavior.\n6. If evidence is insufficient, say exactly what must be verified.\n7. Prefer the simplest design that satisfies the stated constraints.\n\nPROJECT IDEA:\n{idea}\n\nSHARED CONTEXT:\n{context}\n\nReturn structured engineering work with: summary, decisions, assumptions, artifacts, risks, verification_checks, conflicts, unresolved_questions, and next_steps."""
