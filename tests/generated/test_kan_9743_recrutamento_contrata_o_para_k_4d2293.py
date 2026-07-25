"""
Pytest unit test suite for HR Onboarding: kan_9743_recrutamento_contrata_o_para_k_4d2293.
"""
import pytest
from flose.solutions.kan_9743_recrutamento_contrata_o_para_k_4d2293 import Kan9743RecrutamentoContrataOParaK4d2293Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9743RecrutamentoContrataOParaK4d2293Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
