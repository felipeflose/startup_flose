"""
Pytest unit test suite for HR Onboarding: kan_9887_recrutamento_contrata_o_para_k_1d09b0.
"""
import pytest
from flose.solutions.kan_9887_recrutamento_contrata_o_para_k_1d09b0 import Kan9887RecrutamentoContrataOParaK1d09b0Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9887RecrutamentoContrataOParaK1d09b0Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
