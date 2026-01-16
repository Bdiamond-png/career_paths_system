import pytest
from path_feasibility import *
from dataclasses import dataclass
from typing import List

# Mock ledger entry for testing
@dataclass
class MockLedgerEntry:
    id: str
    trusted: bool
    refused: bool
    status: str
    confidence_score: float

class MockLedger:
    def __init__(self, entries: List[MockLedgerEntry]):
        self.entries = {e.id: e for e in entries}

    def get_entry(self, entry_id):
        return self.entries.get(entry_id)

def test_fully_feasible_path():
    ledger = MockLedger(entries=[
        MockLedgerEntry(id="e1", trusted=True, refused=False, status="PASSED", confidence_score=0.9),
        MockLedgerEntry(id="e2", trusted=True, refused=False, status="PASSED", confidence_score=0.95),
    ])
    steps = [
        PathStep(id="s1", description="Step 1", required_evidence_ids=["e1"]),
        PathStep(id="s2", description="Step 2", required_evidence_ids=["e2"], dependencies=["s1"]),
    ]
    checker = PathFeasibilityChecker(steps, ledger)
    report = checker.check()

    assert report.feasible is True
    assert report.blocked_steps == []
    assert report.risky_steps == []
    assert len(report.notes) == 0

def test_blocked_missing_evidence():
    ledger = MockLedger(entries=[])
    steps = [PathStep(id="s1", description="Step 1", required_evidence_ids=["e1"])]
    checker = PathFeasibilityChecker(steps, ledger)
    report = checker.check()

    assert report.feasible is False
    assert "s1" in report.blocked_steps
    assert any("missing evidence e1" in note for note in report.notes)

def test_blocked_refused_evidence():
    ledger = MockLedger(entries=[
        MockLedgerEntry(id="e1", trusted=False, refused=True, status="FAILED", confidence_score=0.0)
    ])
    steps = [PathStep(id="s1", description="Step 1", required_evidence_ids=["e1"])]
    checker = PathFeasibilityChecker(steps, ledger)
    report = checker.check()

    assert report.feasible is False
    assert "s1" in report.blocked_steps
    assert any("untrusted evidence e1" in note for note in report.notes)

def test_blocked_failed_dependency():
    ledger = MockLedger(entries=[
        MockLedgerEntry(id="e1", trusted=True, refused=False, status="PASSED", confidence_score=0.9)
    ])
    steps = [
        PathStep(id="s1", description="Step 1", required_evidence_ids=["e1"]),
        PathStep(id="s2", description="Step 2", dependencies=["s1"])
    ]
    # simulate s1 not passed in ledger
    ledger.entries["s1"] = MockLedgerEntry(id="s1", trusted=True, refused=False, status="FAILED", confidence_score=1.0)
    checker = PathFeasibilityChecker(steps, ledger)
    report = checker.check()

    assert report.feasible is False
    assert "s2" in report.blocked_steps
    assert any("blocked by dependency s1" in note for note in report.notes)

def test_risky_low_confidence():
    ledger = MockLedger(entries=[
        MockLedgerEntry(id="e1", trusted=True, refused=False, status="PASSED", confidence_score=0.3)
    ])
    steps = [PathStep(id="s1", description="Step 1", required_evidence_ids=["e1"])]
    checker = PathFeasibilityChecker(steps, ledger)
    report = checker.check()

    assert report.feasible is False
    assert "s1" in report.risky_steps
    assert any("low confidence in evidence e1" in note for note in report.notes)
