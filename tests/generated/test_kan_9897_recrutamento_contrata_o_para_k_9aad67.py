"""
Pytest unit test suite for HR Onboarding: kan_9897_recrutamento_contrata_o_para_k_9aad67.
"""
import pytest
from flose.solutions.kan_9897_recrutamento_contrata_o_para_k_9aad67 import Kan9897RecrutamentoContrataOParaK9aad67Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9897RecrutamentoContrataOParaK9aad67Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
