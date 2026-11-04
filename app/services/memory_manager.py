import json
from pathlib import Path


class MemoryManager:

    def __init__(self):

        self.save_folder = Path("data/saves")
        self.save_folder.mkdir(parents=True, exist_ok=True)

    def save_game(self, player, game_state):

        filename = f"{player.player.name.lower()}.json"
        file_path = self.save_folder / filename

        save_data = {
            "player": player.player.model_dump(),
            "game_state": game_state
        }

        with open(file_path, "w") as file:
            json.dump(save_data, file, indent=4)

        print("\nGame saved successfully!")

    def load_game(self, player_name):

        file_path = self.save_folder / f"{player_name.lower()}.json"

        if not file_path.exists():
            print("\nNo previous save found.")
            return None

        with open(file_path, "r") as file:
            save_data = json.load(file)

        print("\nPrevious adventure loaded!")

        return save_data