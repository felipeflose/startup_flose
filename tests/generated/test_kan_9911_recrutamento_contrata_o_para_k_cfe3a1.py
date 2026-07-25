"""
Pytest unit test suite for HR Onboarding: kan_9911_recrutamento_contrata_o_para_k_cfe3a1.
"""
import pytest
from flose.solutions.kan_9911_recrutamento_contrata_o_para_k_cfe3a1 import Kan9911RecrutamentoContrataOParaKCfe3a1Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9911RecrutamentoContrataOParaKCfe3a1Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
