from app.agents import SPECIALISTS, specialist_prompt
from app.engineering import build_project, validate_project, synthesize_consensus
from app.evaluation import evaluate_project

def test_has_48_specialists():
    assert len(SPECIALISTS) == 48

def test_specialists_have_real_work_contracts():
    assert all(a.mission and a.outputs and a.responsibility for a in SPECIALISTS)

def test_generation_has_pro_depth():
    project = build_project("Build an ESP32 rover with motors, ultrasonic obstacle detection and battery power", pro=True)
    assert project["analysis"]["specialist_count"] == 48
    assert "power" in project["analysis"]["matched_domains"]
    assert "sensors" in project["analysis"]["matched_domains"]
    assert len(project["specialist_work_orders"]) == 48

def test_validation_and_quality_gate():
    project = build_project("Build a line following robot", pro=False)
    findings = validate_project(project)
    consensus = synthesize_consensus(project, findings)
    quality = evaluate_project(project)
    assert consensus["approval_gate"] == "PASS"
    assert quality["quality_score"] >= 0.8

def test_prompt_is_domain_specific():
    agent = next(a for a in SPECIALISTS if a.domain == "power")
    prompt = specialist_prompt(agent, "12V battery robot")
    assert "Power Systems Engineer" in prompt
    assert "power_budget" in prompt
