"""
Pytest unit test suite for HR Onboarding: kan_9793_recrutamento_contrata_o_para_k_aaf1f8.
"""
import pytest
from flose.solutions.kan_9793_recrutamento_contrata_o_para_k_aaf1f8 import Kan9793RecrutamentoContrataOParaKAaf1f8Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9793RecrutamentoContrataOParaKAaf1f8Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
