"""
Pytest unit test suite for HR Onboarding: kan_9718_recrutamento_contrata_o_para_k_fc604c.
"""
import pytest
from flose.solutions.kan_9718_recrutamento_contrata_o_para_k_fc604c import Kan9718RecrutamentoContrataOParaKFc604cSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9718RecrutamentoContrataOParaKFc604cSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
