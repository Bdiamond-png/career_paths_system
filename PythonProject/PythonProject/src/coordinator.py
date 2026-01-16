from typing import List, Optional
from base_state import *
from data_state import *
from evidence_mapping import *
from justification_gate import *
from path_feasibility import *
from output_gate import *
from evaluation import *
class Coordinator:

    def __init__(self, raw_data, evidence_bindings, path_steps, ledger):
        self.raw_data = raw_data
        self.evidence_bindings = evidence_bindings
        self.path_steps = path_steps
        self.ledger = ledger

        self.data_state: Optional[DataState] = None
        self.path_report: Optional[PathFeasibilityReport] = None
        self.output_report: Optional[OutputGateReport] = None
        self.final_evaluation: Optional[EvaluationReport] = None

    def run(self) -> EvaluationReport:
        # Step 1: Load and verify data
        self.data_state = DataState(self.raw_data)
        self.data_state.load_data()

        labels_align = True
        data_complete = True
        self.data_state.verify_data(labels_align, data_complete)

        if self.data_state.refused:
            # Data verification failed
            notes = list(self.data_state.logs)
            self.final_evaluation = EvaluationReport(
                status="FAILED",
                blocked_steps=[],
                risky_steps=[],
                notes=notes
            )
            return self.final_evaluation

        trust_states = []
        for binding in self.evidence_bindings:
            trust_state = JustificationGate.justify(binding)
            trust_states.append(trust_state)

            if not trust_state.trusted:
                self.data_state.log(f"Evidence refused: {trust_state.refusal_reason}")

        self.path_report = PathFeasibilityChecker(self.path_steps, self.ledger).check()

        self.output_report = OutputGate(self.path_report).check_output()

        self.final_evaluation = Evaluation(self.path_report, self.output_report).evaluate()

        return self.final_evaluation

    def get_logs(self) -> List[str]:
        logs = []
        if self.data_state:
            logs.extend(self.data_state.logs)
        if self.path_report:
            logs.extend(self.path_report.notes)
        if self.output_report:
            logs.extend(self.output_report.notes)
        return logs