"""
Pytest unit test suite for HR Onboarding: kan_9872_recrutamento_contrata_o_para_k_67bdf8.
"""
import pytest
from flose.solutions.kan_9872_recrutamento_contrata_o_para_k_67bdf8 import Kan9872RecrutamentoContrataOParaK67bdf8Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9872RecrutamentoContrataOParaK67bdf8Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
