"""
Pytest unit test suite for HR Onboarding: kan_9911_recrutamento_contrata_o_para_k_e0a77b.
"""
import pytest
from flose.solutions.kan_9911_recrutamento_contrata_o_para_k_e0a77b import Kan9911RecrutamentoContrataOParaKE0a77bSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9911RecrutamentoContrataOParaKE0a77bSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
