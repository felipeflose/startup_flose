"""
Pytest unit test suite for HR Onboarding: kan_9698_recrutamento_contrata_o_para_k_12f88b.
"""
import pytest
from flose.solutions.kan_9698_recrutamento_contrata_o_para_k_12f88b import Kan9698RecrutamentoContrataOParaK12f88bSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9698RecrutamentoContrataOParaK12f88bSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
