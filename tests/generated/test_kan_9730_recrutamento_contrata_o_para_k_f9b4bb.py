"""
Pytest unit test suite for HR Onboarding: kan_9730_recrutamento_contrata_o_para_k_f9b4bb.
"""
import pytest
from flose.solutions.kan_9730_recrutamento_contrata_o_para_k_f9b4bb import Kan9730RecrutamentoContrataOParaKF9b4bbSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9730RecrutamentoContrataOParaKF9b4bbSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
