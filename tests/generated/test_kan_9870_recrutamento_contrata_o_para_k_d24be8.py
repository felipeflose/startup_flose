"""
Pytest unit test suite for HR Onboarding: kan_9870_recrutamento_contrata_o_para_k_d24be8.
"""
import pytest
from flose.solutions.kan_9870_recrutamento_contrata_o_para_k_d24be8 import Kan9870RecrutamentoContrataOParaKD24be8Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9870RecrutamentoContrataOParaKD24be8Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
