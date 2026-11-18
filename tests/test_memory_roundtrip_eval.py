"""Randomized round-trip regression for persisted player and game state."""
import random
import string

from app.schemas.player import PlayerState
from app.services.memory_manager import MemoryManager
from app.services.player_manager import PlayerManager


def test_randomized_player_and_game_state_round_trip(tmp_path, monkeypatch):
    rng = random.Random(20261118)
    manager = MemoryManager()
    monkeypatch.setattr(manager, "save_folder", tmp_path)

    for index in range(25):
        name = f"eval_{index}_{''.join(rng.choices(string.ascii_lowercase, k=5))}"
        player = PlayerManager(name)
        player.player = PlayerState(
            name=name,
            health=rng.randint(0, 100),
            max_health=100,
            gold=rng.randint(0, 500),
            xp=rng.randint(0, 999),
            level=rng.randint(1, 12),
            location=rng.choice(["Silverkeep", "Whispering Forest", "Sunken Citadel"]),
            inventory=[rng.choice(["Wooden Sword", "Crystal Sword", "Health Potion"])
                       for _ in range(rng.randint(0, 8))],
        )
        state = {
            "world": "Aethelgard",
            "scene": f"Scene {index}: {''.join(rng.choices(string.ascii_letters, k=24))}",
            "summary": f"Summary {index}",
            "atmosphere": rng.choice(["ominous", "hopeful", "mysterious"]),
            "choices": [f"Choice {n}" for n in range(3)],
            "story_history": [
                {"turn": turn, "action": f"action-{turn}", "scene": f"scene-{turn}"}
                for turn in range(rng.randint(1, 8))
            ],
        }
        manager.save_game(player, state)

        fresh = MemoryManager()
        monkeypatch.setattr(fresh, "save_folder", tmp_path)
        restored = fresh.load_game(name)
        assert PlayerState.model_validate(restored["player"]) == player.player
        assert restored["game_state"] == state
