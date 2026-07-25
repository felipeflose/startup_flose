"""
Pytest unit test suite for HR Onboarding: kan_9793_recrutamento_contrata_o_para_k_dc5a24.
"""
import pytest
from flose.solutions.kan_9793_recrutamento_contrata_o_para_k_dc5a24 import Kan9793RecrutamentoContrataOParaKDc5a24Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9793RecrutamentoContrataOParaKDc5a24Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
