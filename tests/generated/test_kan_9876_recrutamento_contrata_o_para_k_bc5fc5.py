"""
Pytest unit test suite for HR Onboarding: kan_9876_recrutamento_contrata_o_para_k_bc5fc5.
"""
import pytest
from flose.solutions.kan_9876_recrutamento_contrata_o_para_k_bc5fc5 import Kan9876RecrutamentoContrataOParaKBc5fc5Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9876RecrutamentoContrataOParaKBc5fc5Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
