from langgraph.graph import MessagesState
from typing import Optional, List, Dict

class State(MessagesState):
    customer_name: Optional[str]
    phone: Optional[str]
    my_age: Optional[str]
     # ====================================
    # NUEVO: Campos para investigación
    # ====================================
    research_context: Optional[Dict[str, str]]  # Contexto de investigación activa
    saved_notes: Optional[List[str]]            # IDs de notas guardadas en la sesión