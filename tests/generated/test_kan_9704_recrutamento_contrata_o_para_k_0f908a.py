"""
Pytest unit test suite for HR Onboarding: kan_9704_recrutamento_contrata_o_para_k_0f908a.
"""
import pytest
from flose.solutions.kan_9704_recrutamento_contrata_o_para_k_0f908a import Kan9704RecrutamentoContrataOParaK0f908aSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9704RecrutamentoContrataOParaK0f908aSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
