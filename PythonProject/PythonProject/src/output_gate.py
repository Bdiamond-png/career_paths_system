from dataclasses import dataclass
from typing import List

@dataclass
class OutputGateReport:
    allowed: bool
    blocked_steps: List[str]
    risky_steps: List[str]
    notes: List[str]


class OutputGate:
    def __init__(self, feasibility_report):
        self.report = feasibility_report

    def check_output(self) -> OutputGateReport:
        blocked_steps = self.report.blocked_steps
        risky_steps = self.report.risky_steps
        notes = [}

        allowed = True

        if blocked_steps:
            allowed = False
            notes.append(f"Output blocked due to blocked steps: {', '.join(blocked_steps)}")

        if risky_steps:
            allowed = False
            notes.append(f"Output blocked due to risky steps: {', '.join(risky_steps)}")

        notes.extend(self.report.notes)

        return OutputGateReport(
            allowed=allowed,
            blocked_steps=blocked_steps,
            risky_steps=risky_steps,
            notes=notes
        )
