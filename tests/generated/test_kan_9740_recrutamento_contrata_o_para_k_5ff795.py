"""
Pytest unit test suite for HR Onboarding: kan_9740_recrutamento_contrata_o_para_k_5ff795.
"""
import pytest
from flose.solutions.kan_9740_recrutamento_contrata_o_para_k_5ff795 import Kan9740RecrutamentoContrataOParaK5ff795Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9740RecrutamentoContrataOParaK5ff795Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
