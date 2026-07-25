"""
Pytest unit test suite for HR Onboarding: kan_9730_recrutamento_contrata_o_para_k_91436d.
"""
import pytest
from flose.solutions.kan_9730_recrutamento_contrata_o_para_k_91436d import Kan9730RecrutamentoContrataOParaK91436dSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9730RecrutamentoContrataOParaK91436dSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
