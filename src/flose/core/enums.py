from enum import Enum

class AgentTier(str, Enum):
    EXECUTIVE = "EXECUTIVE"
    ARCHITECTURE = "ARCHITECTURE"
    ENGINEERING = "ENGINEERING"
    QA_SECURITY = "QA_SECURITY"
    DEVOPS = "DEVOPS"
    GOVERNANCE = "GOVERNANCE"

class TaskStatus(str, Enum):
    BACKLOG = "BACKLOG"
    READY = "READY"
    IN_PROGRESS = "IN_PROGRESS"
    IN_REVIEW = "IN_REVIEW"
    QA_VERIFICATION = "QA_VERIFICATION"
    DONE = "DONE"
    FAILED = "FAILED"

class PriorityLevel(int, Enum):
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class MemoryType(str, Enum):
    EPISODIC = "EPISODIC"
    SEMANTIC = "SEMANTIC"
    PROCEDURAL = "PROCEDURAL"
    WORKING = "WORKING"
