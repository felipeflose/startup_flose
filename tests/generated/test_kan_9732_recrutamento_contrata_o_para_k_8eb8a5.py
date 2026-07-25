"""
Pytest unit test suite for HR Onboarding: kan_9732_recrutamento_contrata_o_para_k_8eb8a5.
"""
import pytest
from flose.solutions.kan_9732_recrutamento_contrata_o_para_k_8eb8a5 import Kan9732RecrutamentoContrataOParaK8eb8a5Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9732RecrutamentoContrataOParaK8eb8a5Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
