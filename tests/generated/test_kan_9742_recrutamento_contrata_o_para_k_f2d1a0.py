"""
Pytest unit test suite for HR Onboarding: kan_9742_recrutamento_contrata_o_para_k_f2d1a0.
"""
import pytest
from flose.solutions.kan_9742_recrutamento_contrata_o_para_k_f2d1a0 import Kan9742RecrutamentoContrataOParaKF2d1a0Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9742RecrutamentoContrataOParaKF2d1a0Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
