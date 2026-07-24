from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict
from flose.core.enums import AgentTier, TaskStatus, PriorityLevel, MemoryType

class SecurityContext(BaseModel):
    auth_token: str
    signature: str
    permissions: List[str] = Field(default_factory=list)

class AgentIdentity(BaseModel):
    agent_id: str = Field(..., description="Unique agent identifier (e.g., agt_dev_01)")
    role_name: str
    tier: AgentTier
    reputation_score: float = Field(default=1.0, ge=0.0, le=1.0)

class TaskSpecification(BaseModel):
    task_id: str
    title: str
    description: str
    acceptance_criteria: List[str] = Field(default_factory=list)
    assigned_agent_id: Optional[str] = None
    status: TaskStatus = TaskStatus.BACKLOG
    priority: PriorityLevel = PriorityLevel.MEDIUM
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    estimated_tokens: int = 1000
    actual_tokens_used: int = 0
    evidence_links: List[str] = Field(default_factory=list)

class FLOSEMessage(BaseModel):
    message_id: str
    trace_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sender: AgentIdentity
    recipient_id: str
    topic: str
    payload: Dict[str, Any]
    priority: PriorityLevel = PriorityLevel.MEDIUM
    security_context: SecurityContext

class AuditRecord(BaseModel):
    model_config = ConfigDict(frozen=True)

    event_id: str
    trace_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    agent_id: str
    action_taken: str
    payload_hash: str
    verification_status: bool = True
