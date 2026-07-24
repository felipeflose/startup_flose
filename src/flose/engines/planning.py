from typing import List, Dict
from flose.core.models import TaskSpecification
from flose.core.enums import PriorityLevel, TaskStatus

class PlanningEngine:
    """Engine responsible for decomposing high-level goals into DAG tasks."""

    def decompose_goal(self, goal_id: str, goal_title: str, steps: List[str]) -> List[TaskSpecification]:
        """Decomposes a strategic goal into executable task specifications."""
        tasks: List[TaskSpecification] = []
        for idx, step in enumerate(steps, start=1):
            task = TaskSpecification(
                task_id=f"tsk_{goal_id}_{idx}",
                title=f"[{goal_title}] Step {idx}: {step}",
                description=f"Execute sub-step: {step}",
                acceptance_criteria=[f"Empirical evidence generated for {step}"],
                status=TaskStatus.READY,
                priority=PriorityLevel.HIGH if idx == 1 else PriorityLevel.MEDIUM,
            )
            tasks.append(task)
        return tasks

    def calculate_wsjf(self, user_business_value: float, time_criticality: float, risk_reduction: float, job_size: float) -> float:
        """Calculates Weighted Shortest Job First (WSJF) priority score."""
        if job_size <= 0:
            raise ValueError("Job size must be greater than zero.")
        cost_of_delay = user_business_value + time_criticality + risk_reduction
        return cost_of_delay / job_size
