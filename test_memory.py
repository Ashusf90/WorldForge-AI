from app.services.memory_manager import MemoryManager
from app.services.player_manager import PlayerManager

# Create player
player = PlayerManager("Ashu")

# Update player information
player.take_damage(20)
player.add_gold(100)
player.add_xp(50)
player.update_location("Sunken Citadel")

# Create memory manager
memory = MemoryManager()

# Save game information
game_state = {
    "world": "Aethelgard",
    "scene": "Ashu entered the Sunken Citadel.",
    "summary": "Ashu discovered an ancient magical kingdom."
}

memory.save_game(player, game_state)

# Load saved information
saved_data = memory.load_game("Ashu")

print("\n========== LOADED MEMORY ==========")

print("Player:", saved_data["player"]["name"])
print("Health:", saved_data["player"]["health"])
print("Gold:", saved_data["player"]["gold"])
print("Location:", saved_data["player"]["location"])

print("World:", saved_data["game_state"]["world"])
print("Story:", saved_data["game_state"]["summary"])