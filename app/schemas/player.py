from pydantic import BaseModel, Field


class PlayerState(BaseModel):

    name: str

    health: int = 100

    max_health: int = 100

    gold: int = 50

    xp: int = 0

    level: int = 1

    location: str = "Unknown"

    inventory: list[str] = Field(
        default_factory=lambda: ["Wooden Sword", "Health Potion"]
    )