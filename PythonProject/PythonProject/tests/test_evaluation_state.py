import pytest
from dataclasses import dataclass
from path_feasibility import PathFeasibilityReport
from output_gate import OutputGateReport
from evaluation import Evaluation, EvaluationReport

@pytest.fixture
def blocked_report():
    return PathFeasibilityReport(
        feasible=False,
        blocked_steps=["s1", "s2"],
        risky_steps=[],
        notes=["Step s1 blocked", "Step s2 blocked"]
    )

@pytest.fixture
def risky_report():
    return PathFeasibilityReport(
        feasible=True,
        blocked_steps=[],
        risky_steps=["s1"],
        notes=["Step s1 risky"]
    )

@pytest.fixture
def success_report():
    return PathFeasibilityReport(
        feasible=True,
        blocked_steps=[],
        risky_steps=[],
        notes=[]
    )

def test_evaluation_failed(blocked_report):
    evaluator = Evaluation(blocked_report)
    report = evaluator.evaluate()

    assert report.status == "FAILED"
    assert "s1" in report.blocked_steps
    assert report.notes[0].startswith("Evaluation: path failed")

def test_evaluation_risky(risky_report):
    evaluator = Evaluation(risky_report)
    report = evaluator.evaluate()

    assert report.status == "RISKY"
    assert "s1" in report.risky_steps
    assert report.notes[0].startswith("Evaluation: path risky")

def test_evaluation_success(success_report):
    evaluator = Evaluation(success_report)
    report = evaluator.evaluate()

    assert report.status == "SUCCESS"
    assert report.blocked_steps == []
    assert report.risky_steps == []
    assert report.notes[0].startswith("Evaluation: path fully feasible")

def test_evaluation_with_output_gate(success_report):
    output_notes = ["OutputGate: success confirmed"]
    output_report = OutputGateReport(
        allowed=True,
        blocked_steps=[],
        risky_steps=[],
        notes=output_notes
    )

    evaluator = Evaluation(success_report, output_report=output_report)
    report = evaluator.evaluate()

    assert report.status == "SUCCESS"
    assert "OutputGate: success confirmed" in report.notes