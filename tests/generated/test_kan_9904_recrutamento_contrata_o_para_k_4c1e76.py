"""
Pytest unit test suite for HR Onboarding: kan_9904_recrutamento_contrata_o_para_k_4c1e76.
"""
import pytest
from flose.solutions.kan_9904_recrutamento_contrata_o_para_k_4c1e76 import Kan9904RecrutamentoContrataOParaK4c1e76Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9904RecrutamentoContrataOParaK4c1e76Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
