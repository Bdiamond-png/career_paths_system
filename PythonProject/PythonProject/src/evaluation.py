from dataclasses import dataclass
from typing import List, Optional

@dataclass
class EvaluationReport:
    status: str  # SUCCESS, RISKY, FAILED
    blocked_steps: List[str]
    risky_steps: List[str]
    notes: List[str]

class Evaluation:
    def __init__(self, path_report, output_report: Optional = None):
        self.path_report = path_report
        self.output_report = output_report

    def evaluate(self) -> EvaluationReport:
        blocked = self.path_report.blocked_steps
        risky = self.path_report.risky_steps
        notes = list(self.path_report.notes)

        if self.output_report:
            notes.extend(self.output_report.notes)

        if blocked:
            status = "FAILED"
            notes.insert(0, f"Evaluation: path failed due to blocked steps: {', '.join(blocked)}")
        elif risky:
            status = "RISKY"
            notes.insert(0, f"Evaluation: path risky due to low confidence steps: {', '.join(risky)}")
        else:
            status = "SUCCESS"
            notes.insert(0, "Evaluation: path fully feasible with no risks.")

        return EvaluationReport(
            status=status,
            blocked_steps=blocked,
            risky_steps=risky,
            notes=notes
        )