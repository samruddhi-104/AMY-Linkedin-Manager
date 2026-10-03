from dataclasses import dataclass


@dataclass
class PlannedTask:
    task_type: str
    agents: list[str]


class BasicPlanner:
    def plan(self, intent: str) -> PlannedTask:
        plans = {
            "RESEARCH": PlannedTask(
                task_type="RESEARCH",
                agents=["research"],
            ),
            "COMPETITOR_RESEARCH": PlannedTask(
                task_type="COMPETITOR_RESEARCH",
                agents=["competitor"],
            ),
            "KEYWORD_RESEARCH": PlannedTask(
                task_type="KEYWORD_RESEARCH",
                agents=["keyword"],
            ),
            "GENERAL": PlannedTask(
                task_type="GENERAL",
                agents=[],
            ),
        }

        return plans.get(
            intent,
            PlannedTask(
                task_type="GENERAL",
                agents=[],
            ),
        )