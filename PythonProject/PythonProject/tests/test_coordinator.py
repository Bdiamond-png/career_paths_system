import pytest
from dataclasses import dataclass
from typing import List

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

@dataclass
class MockEvidence:
    payload: dict
    source: str

@dataclass
class MockClaim:
    description: str

@dataclass
class MockEvidenceBinding:
    claim: MockClaim
    evidence: List[MockEvidence]

def test_coordinator_success():
    # Step 0: raw data
    raw_data = {"field1": 1, "field2": 2}

    evidence_binding = MockEvidenceBinding(
        claim=MockClaim(description="Data is complete and aligned"),
        evidence=[MockEvidence(payload={"field1": 1, "field2": 2}, source="source1")]
    )

    ledger = MockLedger(entries=[
        MockLedgerEntry(id="step1", trusted=True, refused=False, status="PASSED", confidence_score=0.9),
        MockLedgerEntry(id="step2", trusted=True, refused=False, status="PASSED", confidence_score=0.95)
    ])

    from path_feasibility import PathStep  # adjust import as needed
    path_steps = [
        PathStep(id="step1", description="Step 1", required_evidence_ids=[]),
        PathStep(id="step2", description="Step 2", dependencies=["step1"])
    ]

    from coordinator import Coordinator  # adjust import
    coordinator = Coordinator(
        raw_data=raw_data,
        evidence_bindings=[evidence_binding],
        path_steps=path_steps,
        ledger=ledger
    )

    final_report = coordinator.run()

    # --- Assertions ---
    assert final_report.status == "SUCCESS"
    assert final_report.blocked_steps == []
    assert final_report.risky_steps == []
    assert any("Evaluation: path fully feasible" in note for note in final_report.notes)

    logs = coordinator.get_logs()
    assert any("Data verified successfully" in log for log in logs)

