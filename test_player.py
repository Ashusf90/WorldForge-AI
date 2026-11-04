from app.services.player_manager import PlayerManager


player = PlayerManager("Ashu")

player.take_damage(20)
player.add_gold(100)
player.add_xp(120)
player.add_item("Magic Sword")
player.update_location("Sunken Citadel")

player.show_status()