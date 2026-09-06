from dataclasses import dataclass

@dataclass(frozen=True)
class Specialist:
    id: int
    name: str
    domain: str
    mission: str

_DOMAINS = [
    ("Systems Architect", "architecture", "Define requirements, interfaces, constraints, and system decomposition."),
    ("Electronics Engineer", "electronics", "Design and review electronic subsystems and signal paths."),
    ("Embedded Engineer", "embedded", "Design firmware architecture, timing, IO, and device behavior."),
    ("Robotics Engineer", "robotics", "Plan mechanisms, sensing, actuation, and robot behaviors."),
    ("Control Engineer", "control", "Reason about feedback, stability, motion, and control strategies."),
    ("Power Engineer", "power", "Validate rails, current budgets, protection, and power sequencing."),
    ("PCB Engineer", "pcb", "Review board-level connectivity, grounding, decoupling, and layout constraints."),
    ("Mechanical Engineer", "mechanical", "Translate requirements into mechanisms, dimensions, and materials."),
    ("CAD Engineer", "cad", "Produce CAD-ready specifications, dimensions, assemblies, and constraints."),
    ("Simulation Engineer", "simulation", "Create simulation plans, test cases, and expected behavior."),
    ("Firmware Engineer", "firmware", "Generate maintainable embedded firmware plans and implementation details."),
    ("Software Engineer", "software", "Design application software, APIs, state, persistence, and integration."),
    ("Python Engineer", "python", "Design reliable Python automation, tooling, and services."),
    ("C++ Engineer", "cpp", "Design robust C++ implementations for embedded and robotics workloads."),
    ("Arduino Engineer", "arduino", "Translate robotics requirements into Arduino-compatible implementations."),
    ("ESP32 Engineer", "esp32", "Design ESP32 networking, peripherals, and real-time behavior."),
    ("Sensor Specialist", "sensors", "Select and validate sensor interfaces, ranges, and failure modes."),
    ("Actuator Specialist", "actuators", "Select and validate motors, servos, drivers, and actuation requirements."),
    ("Communication Engineer", "communications", "Design UART, I2C, SPI, CAN, BLE, Wi-Fi, and protocol interfaces."),
    ("Computer Vision Engineer", "vision", "Design camera and vision pipelines appropriate to the project."),
    ("AI/ML Engineer", "ml", "Plan ML components, inference boundaries, evaluation, and fallbacks."),
    ("NLP Engineer", "nlp", "Interpret natural-language engineering requirements and normalize intent."),
    ("Security Engineer", "security", "Threat-model the system and identify practical security controls."),
    ("Safety Engineer", "safety", "Identify hazards, safeguards, fail-safe states, and safe operating limits."),
    ("Test Engineer", "testing", "Create verification matrices, edge cases, and acceptance criteria."),
    ("QA Engineer", "qa", "Review outputs for correctness, consistency, and regression risk."),
    ("Compiler Specialist", "compiler", "Check generated code for structural, dependency, and build issues."),
    ("Debugger", "debugging", "Diagnose failures and propose minimal, testable repairs."),
    ("Requirements Engineer", "requirements", "Turn user goals into measurable engineering requirements."),
    ("BOM Specialist", "bom", "Build a practical bill of materials and identify missing dependencies."),
    ("Component Researcher", "components", "Evaluate component fit, specifications, and compatibility."),
    ("Integration Engineer", "integration", "Validate boundaries between software, firmware, electronics, and mechanics."),
    ("Manufacturing Engineer", "manufacturing", "Review manufacturability, assembly, tolerances, and serviceability."),
    ("Thermal Engineer", "thermal", "Assess heat generation, dissipation, and thermal constraints."),
    ("Reliability Engineer", "reliability", "Identify likely failure points and improve robustness."),
    ("Performance Engineer", "performance", "Optimize latency, throughput, memory, and power where relevant."),
    ("Documentation Engineer", "documentation", "Create clear technical documentation and reproducible build instructions."),
    ("UX Engineer", "ux", "Design intuitive engineering workflows and useful mobile interactions."),
    ("Mobile Engineer", "mobile", "Design the Flutter Android client and its API integration."),
    ("Backend Engineer", "backend", "Design secure, scalable API services and job orchestration."),
    ("Cloud Engineer", "cloud", "Design deployment, observability, scaling, and recovery strategies."),
    ("Data Engineer", "data", "Design project schemas, persistence, migrations, and data validation."),
    ("Cost Engineer", "cost", "Estimate component, inference, hosting, and operational cost drivers."),
    ("Product Engineer", "product", "Turn engineering capability into a coherent, usable product workflow."),
    ("Localization Engineer", "localization", "Design internationalization and engineering terminology support."),
    ("Final Reviewer", "review", "Perform a final cross-domain review and flag unresolved contradictions."),
]

SPECIALISTS = tuple(Specialist(i + 1, *item) for i, item in enumerate(_DOMAINS))
assert len(SPECIALISTS) == 48


def list_specialists() -> list[dict]:
    return [s.__dict__ for s in SPECIALISTS]
