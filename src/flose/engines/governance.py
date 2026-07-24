import hashlib
from typing import Tuple
from flose.core.models import TaskSpecification, TaskStatus

class GovernanceEngine:
    """Engine enforcing anti-hallucination policies and empirical evidence validation."""

    def validate_evidence(self, task: TaskSpecification) -> Tuple[bool, str]:
        """Validates that a task includes valid evidence links before completion."""
        if not task.evidence_links:
            return False, "Axiom 1 Violation: No empirical evidence links provided."
        
        for link in task.evidence_links:
            if not (link.startswith("file://") or link.startswith("http://") or link.startswith("https://")):
                return False, f"Invalid evidence reference format: {link}"
        
        return True, "Evidence verified."

    def generate_audit_hash(self, agent_id: str, action: str, payload_str: str) -> str:
        """Generates SHA-256 hash for immutable audit logging."""
        raw_data = f"{agent_id}:{action}:{payload_str}"
        return hashlib.sha256(raw_data.encode("utf-8")).hexdigest()
