from app.schemas.enemy import Enemy


class CombatManager:

    def __init__(self, player_manager):

        self.player = player_manager

    def create_enemy(self, name="Shadow Beast"):

        return Enemy(
            name=name,
            health=50,
            max_health=50,
            attack_power=10,
            gold_reward=20,
            xp_reward=30
        )

    def player_attack(self, enemy):

        if enemy.health <= 0:
            return "Enemy is already defeated."

        damage = 20

        enemy.health = max(0, enemy.health - damage)

        print(f"\nYou attacked {enemy.name}!")
        print(f"You dealt {damage} damage.")

        if enemy.health == 0:

            print("\nEnemy defeated!")

            self.player.add_gold(enemy.gold_reward)
            self.player.add_xp(enemy.xp_reward)

            return "VICTORY"

        return "CONTINUE"

    def enemy_attack(self, enemy):

        if enemy.health <= 0:
            return

        damage = enemy.attack_power

        self.player.take_damage(damage)

        print(f"\n{enemy.name} attacked you!")
        print(f"You lost {damage} health.")

    def use_potion(self):

        inventory = self.player.player.inventory

        if "Health Potion" not in inventory:
            print("\nYou don't have a health potion!")
            return

        if self.player.player.health >= self.player.player.max_health:
            print("\nYour health is already full!")
            return

        inventory.remove("Health Potion")

        self.player.heal(30)

        print("\nYou used a Health Potion!")
        print("You recovered 30 health.")