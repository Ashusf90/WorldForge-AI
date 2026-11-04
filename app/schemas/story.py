from pydantic import BaseModel, Field


class StoryResponse(BaseModel):

    world_name: str
    scene: str
    atmosphere: str

    choices: list[str] = Field(
        min_length=3,
        max_length=4
    )

    story_summary: str


class TurnResponse(BaseModel):

    scene: str

    atmosphere: str

    choices: list[str] = Field(
        min_length=3,
        max_length=4
    )

    story_summary: str