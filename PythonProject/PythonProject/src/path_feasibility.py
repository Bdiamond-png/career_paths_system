from base_state import BaseState


class PathFeasibility(BaseState):
    def __init__(self, confidence_score, verified_evidence):
        super().__init__()
        self.confidence_score = confidence_score
        self.verified_evidence = verified_evidence
        self.candidate_paths = []
        self.refused = False

    def generate_path(self):
        if self.confidence_score < 0.5 or not self.verified_evidence:
            self.refused = True
            return "Refused: not enough evidence or confidence too low"

        for i, evidence in enumerate(self.verified_evidence, start=1):
            path = f'candidate_paths_{i} based on {evidence}'
            self.candidate_paths.append(path)

        return self.candidate_paths