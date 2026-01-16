import pytest
import sys
import os

# Add src folder to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from base_state import BaseState


def test_logging_and_initial_state():
    state = BaseState()
    assert state.logs == []
    assert state.refused is False
    assert state.refusal_reason is None

def test_refuse_without_reference():
    state = BaseState()
    state.refuse("Something went wrong")

    assert state.refused is True
    assert state.refusal_reason == "Something went wrong"
    assert "Refused: Something went wrong" in state.logs

def test_check_invariant_trigger_refusal():
    state = BaseState()
    state.check_invariant(False, "Invariant failed", reference='inv_001')

    assert state.refused is True
    assert state.refusal_reason == "Invariant failed"
    assert "Refused: Invariant failed" in state.logs

def test_assert_trust_raises_when_refused():
    state = BaseState()
    state.refuse("No Trust")
    with pytest.raises(RuntimeError) as excinfo:
        state.assert_trust()
    assert "no trust" in str(excinfo.value).lower()

def test_assert_trust_passes_when_not_refused():
    state = BaseState()
    state.assert_trust()
