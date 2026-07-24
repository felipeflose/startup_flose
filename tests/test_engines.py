import pytest
from flose.engines.planning import PlanningEngine
from flose.engines.governance import GovernanceEngine
from flose.core.models import TaskSpecification, TaskStatus

def test_planning_engine_decomposition():
    planner = PlanningEngine()
    tasks = planner.decompose_goal(
        goal_id="G1",
        goal_title="Setup Auth",
        steps=["Create DB Schema", "Write Endpoint", "Add Tests"]
    )
    assert len(tasks) == 3
    assert tasks[0].task_id == "tsk_G1_1"
    assert tasks[0].status == TaskStatus.READY

def test_planning_wsjf_calculation():
    planner = PlanningEngine()
    score = planner.calculate_wsjf(
        user_business_value=8.0,
        time_criticality=5.0,
        risk_reduction=3.0,
        job_size=2.0
    )
    assert score == 8.0

def test_governance_evidence_validation():
    gov = GovernanceEngine()
    task = TaskSpecification(
        task_id="tsk_01",
        title="Test Task",
        description="Desc",
        evidence_links=["file:///path/to/evidence.txt"]
    )
    valid, msg = gov.validate_evidence(task)
    assert valid is True
    assert msg == "Evidence verified."

    task_no_evidence = TaskSpecification(
        task_id="tsk_02",
        title="Test Task No Evidence",
        description="Desc"
    )
    valid_no, msg_no = gov.validate_evidence(task_no_evidence)
    assert valid_no is False
    assert "Axiom 1 Violation" in msg_no
