"""
Pytest unit test suite for HR Onboarding: kan_9730_recrutamento_contrata_o_para_k_3d31d9.
"""
import pytest
from flose.solutions.kan_9730_recrutamento_contrata_o_para_k_3d31d9 import Kan9730RecrutamentoContrataOParaK3d31d9Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9730RecrutamentoContrataOParaK3d31d9Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
