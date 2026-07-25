"""
Pytest unit test suite for HR Onboarding: kan_9771_recrutamento_contrata_o_para_k_fe45b1.
"""
import pytest
from flose.solutions.kan_9771_recrutamento_contrata_o_para_k_fe45b1 import Kan9771RecrutamentoContrataOParaKFe45b1Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9771RecrutamentoContrataOParaKFe45b1Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
