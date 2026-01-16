import pytest
from dataclasses import dataclass
from typing import List
from path_feasibility import PathStep, PathFeasibilityReport
from output_gate import *

@dataclass
class MockPathFeasibilityReport:
    feasible: bool
    blocked_steps: List[str]
    risky_steps: List[str]
    notes: List[str]

def test_output_allowed_when_all_passed():
    report = MockPathFeasibilityReport(
        feasible=True,
        blocked_steps=[],
        risky_steps=[],
        notes=[]
    )
    gate = OutputGate(report)
    out_report = gate.check_output()

    assert out_report.allowed is True
    assert out_report.blocked_steps == []
    assert out_report.risky_steps == []
    assert out_report.notes == []

def test_output_blocked_due_to_blocked_steps():
    report = MockPathFeasibilityReport(
        feasible=False,
        blocked_steps=["s1", "s2"],
        risky_steps=[],
        notes=["Step s1 missing evidence", "Step s2 blocked by dependency"]
    )
    gate = OutputGate(report)
    out_report = gate.check_output()

    assert out_report.allowed is False
    assert out_report.blocked_steps == ["s1", "s2"]
    assert out_report.risky_steps == []
    assert "blocked due to blocked steps: s1, s2" in out_report.notes[0]
    assert "Step s1 missing evidence" in out_report.notes
    assert "Step s2 blocked by dependency" in out_report.notes

def test_output_blocked_due_to_risky_steps():
    report = MockPathFeasibilityReport(
        feasible=True,
        blocked_steps=[],
        risky_steps=["s3"],
        notes=["Step s3 low confidence"]
    )
    gate = OutputGate(report)
    out_report = gate.check_output()

    assert out_report.allowed is False
    assert out_report.blocked_steps == []
    assert out_report.risky_steps == ["s3"]
    assert "blocked due to risky steps: s3" in out_report.notes[0]
    assert "Step s3 low confidence" in out_report.notes

def test_output_blocked_due_to_both_blocked_and_risky():
    report = MockPathFeasibilityReport(
        feasible=False,
        blocked_steps=["s1"],
        risky_steps=["s2"],
        notes=["Step s1 missing evidence", "Step s2 low confidence"]
    )
    gate = OutputGate(report)
    out_report = gate.check_output()

    assert out_report.allowed is False
    assert out_report.blocked_steps == ["s1"]
    assert out_report.risky_steps == ["s2"]
    assert any("blocked due to blocked steps: s1" in note for note in out_report.notes)
    assert any("blocked due to risky steps: s2" in note for note in out_report.notes)
    assert "Step s1 missing evidence" in out_report.notes
    assert "Step s2 low confidence" in out_report.notes
