"""
Pytest unit test suite for HR Onboarding: kan_9770_recrutamento_contrata_o_para_k_d5f1c1.
"""
import pytest
from flose.solutions.kan_9770_recrutamento_contrata_o_para_k_d5f1c1 import Kan9770RecrutamentoContrataOParaKD5f1c1Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9770RecrutamentoContrataOParaKD5f1c1Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
