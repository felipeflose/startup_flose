"""
Pytest unit test suite for HR Onboarding: kan_9901_recrutamento_contrata_o_para_k_4b6b46.
"""
import pytest
from flose.solutions.kan_9901_recrutamento_contrata_o_para_k_4b6b46 import Kan9901RecrutamentoContrataOParaK4b6b46Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9901RecrutamentoContrataOParaK4b6b46Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
