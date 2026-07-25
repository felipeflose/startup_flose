"""
Pytest unit test suite for HR Onboarding: kan_9704_recrutamento_contrata_o_para_k_97e42f.
"""
import pytest
from flose.solutions.kan_9704_recrutamento_contrata_o_para_k_97e42f import Kan9704RecrutamentoContrataOParaK97e42fSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9704RecrutamentoContrataOParaK97e42fSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
