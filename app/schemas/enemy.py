from pydantic import BaseModel


class Enemy(BaseModel):

    name: str

    health: int = 50

    max_health: int = 50

    attack_power: int = 10

    gold_reward: int = 20

    xp_reward: int = 30