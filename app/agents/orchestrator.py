from app.agents.game_agent import GameAgent
from app.agents.planner import Planner


class GameOrchestrator:

    def __init__(self):
        self.agent = GameAgent()
        self.planner = Planner()

    def process_action(self, action, player_status):

        print("\nAI is analysing your action...")

        decision = self.agent.decide_action(
            action,
            player_status
        )

        print("\nAI Decision:", decision)

        plan = None

        if decision == "STORY":
            plan = self.planner.create_plan(
                action,
                player_status,
                self.agent.memory.get_memory()
            )

            print("\nAI ACTION PLAN:")
            print(plan)

        return {
            "decision": decision,
            "plan": plan
        }