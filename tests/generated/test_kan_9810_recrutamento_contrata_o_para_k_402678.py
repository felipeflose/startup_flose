"""
Pytest unit test suite for HR Onboarding: kan_9810_recrutamento_contrata_o_para_k_402678.
"""
import pytest
from flose.solutions.kan_9810_recrutamento_contrata_o_para_k_402678 import Kan9810RecrutamentoContrataOParaK402678Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9810RecrutamentoContrataOParaK402678Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
