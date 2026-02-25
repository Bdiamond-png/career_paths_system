from base_state import BaseState

class DataState(BaseState):
    def __init__(self, raw_data):
        super().__init__()
        self.raw_data = raw_data
        self.verified_data = None


    def load_data(self):
        self.log("Loading raw data")
        return self.raw_data


    def verify_data(self, labels_align, data_complete):
        self.check_invariant(labels_align, "Labels do not align with inputs")
        self.check_invariant(data_complete, "Data is incomplete")

        if not self.refused:
            self.verified_data = self.raw_data
            self.log("Data verified successfully")