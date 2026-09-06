from dataclasses import dataclass

@dataclass(frozen=True)
class Specialist:
    id: str
    name: str
    domain: str
    responsibility: str

DOMAINS = [
    ("systems", "Systems Architect", "requirements, interfaces, architecture"),
    ("electronics", "Electronics Engineer", "analog and digital electronics"),
    ("power", "Power Systems Engineer", "power budgets, rails, current paths"),
    ("embedded", "Embedded Engineer", "MCU firmware and peripherals"),
    ("firmware", "Firmware Reviewer", "firmware correctness and reliability"),
    ("robotics", "Robotics Engineer", "robot mechanisms and control"),
    ("control", "Control Engineer", "feedback, motion and stability"),
    ("mechanical", "Mechanical Engineer", "mechanisms, loads and tolerances"),
    ("cad", "CAD Engineer", "manufacturing-ready geometry specifications"),
    ("simulation", "Simulation Engineer", "test scenarios and simulation plans"),
    ("materials", "Materials Specialist", "materials and component suitability"),
    ("safety", "Safety Engineer", "hazards, limits and safe operation"),
    ("software", "Software Architect", "software structure and interfaces"),
    ("python", "Python Engineer", "Python automation and tooling"),
    ("cpp", "C++ Engineer", "C/C++ embedded implementation"),
    ("mobile", "Mobile Engineer", "Android client architecture"),
    ("backend", "Backend Engineer", "API and service architecture"),
    ("data", "Data Engineer", "project schemas and persistence"),
    ("ai", "AI Systems Engineer", "model routing and structured generation"),
    ("verification", "Verification Engineer", "independent requirement checks"),
    ("testing", "Test Engineer", "test coverage and regression strategy"),
    ("debugging", "Debug Engineer", "fault isolation and repair planning"),
    ("documentation", "Technical Writer", "clear engineering documentation"),
    ("bom", "BOM Specialist", "bill of materials completeness"),
    ("components", "Component Specialist", "component selection constraints"),
    ("interfaces", "Interface Engineer", "electrical and software interfaces"),
    ("communications", "Communications Engineer", "UART, I2C, SPI, CAN and wireless interfaces"),
    ("sensors", "Sensor Engineer", "sensor selection and integration"),
    ("actuators", "Actuator Engineer", "motors, servos and actuator interfaces"),
    ("kinematics", "Kinematics Engineer", "geometry and motion relationships"),
    ("dynamics", "Dynamics Engineer", "forces, motion and system behavior"),
    ("manufacturing", "Manufacturing Engineer", "fabrication and assembly constraints"),
    ("reliability", "Reliability Engineer", "failure modes and robustness"),
    ("performance", "Performance Engineer", "latency, throughput and resource budgets"),
    ("security", "Security Engineer", "secure API and project handling"),
    ("ux", "UX Engineer", "professional engineering workflow"),
    ("product", "Product Engineer", "feature coherence and user outcomes"),
    ("requirements", "Requirements Analyst", "acceptance criteria and traceability"),
    ("optimization", "Optimization Engineer", "cost, size and efficiency tradeoffs"),
    ("robotics_software", "Robotics Software Engineer", "robotics middleware and behavior"),
    ("vision", "Computer Vision Specialist", "camera and vision pipeline planning"),
    ("navigation", "Navigation Specialist", "localization and path planning"),
    ("ai_robotics", "AI Robotics Specialist", "AI-assisted perception and autonomy"),
    ("education", "Robotics Educator", "explainable build guidance"),
    ("release", "Release Engineer", "deployment and reproducibility"),
    ("auditor", "Engineering Auditor", "cross-domain audit"),
    ("lead", "Lead Robotics Engineer", "final engineering synthesis"),
]

SPECIALISTS = tuple(
    Specialist(f"agent-{i+1:02d}", name, domain, responsibility)
    for i, (domain, name, responsibility) in enumerate(DOMAINS)
)

assert len(SPECIALISTS) == 48

def specialist_directory() -> list[dict]:
    return [a.__dict__ for a in SPECIALISTS]
