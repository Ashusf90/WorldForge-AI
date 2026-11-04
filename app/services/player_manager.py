from app.schemas.player import PlayerState


class PlayerManager:

    def __init__(self, player_name):

        self.player = PlayerState(
            name=player_name
        )

    def take_damage(self, amount):

        self.player.health = max(
            0,
            self.player.health - amount
        )

    def heal(self, amount):

        self.player.health = min(
            self.player.max_health,
            self.player.health + amount
        )

    def add_gold(self, amount):

        self.player.gold += amount

    def add_xp(self, amount):

        self.player.xp += amount

        while self.player.xp >= self.player.level * 100:

            required_xp = self.player.level * 100

            self.player.xp -= required_xp
            self.player.level += 1

    def add_item(self, item):

        self.player.inventory.append(item)

    def update_location(self, location):

        self.player.location = location

    def show_status(self):

        print("\n========== PLAYER STATUS ==========")

        print("Name:", self.player.name)
        print("Level:", self.player.level)

        print(
            f"Health: {self.player.health}/"
            f"{self.player.max_health}"
        )

        print("Gold:", self.player.gold)
        print("XP:", self.player.xp)
        print("Location:", self.player.location)

        print("\nInventory:")

        for item in self.player.inventory:
            print("-", item)

        print("===================================")