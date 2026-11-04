from app.llm.gemini_client import GeminiClient
from app.schemas.story import StoryResponse, TurnResponse
from app.services.lore_manager import LoreManager


class StoryEngine:

    def __init__(self):
        self.ai = GeminiClient()
        self.lore = LoreManager()
        self.lore.load_lore()

    def generate_world(self, player_name):
        knowledge = self.lore.search_lore(
            "Aethelgard kingdom, history and important locations"
        )

        prompt = f"""
        You are WorldForge AI, a fantasy game master.

        Player: {player_name}

        WORLD KNOWLEDGE:
        {knowledge}

        Create an immersive fantasy adventure.
        Use the provided world knowledge to maintain consistency.

        Generate:
        - Unique world name
        - Opening scene
        - Atmosphere
        - Three or four meaningful choices
        - Story summary
        """

        return self.ai.generate_structured(prompt, StoryResponse)

    def process_action(
        self, player_name, world_name, previous_scene,
        previous_summary, action
    ):
        knowledge = self.lore.search_lore(action)

        prompt = f"""
        You are the Dungeon Master of WorldForge AI.

        Player: {player_name}
        World: {world_name}

        PREVIOUS SCENE:
        {previous_scene}

        STORY SUMMARY:
        {previous_summary}

        PLAYER ACTION:
        {action}

        RELEVANT WORLD KNOWLEDGE:
        {knowledge}

        Continue the same adventure.
        Use relevant world knowledge.
        Describe consequences of the player's action.
        Do not contradict established world facts.
        Give three or four meaningful choices.
        Update the story summary.
        """

        return self.ai.generate_structured(prompt, TurnResponse)