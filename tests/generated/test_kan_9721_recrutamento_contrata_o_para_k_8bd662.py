"""
Pytest unit test suite for HR Onboarding: kan_9721_recrutamento_contrata_o_para_k_8bd662.
"""
import pytest
from flose.solutions.kan_9721_recrutamento_contrata_o_para_k_8bd662 import Kan9721RecrutamentoContrataOParaK8bd662Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9721RecrutamentoContrataOParaK8bd662Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
