from dataclasses import dataclass
from typing import Any, List, Optional, Dict

@dataclass
class PathStep:
    id: str
    description: str
    required_evidence_ids: Optional[List[str]] = None
    dependencies: Optional[List[str]] = None

@dataclass
class PathFeasibilityReport:
    feasible: bool
    blocked_steps: List[str]
    risky_steps: List[str]
    notes: List[str]

class PathFeasibilityChecker:
    def __init__(self, path: List[PathStep], ledger: Any):
        self.path = path
        self.ledger = ledger

    def check_dependencies(self, step: PathStep, step_status: dict):
        for dep_id in step.dependencies or []:
            dep_entry = self.ledger.get_entry(dep_id)
            dep_status = dep_entry.status if dep_entry else step_status.get(dep_id)

            if dep_status != "PASSED":
                return dep_id
            return None

    def check(self) -> PathFeasibilityReport:
        blocked: List[str] = []
        risky: List[str] = []
        notes: List[str] = []

        step_status: Dict[str, str] = {}

        for step in self.path:
            blocked_dep = self.check_dependencies(step, step_status)
            if blocked_dep:
                blocked.append(step.id)
                notes.append(f"Step {step.id} is blocked by dependency {blocked_dep}")
                step_status[step.id] = "BLOCKED"
                continue

            if step.id in blocked:
                continue
            if step.required_evidence_ids:
                for ev_id in step.required_evidence_ids:
                    ev_entry = self.ledger.get_entry(ev_id)
                    if not ev_entry:
                        blocked.append(step.id)
                        notes.append(f"Step {step.id} blocked: missing evidence {ev_id}")
                        step_status[step.id] = "BLOCKED"
                        break
                    if ev_entry.trusted is False:
                        blocked.append(step.id)
                        notes.append(f"Step {step.id} blocked: untrusted evidence {ev_id}")
                        step_status[step.id] = "BLOCKED"
                        break
                    if hasattr(ev_entry, "confidence_score") and ev_entry.confidence_score < 0.5:
                        risky.append(step.id)
                        notes.append(f"Step {step.id} risky: low confidence in evidence {ev_id}")
            if step.id not in step_status:
                step_status[step.id] = "PASSED"

        feasible = len(blocked) == 0 and len(risky) == 0

        return PathFeasibilityReport(
            feasible=feasible,
            blocked_steps=blocked,
            risky_steps=risky,
            notes=notes
        )