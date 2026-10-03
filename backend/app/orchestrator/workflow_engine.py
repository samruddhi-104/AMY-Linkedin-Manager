from app.orchestrator.planner import BasicPlanner


class WorkflowEngine:
    def __init__(self) -> None:
        self.planner = BasicPlanner()

    def create_plan(self, intent: str):
        return self.planner.plan(intent)