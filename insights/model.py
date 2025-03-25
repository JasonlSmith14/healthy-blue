import time
from typing import Generator
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from insights.formatting import ResponseFormatter


class Model:
    def __init__(self, system_prompt: str, model: str = "gpt-4o-mini"):
        self.client = ChatOpenAI(model=model, streaming=True)
        self.system_prompt = system_prompt

    def generate_insight(self, user_data: str) -> ResponseFormatter:

        chat_prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("user", user_data),
            ]
        )

        model = self.client.model_copy()
        model = model.with_structured_output(ResponseFormatter)

        chain = chat_prompt_template | model

        return chain.invoke({})
