import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from data_state import DataState
import pytest
class TestDataState:

    def test_verification_failure_refuses_state(self):
            state = DataState(raw_data={"x": 1})
            state.verify_data(
                labels_align=False,
                data_complete=True
            )

            assert state.refused is True
            assert state.refusal_reason == "Labels do not align with inputs"
            assert state.verified_data is None

    def test_verification_is_final(self):
            state = DataState(raw_data={"x": 1})
            state.verify_data(True, data_complete=True)
            first_verified = state.verified_data
            state.verify_data(labels_align=True, data_complete=True)

            assert state.refused is False
            assert state.verified_data == first_verified
            assert "Data verified successfully" in state.logs

    def test_refusal_blocks_downstream_usage(self):
            import pytest

            state = DataState(raw_data={"x": 1})
            state.verify_data(labels_align=False, data_complete=True)
            def downstream_uses_data(data_state):
                    data_state.assert_trust()
                    return data_state.verified_data
            with pytest.raises(RuntimeError) as excinfo:
                    downstream_uses_data(state)
            assert "Refusal reason: Labels do not align with inputs" in str(excinfo.value)