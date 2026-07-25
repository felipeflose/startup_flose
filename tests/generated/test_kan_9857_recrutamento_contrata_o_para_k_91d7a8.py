"""
Pytest unit test suite for HR Onboarding: kan_9857_recrutamento_contrata_o_para_k_91d7a8.
"""
import pytest
from flose.solutions.kan_9857_recrutamento_contrata_o_para_k_91d7a8 import Kan9857RecrutamentoContrataOParaK91d7a8Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9857RecrutamentoContrataOParaK91d7a8Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
