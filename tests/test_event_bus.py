import pytest
import asyncio
from flose.bus.event_bus import EventBus
from flose.core.models import (
    FLOSEMessage,
    AgentIdentity,
    AgentTier,
    SecurityContext,
    PriorityLevel,
)

@pytest.mark.asyncio
async def test_event_bus_publish_subscribe():
    bus = EventBus()
    received_messages = []

    async def sample_handler(msg: FLOSEMessage):
        received_messages.append(msg)

    bus.subscribe("task.execution", sample_handler)
    await bus.start()

    sender = AgentIdentity(
        agent_id="agt_ceo",
        role_name="Chief Executive Agent",
        tier=AgentTier.EXECUTIVE,
    )
    sec_ctx = SecurityContext(auth_token="token", signature="sig")
    message = FLOSEMessage(
        message_id="msg_001",
        trace_id="tr_001",
        sender=sender,
        recipient_id="agt_dev_01",
        topic="task.execution",
        payload={"task_id": "tsk_01"},
        priority=PriorityLevel.CRITICAL,
        security_context=sec_ctx,
    )

    await bus.publish(message)
    await asyncio.sleep(0.05)
    await bus.stop()

    assert len(received_messages) == 1
    assert received_messages[0].message_id == "msg_001"
    assert received_messages[0].priority == PriorityLevel.CRITICAL
