import time
from typing import Generator
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from insights.formatting import ResponseFormatter


class Model:
    def __init__(self, system_prompt: str, model: str = "gpt-4o-mini"):
        self.client = ChatOpenAI(model=model, streaming=True)
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
            time.sleep(0.1)
            yield chunk
