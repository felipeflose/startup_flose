import pytest
from flose.core.models import (
    AgentIdentity,
    AgentTier,
    TaskSpecification,
    TaskStatus,
    PriorityLevel,
    SecurityContext,
    FLOSEMessage,
)

def test_agent_identity_creation():
    agent = AgentIdentity(
        agent_id="agt_dev_01",
        role_name="Backend Developer",
        tier=AgentTier.ENGINEERING,
        reputation_score=0.95,
    )
    assert agent.agent_id == "agt_dev_01"
    assert agent.tier == AgentTier.ENGINEERING
    assert agent.reputation_score == 0.95

def test_task_specification_default_status():
    task = TaskSpecification(
        task_id="tsk_001",
        title="Implement Auth Module",
        description="Write JWT token handling code",
    )
    assert task.status == TaskStatus.BACKLOG
    assert task.priority == PriorityLevel.MEDIUM
    assert task.evidence_links == []

def test_flose_message_instantiation():
    sender = AgentIdentity(
        agent_id="agt_arch_01",
        role_name="Software Architect",
        tier=AgentTier.ARCHITECTURE,
    )
    sec_ctx = SecurityContext(auth_token="token_abc", signature="sig_123")
    msg = FLOSEMessage(
        message_id="msg_100",
        trace_id="tr_100",
        sender=sender,
        recipient_id="agt_dev_01",
        topic="task.execution",
        payload={"action": "start"},
        priority=PriorityLevel.HIGH,
        security_context=sec_ctx,
    )
    assert msg.sender.agent_id == "agt_arch_01"
    assert msg.priority == PriorityLevel.HIGH
