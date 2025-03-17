import time
from typing import Generator
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


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


class Model:
    def __init__(self, system_prompt: str):
        self.client = ChatOpenAI(model="gpt-4o-mini", streaming=True)
        self.system_prompt = system_prompt

    def generate_output(self, user_prompt: str) -> Generator[
        ResponseFormatter,
        None,
        None,
    ]:

        chat_prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("user", user_prompt),
            ]
        )

        model = self.client.model_copy()
        model = model.with_structured_output(ResponseFormatter)

        chain = chat_prompt_template | model

        # With 4o-mini, this is so quick that streaming is pointless. But 4o-mini is expensive, might be ideal to switch to slower model where streaming will be needed
        for chunk in chain.stream({}):
            # time.sleep(0.1)
            yield chunk
