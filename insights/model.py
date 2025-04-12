# import json
# from typing import Any, Dict, TypedDict
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph import START, MessagesState, StateGraph
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from pydantic import BaseModel
# from langchain_core.messages import HumanMessage, AIMessage
# from insights.formatting import FollowUpFormatter, InsightsFormatter


# class Model:
#     def __init__(
#         self,
#         insights_system_prompt: str,
#         follow_up_system_prompt: str,
#         insights_formatter: BaseModel,
#         follow_up_formatter: BaseModel,
#         model: str = "gpt-4o-mini",
#     ):
#         self.client = ChatOpenAI(model=model)
#         self.insights_system_prompt = insights_system_prompt
#         self.follow_up_system_prompt = follow_up_system_prompt

#         self.insights_formatter = insights_formatter
#         self.follow_up_formatter = follow_up_formatter

#         self._create_insights_chain()
#         self._create_follow_up_chain()

#         workflow = StateGraph(state_schema=MessagesState)

#         workflow.add_edge(START, "invoke_chain")
#         workflow.add_node("invoke_chain", self.invoke_chain)

#         memory = MemorySaver()
#         self.app = workflow.compile(checkpointer=memory)

#         self.config = {"configurable": {"thread_id": "abc123"}}

#     def _create_chain(self, prompt: str, response_formatter: BaseModel):
#         chat_prompt_template = ChatPromptTemplate.from_messages(
#             [("system", prompt), ("user", "{user}")]
#         )

#         model = self.client.model_copy()
#         model = model.with_structured_output(response_formatter)

#         return chat_prompt_template | model

#     def _create_insights_chain(self):
#         self.insights_chain = self._create_chain(
#             prompt=self.insights_system_prompt,
#             response_formatter=self.insights_formatter,
#         )

#     def _create_follow_up_chain(self):
#         self.follow_up_chain = self._create_chain(
#             prompt=self.follow_up_system_prompt,
#             response_formatter=self.follow_up_formatter,
#         )

#     def generate_insight(
#         self, user_data: str, follow_up: bool = False
#     ) -> InsightsFormatter | FollowUpFormatter:

#         response = self.app.invoke(
#             {
#                 "messages": HumanMessage(
#                     content=user_data, kwargs={"follow_up": follow_up}
#                 )
#             },
#             config=self.config,
#         )

#         parsed_dict = json.loads(response["messages"][-1].content)

#         if follow_up:
#             data = self.follow_up_formatter(**parsed_dict)
#         else:
#             data = self.insights_formatter(**parsed_dict)

#         return data

#     def invoke_chain(
#         self, state: MessagesState
#     ) -> InsightsFormatter | FollowUpFormatter:
#         follow_up = state["messages"][-1].kwargs["follow_up"]
#         user = state["messages"][-1].content
#         invoke = {"user": user}
#         if follow_up:
#             response = self.follow_up_chain.invoke(invoke)
#         else:
#             response = self.insights_chain.invoke(invoke)

#         return {"messages": AIMessage(content=json.dumps(response.dict()))}


import json
from typing import Union
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from insights.formatting import FollowUpFormatter, InsightsFormatter


class Model:
    def __init__(
        self,
        insights_system_prompt: str,
        follow_up_system_prompt: str,
        insights_formatter: BaseModel,
        follow_up_formatter: BaseModel,
        model: str = "gpt-4o-mini",
    ):
        self.client = ChatOpenAI(model=model)
        self.insights_formatter = insights_formatter
        self.follow_up_formatter = follow_up_formatter

        self.insights_system_prompt = insights_system_prompt
        self.follow_up_system_prompt = follow_up_system_prompt

        workflow = StateGraph(state_schema=MessagesState)
        workflow.add_edge(START, "invoke_chain")
        workflow.add_node("invoke_chain", self.invoke_chain)

        memory = MemorySaver()
        self.app = workflow.compile(checkpointer=memory)
        self.config = {"configurable": {"thread_id": "abc123"}}

    def generate_insight(
        self, user_data: str, follow_up: bool = False
    ) -> Union[InsightsFormatter, FollowUpFormatter]:
        response = self.app.invoke(
            {
                "messages": HumanMessage(
                    content=user_data,
                    kwargs={"follow_up": follow_up},
                )
            },
            config=self.config,
        )

        parsed_dict = json.loads(response["messages"][-1].content)

        if follow_up:
            return self.follow_up_formatter(**parsed_dict)
        return self.insights_formatter(**parsed_dict)

    def invoke_chain(self, state: MessagesState) -> MessagesState:
        messages = state["messages"]
        follow_up = messages[-1].kwargs.get("follow_up", False)

        system_message = SystemMessage(
            content=(
                self.follow_up_system_prompt
                if follow_up
                else self.insights_system_prompt
            )
        )
        prompt_messages = [system_message] + messages

        model = self.client.model_copy()
        model = model.with_structured_output(
            self.follow_up_formatter if follow_up else self.insights_formatter
        )

        response = model.invoke(prompt_messages)

        return {"messages": AIMessage(content=json.dumps(response.dict()))}
