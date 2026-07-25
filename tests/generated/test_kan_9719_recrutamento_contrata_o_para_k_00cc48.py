"""
Pytest unit test suite for HR Onboarding: kan_9719_recrutamento_contrata_o_para_k_00cc48.
"""
import pytest
from flose.solutions.kan_9719_recrutamento_contrata_o_para_k_00cc48 import Kan9719RecrutamentoContrataOParaK00cc48Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9719RecrutamentoContrataOParaK00cc48Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
