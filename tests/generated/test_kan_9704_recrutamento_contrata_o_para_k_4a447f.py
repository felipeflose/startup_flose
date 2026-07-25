"""
Pytest unit test suite for HR Onboarding: kan_9704_recrutamento_contrata_o_para_k_4a447f.
"""
import pytest
from flose.solutions.kan_9704_recrutamento_contrata_o_para_k_4a447f import Kan9704RecrutamentoContrataOParaK4a447fSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9704RecrutamentoContrataOParaK4a447fSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
