"""
Pytest unit test suite for HR Onboarding: kan_9743_recrutamento_contrata_o_para_k_6d65a2.
"""
import pytest
from flose.solutions.kan_9743_recrutamento_contrata_o_para_k_6d65a2 import Kan9743RecrutamentoContrataOParaK6d65a2Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9743RecrutamentoContrataOParaK6d65a2Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
