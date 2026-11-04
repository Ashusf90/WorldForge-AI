from app.agents.orchestrator import GameOrchestrator

game_ai = GameOrchestrator()

result = game_ai.process_action(
    "Explore the Sunken Citadel and find King Arveth",
    {
        "health": 100,
        "gold": 50,
        "level": 1
    }
)

print("\n========== FINAL RESULT ==========")
print(result)