"""
Pytest unit test suite for HR Onboarding: kan_9732_recrutamento_contrata_o_para_k_214f94.
"""
import pytest
from flose.solutions.kan_9732_recrutamento_contrata_o_para_k_214f94 import Kan9732RecrutamentoContrataOParaK214f94Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9732RecrutamentoContrataOParaK214f94Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
