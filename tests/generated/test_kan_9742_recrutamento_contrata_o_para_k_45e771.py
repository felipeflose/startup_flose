"""
Pytest unit test suite for HR Onboarding: kan_9742_recrutamento_contrata_o_para_k_45e771.
"""
import pytest
from flose.solutions.kan_9742_recrutamento_contrata_o_para_k_45e771 import Kan9742RecrutamentoContrataOParaK45e771Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9742RecrutamentoContrataOParaK45e771Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
