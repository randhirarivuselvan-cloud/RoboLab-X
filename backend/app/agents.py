from dataclasses import dataclass

@dataclass(frozen=True)
class Specialist:
    id: str
    name: str
    domain: str
    responsibility: str
    mission: str
    outputs: tuple[str, ...]
    risk_level: str = "medium"

DOMAINS = [
    ("systems", "Systems Architect", "requirements, interfaces, architecture", "Turn an ambiguous idea into a coherent, testable system architecture.", ("requirements", "architecture", "interfaces", "acceptance_tests"), "high"),
    ("electronics", "Electronics Engineer", "analog and digital electronics", "Design electrically consistent signal and power interfaces.", ("schematic", "signal_paths", "component_constraints", "test_points"), "high"),
    ("power", "Power Systems Engineer", "power budgets, rails, current paths", "Size rails, protection and energy paths with explicit margins.", ("power_budget", "rails", "protection", "margin_checks"), "critical"),
    ("embedded", "Embedded Engineer", "MCU firmware and peripherals", "Map hardware capabilities to deterministic firmware architecture.", ("pin_map", "drivers", "state_machine", "timing"), "high"),
    ("firmware", "Firmware Reviewer", "firmware correctness and reliability", "Independently challenge generated firmware for faults and edge cases.", ("review", "faults", "repair_plan", "regression_tests"), "critical"),
    ("robotics", "Robotics Engineer", "robot mechanisms and control", "Translate the goal into a practical robot architecture.", ("robot_architecture", "subsystems", "motion_plan", "integration"), "high"),
    ("control", "Control Engineer", "feedback, motion and stability", "Specify sensing, feedback and control behavior with stability checks.", ("controller", "feedback", "sampling", "stability_tests"), "critical"),
    ("mechanical", "Mechanical Engineer", "mechanisms, loads and tolerances", "Evaluate mechanisms, loads, clearances and structural constraints.", ("mechanism", "loads", "tolerances", "assembly"), "high"),
    ("cad", "CAD Engineer", "manufacturing-ready geometry specifications", "Produce parametric, dimensioned CAD-ready specifications.", ("dimensions", "features", "materials", "manufacturing_notes"), "high"),
    ("simulation", "Simulation Engineer", "test scenarios and simulation plans", "Convert assumptions into repeatable simulation and validation scenarios.", ("scenarios", "parameters", "metrics", "pass_fail"), "high"),
    ("materials", "Materials Specialist", "materials and component suitability", "Check material selection against environment, loads and fabrication.", ("material_choices", "properties", "constraints", "alternatives"), "medium"),
    ("safety", "Safety Engineer", "hazards, limits and safe operation", "Identify hazards, operating limits and protective measures.", ("hazards", "limits", "mitigations", "safe_test_plan"), "critical"),
    ("software", "Software Architect", "software structure and interfaces", "Design maintainable software boundaries, data flow and failure handling.", ("modules", "interfaces", "state", "error_strategy"), "high"),
    ("python", "Python Engineer", "Python automation and tooling", "Build reliable Python tooling with validation and tests.", ("modules", "schemas", "automation", "tests"), "medium"),
    ("cpp", "C++ Engineer", "C/C++ embedded implementation", "Generate portable, resource-aware embedded C/C++ structure.", ("source_layout", "drivers", "memory_plan", "build_flags"), "high"),
    ("mobile", "Mobile Engineer", "Android client architecture", "Design robust Android workflows, networking and offline behavior.", ("screens", "state", "api_client", "offline_strategy"), "high"),
    ("backend", "Backend Engineer", "API and service architecture", "Build secure, observable and scalable service boundaries.", ("routes", "schemas", "security", "observability"), "high"),
    ("data", "Data Engineer", "project schemas and persistence", "Create versioned, migration-friendly engineering project data.", ("schema", "indexes", "migrations", "export"), "medium"),
    ("ai", "AI Systems Engineer", "model routing and structured generation", "Route work to specialists and enforce structured outputs.", ("routing", "schemas", "fallbacks", "evaluation"), "critical"),
    ("verification", "Verification Engineer", "independent requirement checks", "Try to falsify the proposed design instead of agreeing with it.", ("checks", "counterexamples", "severity", "evidence"), "critical"),
    ("testing", "Test Engineer", "test coverage and regression strategy", "Build unit, integration and hardware-in-loop test strategies.", ("test_matrix", "fixtures", "regression", "coverage"), "high"),
    ("debugging", "Debug Engineer", "fault isolation and repair planning", "Trace failures to likely causes and propose bounded repairs.", ("symptoms", "hypotheses", "diagnostics", "repair"), "high"),
    ("documentation", "Technical Writer", "clear engineering documentation", "Turn engineering decisions into reproducible documentation.", ("build_guide", "api_docs", "assumptions", "warnings"), "medium"),
    ("bom", "BOM Specialist", "bill of materials completeness", "Build a procurement-ready bill of materials.", ("parts", "quantities", "specs", "alternatives"), "high"),
    ("components", "Component Specialist", "component selection constraints", "Select components across electrical, mechanical, software and availability constraints.", ("candidate_parts", "constraints", "tradeoffs", "alternatives"), "high"),
    ("interfaces", "Interface Engineer", "electrical and software interfaces", "Resolve interface contracts and incompatibilities.", ("contracts", "levels", "connectors", "compatibility"), "high"),
    ("communications", "Communications Engineer", "UART, I2C, SPI, CAN and wireless interfaces", "Choose and specify reliable communication links.", ("protocol", "rate", "topology", "error_handling"), "high"),
    ("sensors", "Sensor Engineer", "sensor selection and integration", "Match sensors to accuracy, range, timing and environment.", ("sensor_choices", "ranges", "interfaces", "calibration"), "high"),
    ("actuators", "Actuator Engineer", "motors, servos and actuator interfaces", "Match actuators and drivers to loads with safe margins.", ("actuator_choices", "driver", "load", "limits"), "critical"),
    ("kinematics", "Kinematics Engineer", "geometry and motion relationships", "Derive motion geometry, coordinate frames and workspace constraints.", ("frames", "geometry", "workspace", "equations"), "high"),
    ("dynamics", "Dynamics Engineer", "forces, motion and system behavior", "Evaluate forces, inertia, acceleration and dynamic limits.", ("forces", "inertia", "acceleration", "dynamic_limits"), "critical"),
    ("manufacturing", "Manufacturing Engineer", "fabrication and assembly constraints", "Make designs manufacturable with realistic processes and tolerances.", ("process", "tolerances", "assembly", "inspection"), "high"),
    ("reliability", "Reliability Engineer", "failure modes and robustness", "Identify failure modes and improve robustness and serviceability.", ("FMEA", "failure_modes", "derating", "maintenance"), "critical"),
    ("performance", "Performance Engineer", "latency, throughput and resource budgets", "Quantify timing, memory, compute and energy budgets.", ("budgets", "bottlenecks", "benchmarks", "optimization"), "high"),
    ("security", "Security Engineer", "secure API and project handling", "Protect project data, APIs, secrets and untrusted inputs.", ("threat_model", "controls", "validation", "secret_policy"), "critical"),
    ("ux", "UX Engineer", "professional engineering workflow", "Make complex engineering tasks understandable and efficient.", ("workflow", "states", "errors", "accessibility"), "medium"),
    ("product", "Product Engineer", "feature coherence and user outcomes", "Keep features focused on measurable user outcomes.", ("user_story", "workflow", "limits", "acceptance"), "medium"),
    ("requirements", "Requirements Analyst", "acceptance criteria and traceability", "Convert natural language into traceable engineering requirements.", ("requirements", "constraints", "traceability", "acceptance"), "high"),
    ("optimization", "Optimization Engineer", "cost, size and efficiency tradeoffs", "Optimize cost, mass, power and complexity without violating constraints.", ("objectives", "tradeoffs", "pareto_options", "recommendation"), "high"),
    ("robotics_software", "Robotics Software Engineer", "robotics middleware and behavior", "Design robot behaviors, middleware interfaces and deterministic loops.", ("modules", "topics", "behavior", "failsafes"), "high"),
    ("vision", "Computer Vision Specialist", "camera and vision pipeline planning", "Design camera, perception and vision-processing pipelines.", ("camera", "pipeline", "latency", "validation"), "high"),
    ("navigation", "Navigation Specialist", "localization and path planning", "Design localization and navigation with recovery behavior.", ("localization", "planner", "maps", "recovery"), "critical"),
    ("ai_robotics", "AI Robotics Specialist", "AI-assisted perception and autonomy", "Constrain autonomy with deterministic safeguards and fallback behavior.", ("ai_pipeline", "confidence", "fallbacks", "safety"), "critical"),
    ("education", "Robotics Educator", "explainable build guidance", "Explain engineering choices without hiding assumptions or risks.", ("explanation", "steps", "prerequisites", "checks"), "medium"),
    ("release", "Release Engineer", "deployment and reproducibility", "Make builds reproducible, versioned and observable.", ("release_plan", "artifacts", "checksums", "rollback"), "high"),
    ("auditor", "Engineering Auditor", "cross-domain audit", "Perform an adversarial cross-domain audit before approval.", ("audit", "conflicts", "missing_evidence", "approval_gate"), "critical"),
    ("lead", "Lead Robotics Engineer", "final engineering synthesis", "Resolve specialist conflicts and produce the final coherent engineering decision.", ("decision", "tradeoffs", "open_questions", "approval_gate"), "critical"),
]

