from app.llm.gemini_client import GeminiClient
from app.agents.agent_memory import AgentMemory


class GameAgent:

    def __init__(self):
        self.ai = GeminiClient()
        self.memory = AgentMemory()

    def decide_action(self, player_action, player_status):

        past_memory = self.memory.get_memory()

        prompt = f"""
        You are the decision-making agent of WorldForge AI.

        Player action: {player_action}

        Player status:
        {player_status}

        Previous player memories:
        {past_memory}

        Choose one category:
        STORY, COMBAT, HEAL, STATUS, SAVE.

        Return ONLY one category word.
        """

        result = self.ai.generate(prompt).strip().upper()

        categories = ["STORY", "COMBAT", "HEAL", "STATUS", "SAVE"]

        for category in categories:
            if category in result:
                self.memory.remember_action(player_action)
                return category

        return "STORY"