"""
Pytest unit test suite for HR Onboarding: kan_9757_recrutamento_contrata_o_para_k_03a282.
"""
import pytest
from flose.solutions.kan_9757_recrutamento_contrata_o_para_k_03a282 import Kan9757RecrutamentoContrataOParaK03a282Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9757RecrutamentoContrataOParaK03a282Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
