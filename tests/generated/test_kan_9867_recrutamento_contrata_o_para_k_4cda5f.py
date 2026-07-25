"""
Pytest unit test suite for HR Onboarding: kan_9867_recrutamento_contrata_o_para_k_4cda5f.
"""
import pytest
from flose.solutions.kan_9867_recrutamento_contrata_o_para_k_4cda5f import Kan9867RecrutamentoContrataOParaK4cda5fSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9867RecrutamentoContrataOParaK4cda5fSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
