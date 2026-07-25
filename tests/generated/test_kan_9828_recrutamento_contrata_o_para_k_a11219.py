"""
Pytest unit test suite for HR Onboarding: kan_9828_recrutamento_contrata_o_para_k_a11219.
"""
import pytest
from flose.solutions.kan_9828_recrutamento_contrata_o_para_k_a11219 import Kan9828RecrutamentoContrataOParaKA11219Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9828RecrutamentoContrataOParaKA11219Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
