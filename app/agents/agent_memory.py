import json
from pathlib import Path


class AgentMemory:

    def __init__(self):
        self.file_path = Path("data/saves/agent_memory.json")
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if self.file_path.exists():
            self.memory = json.loads(
                self.file_path.read_text(encoding="utf-8")
            )
        else:
            self.memory = {
                "actions": [],
                "defeated_enemies": [],
                "important_events": []
            }

    def remember_action(self, action):
        self.memory["actions"].append(action)
        self.save()

    def remember_defeat(self, enemy):
        if enemy not in self.memory["defeated_enemies"]:
            self.memory["defeated_enemies"].append(enemy)
        self.save()

    def remember_event(self, event):
        self.memory["important_events"].append(event)
        self.save()

    def get_memory(self):
        return self.memory

    def save(self):
        self.file_path.write_text(
            json.dumps(self.memory, indent=4),
            encoding="utf-8"
        )