"""
Pytest unit test suite for HR Onboarding: kan_9894_recrutamento_contrata_o_para_k_b0dcd6.
"""
import pytest
from flose.solutions.kan_9894_recrutamento_contrata_o_para_k_b0dcd6 import Kan9894RecrutamentoContrataOParaKB0dcd6Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9894RecrutamentoContrataOParaKB0dcd6Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
