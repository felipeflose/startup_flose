"""
Pytest unit test suite for HR Onboarding: kan_9743_recrutamento_contrata_o_para_k_b2253e.
"""
import pytest
from flose.solutions.kan_9743_recrutamento_contrata_o_para_k_b2253e import Kan9743RecrutamentoContrataOParaKB2253eSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9743RecrutamentoContrataOParaKB2253eSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
