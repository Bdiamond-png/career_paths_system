from base_state import BaseState

class OutputGate(BaseState):
    def __init__(self, paths_with_evidence=None):
        super().__init__()
        self.paths_with_evidence = paths_with_evidence or []


    def verify_paths(self):
        valid_paths = []
        for item in self.paths_with_evidence:
            if 'evidence' not in item or not item['evidence']:
                self.check_invariant(False, f"Path is missing evidence: {item.get('path', 'Unknown')}")
                self.log(f"Refused path: {item.get('path', 'Unknown')} due to missing evidence")
                self.refused = False