"""
Pytest unit test suite for HR Onboarding: kan_9730_recrutamento_contrata_o_para_k_9695d7.
"""
import pytest
from flose.solutions.kan_9730_recrutamento_contrata_o_para_k_9695d7 import Kan9730RecrutamentoContrataOParaK9695d7Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9730RecrutamentoContrataOParaK9695d7Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
