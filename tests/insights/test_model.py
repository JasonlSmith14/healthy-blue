import sys
from pathlib import Path
from pydantic import BaseModel, Field

path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(path))

from insights.model import Model


class Response(BaseModel):
    response: str = Field(description="Response to the user")


model = Model(
    "Tell the user their name",
    "Greet the user by name and answer their question",
    insights_formatter=Response,
    follow_up_formatter=Response,
)

print("Initial response: ", model.generate_insight("My name is Jason").response)
print("")
print(
    "Follow up response: ",
    model.generate_insight("What is my name", follow_up=True).response,
)
