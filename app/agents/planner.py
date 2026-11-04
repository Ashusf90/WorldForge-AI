from app.llm.gemini_client import GeminiClient


class Planner:

    def __init__(self):
        self.ai = GeminiClient()

    def create_plan(self, player_action, player_status, memory):

        prompt = f"""
        You are the planning agent of WorldForge AI.

        Player action: {player_action}
        Player status: {player_status}
        Previous memory: {memory}

        Create a simple plan with 3 steps to handle
        the player's request.

        Return only a numbered list.
        """

        return self.ai.generate(prompt)