SPECIALISTS = tuple(Specialist(f"agent-{i+1:02d}", name, domain, responsibility, mission, tuple(outputs), risk) for i, (domain, name, responsibility, mission, outputs, risk) in enumerate(DOMAINS))
assert len(SPECIALISTS) == 48

SYSTEM_PROMPT = """You are a specialist inside RoboLab-X, a professional robotics engineering system. Be precise, skeptical and explicit about assumptions. Never invent measured values, pinouts, part availability or safety guarantees. Separate known facts, estimates and user-supplied constraints. Return actionable engineering work, validation checks, failure modes and unresolved questions. Prefer deterministic, testable designs over vague advice."""

def specialist_prompt(agent: Specialist, idea: str, context: str = "") -> str:
    return f"{SYSTEM_PROMPT}\n\nROLE: {agent.name}\nDOMAIN: {agent.domain}\nRESPONSIBILITY: {agent.responsibility}\nMISSION: {agent.mission}\nREQUIRED OUTPUTS: {', '.join(agent.outputs)}\nRISK LEVEL: {agent.risk_level}\n\nPROJECT:\n{idea}\n\nSHARED CONTEXT:\n{context}\n\nAct independently. Challenge assumptions, identify conflicts with other domains, and make every recommendation verifiable."

def specialist_directory() -> list[dict]:
    return [{**a.__dict__, "outputs": list(a.outputs)} for a in SPECIALISTS]
