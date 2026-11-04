from app.agents.planner import Planner

planner = Planner()

plan = planner.create_plan(
    "Explore the Sunken Citadel and find King Arveth",
    {"health": 100, "gold": 50},
    {"defeated_enemies": ["Shadow Beast"]}
)

print("\nAI GENERATED PLAN:")
print(plan)