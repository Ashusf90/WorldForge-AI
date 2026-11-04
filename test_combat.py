from app.services.player_manager import PlayerManager
from app.services.combat_manager import CombatManager

player = PlayerManager("Ashu")

combat = CombatManager(player)

enemy = combat.create_enemy()

print("\n===== BATTLE STARTED =====")

print("Enemy:", enemy.name)
print("Enemy Health:", enemy.health)

# Player attacks
result = combat.player_attack(enemy)

if result != "VICTORY":
    combat.enemy_attack(enemy)

# Show player status
player.show_status()

print("\nEnemy Remaining Health:", enemy.health)

print("\n===== POTION TEST =====")

combat.use_potion()

player.show_status()