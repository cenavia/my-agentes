from langgraph.graph import MessagesState
from typing import Optional

class State(MessagesState):
    customer_name: Optional[str]
    phone: Optional[str]
    my_age: Optional[str]