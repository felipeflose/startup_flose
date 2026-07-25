"""
Pytest unit test suite for HR Onboarding: kan_9808_recrutamento_contrata_o_para_k_af2b09.
"""
import pytest
from flose.solutions.kan_9808_recrutamento_contrata_o_para_k_af2b09 import Kan9808RecrutamentoContrataOParaKAf2b09Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9808RecrutamentoContrataOParaKAf2b09Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
