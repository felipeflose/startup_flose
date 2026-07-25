"""
Pytest unit test suite for HR Onboarding: kan_9832_recrutamento_contrata_o_para_k_194b51.
"""
import pytest
from flose.solutions.kan_9832_recrutamento_contrata_o_para_k_194b51 import Kan9832RecrutamentoContrataOParaK194b51Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9832RecrutamentoContrataOParaK194b51Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
