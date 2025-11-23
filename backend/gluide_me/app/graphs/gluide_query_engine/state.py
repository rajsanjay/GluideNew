from typing import TypedDict, List, Dict
from langchain_core.messages import BaseMessage


class GluideMeState(TypedDict):
    messages: List[BaseMessage]
    input: str
    main_intent: str
    sub_intent: str
    acquired_params: Dict
    missing_params: List[str]
    sql_query: str
    sql_output: str
    answer: str
    follow_up_questions: List[str]
