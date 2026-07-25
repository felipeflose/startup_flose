"""
Pytest unit test suite for HR Onboarding: kan_9794_recrutamento_contrata_o_para_k_eaea5e.
"""
import pytest
from flose.solutions.kan_9794_recrutamento_contrata_o_para_k_eaea5e import Kan9794RecrutamentoContrataOParaKEaea5eSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9794RecrutamentoContrataOParaKEaea5eSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
