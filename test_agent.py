from app.agents.game_agent import GameAgent

agent = GameAgent()

tests = [
    "I want to explore the ancient forest",
    "Attack the Shadow Beast",
    "Drink my health potion",
    "Show my player status",
    "Save my adventure"
]

for action in tests:
    result = agent.decide_action(action, "Health: 80, Gold: 50")

    print(f"\nPlayer: {action}")
    print(f"Agent decision: {result}")