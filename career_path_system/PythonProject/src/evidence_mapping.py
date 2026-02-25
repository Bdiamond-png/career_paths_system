from dataclasses import dataclass
from typing import Any, List, Optional
from justification_gate import Evidence, TrustState


@dataclass(frozen=True)
class EvidenceMappingEntry:
    id: str
    evidence: Evidence


class EvidenceMapping:

    def __init__(self, entries: List[EvidenceMappingEntry]):
        self.entries = {e.id: e for e in entries}

    def get(self, evidence_id: str) -> Optional[Evidence]:
        return self.entries.get(evidence_id).evidence if evidence_id in self.entries else None

    def validate(self, evidence_id: str) -> TrustState:
        entry = self.entries.get(evidence_id)
        if not entry:
            return TrustState(trusted=False, refusal_reason=f"Missing evidence: {evidence_id}")
        ev = entry.evidence
        if ev.payload is None:
            return TrustState(trusted=False, refusal_reason=f"Evidence payload missing for {evidence_id}")
        if not isinstance(ev.payload, dict):
            return TrustState(trusted=False, refusal_reason=f"Evidence payload unstructured for {evidence_id}")
        if len(ev.payload) == 0:
            return TrustState(trusted=False, refusal_reason=f"Evidence payload empty for {evidence_id}")
        return TrustState(trusted=True, verified_data=ev.payload)
