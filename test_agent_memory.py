from app.agents.agent_memory import AgentMemory

memory = AgentMemory()

memory.remember_action("Visited Elara's tower")
memory.remember_action("Explored the Whispering Forest")
memory.remember_defeat("Shadow Beast")
memory.remember_event("Discovered the Sunken Citadel portal")

print("\nAGENT MEMORY")
print(memory.get_memory())