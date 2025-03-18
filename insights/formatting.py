from pydantic import BaseModel, Field


class ResponseFormatter(BaseModel):
    title: str = Field(
        description="A catchy, fun, and engaging title that captures the user's key achievement."
    )
    highlight: str = Field(
        description="The main insight or achievement in an exciting and positive way."
    )
    fun_to_know: str = Field(
        description="A playful or motivational fact related to the user’s data."
    )
    challenge: str = Field(
        description="A motivating challenge or action the user can take based on their performance."
    )
