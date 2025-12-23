from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing import Optional

from agents.support.state import State
from agents.support.nodes.extractor.prompt import prompt_template

class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: Optional[str] = Field(default=None, description="The name of the person, or null if not provided explicitly")
    email: Optional[str] = Field(default=None, description="The email address of the person, or null if not provided explicitly")
    phone: Optional[str] = Field(default=None, description="The phone number of the person, or null if not provided explicitly")
    age: Optional[str] = Field(default=None, description="The age of the person, or null if not provided explicitly")

llm = init_chat_model("openai:gpt-4o", temperature=0)
llm = llm.with_structured_output(schema=ContactInfo)
 

def extractor(state: State):
    history = state["messages"]
    customer_name = state.get("customer_name", None)
    new_state: State = {}
    if customer_name is None:
        prompt = prompt_template.format()
        schema = llm.invoke([("system", prompt)] + history)
        # Solo establecer valores cuando el modelo haya devuelto contenido explícito.
        def _is_present(value: Optional[str]) -> bool:
            if value is None:
                return False
            normalized = value.strip().lower()
            return normalized not in ("", "none", "null", "n/a", "na", "unknown")

        if _is_present(schema.name):
            new_state["customer_name"] = schema.name  # type: ignore[assignment]
        if _is_present(schema.phone):
            new_state["phone"] = schema.phone  # type: ignore[assignment]
        if _is_present(schema.age):
            new_state["my_age"] = schema.age  # type: ignore[assignment]
    return new_state