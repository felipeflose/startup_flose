"""
Pytest unit test suite for HR Onboarding: kan_9781_recrutamento_contrata_o_para_k_1a8df5.
"""
import pytest
from flose.solutions.kan_9781_recrutamento_contrata_o_para_k_1a8df5 import Kan9781RecrutamentoContrataOParaK1a8df5Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9781RecrutamentoContrataOParaK1a8df5Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
