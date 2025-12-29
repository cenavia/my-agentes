"""
Nodo principal del agente de investigación.
"""

from langchain.agents import create_agent
from agents.support.state import State
from agents.support.nodes.research.tools import get_research_tools
from agents.support.nodes.research.prompt import prompt_template
from agents.support.nodes.research.vectorstore import initialize_vectorstore

# Inicializar vector store al cargar el módulo
print("[Research] Inicializando módulo de investigación...")
initialize_vectorstore()
print("[Research] Módulo listo")

# Crear el agente de investigación
research_agent = create_agent(
    model="openai:gpt-4o",
    tools=get_research_tools(),
    system_prompt=prompt_template,
)


def research_node(state: State) -> dict:
    """
    Nodo que maneja investigación y búsqueda de información.
    
    Este nodo:
    1. Recibe el estado con los mensajes del usuario
    2. Invoca el agente de investigación que decide qué herramientas usar
    3. Retorna la respuesta generada
    
    Args:
        state: Estado actual del grafo con el historial de mensajes
        
    Returns:
        Diccionario con los mensajes actualizados
    """
    print("[Research Node] Procesando consulta de investigación...")
    
    # El agente procesa automáticamente los mensajes
    # y usa las herramientas según necesite
    result = research_agent.invoke(state)
    
    print("[Research Node] Consulta procesada")
    
    return result