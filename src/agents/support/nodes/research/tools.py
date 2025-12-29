"""
Herramientas para el agente de investigación.
"""

from typing import List, Tuple
from langchain.tools import tool
from langchain_tavily import TavilySearch

from agents.support.nodes.research.vectorstore import search_documents


@tool(response_format="content_and_artifact")
def buscar_documentos(consulta: str) -> Tuple[str, List[dict]]:
    """
    Busca información en la base de conocimientos local del usuario.
    
    Usa esta herramienta cuando el usuario pregunte sobre temas que
    podrían estar en los documentos que ha cargado en el sistema.
    
    Args:
        consulta: La pregunta o tema a buscar en los documentos locales
        
    Returns:
        Tupla con (contenido formateado, metadatos de los documentos)
    """
    try:
        docs = search_documents(consulta, k=4)
        
        if not docs:
            return "No se encontró información relevante en los documentos locales.", []
        
        # Formatear contenido para el modelo
        contenido = "\n\n".join([
            f"[Fuente: {doc.metadata.get('source', 'desconocida')}]\n{doc.page_content}"
            for doc in docs
        ])
        
        # Metadatos como artefacto
        metadatos = [
            {
                "fuente": doc.metadata.get("source", "desconocida"),
                "preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            }
            for doc in docs
        ]
        
        return contenido, metadatos
        
    except Exception as e:
        return f"Error al buscar en documentos: {str(e)}", []


# Configurar herramienta de búsqueda web con Tavily
buscar_web = TavilySearch(
    max_results=5,
    search_depth="basic",
    include_answer=True,
    include_raw_content=False
)
buscar_web.name = "buscar_web"
buscar_web.description = """
Busca información actualizada en Internet usando Tavily.

Usa esta herramienta cuando necesites:
- Información en tiempo real o noticias recientes
- Datos actualizados (precios, estadísticas, eventos)
- Información que probablemente no esté en los documentos locales
- Verificar hechos o complementar información

Args:
    query: La consulta de búsqueda para Internet
"""


@tool
def guardar_nota(titulo: str, contenido: str) -> str:
    """
    Guarda una nota importante para referencia futura del usuario.
    
    Usa esta herramienta cuando:
    - El usuario quiera recordar algo específico de la investigación
    - Encuentres información valiosa que el usuario debería guardar
    - El usuario explícitamente pida guardar información
    
    Args:
        titulo: Título breve y descriptivo de la nota
        contenido: Contenido detallado de la nota a guardar
        
    Returns:
        Confirmación de que la nota fue guardada
    """
    # TODO: Implementar persistencia real con store o base de datos
    # Por ahora retornamos confirmación
    
    # Validaciones básicas
    if not titulo or not contenido:
        return "Error: Tanto el título como el contenido son requeridos."
    
    if len(titulo) > 100:
        return "Error: El título es demasiado largo (máximo 100 caracteres)."
    
    # En una implementación real, guardarías esto en el store de LangGraph
    # o en una base de datos
    print(f"[Research] Nota guardada: {titulo}")
    return f"✓ Nota '{titulo}' guardada correctamente."


@tool
def listar_notas() -> str:
    """
    Lista todas las notas guardadas por el usuario en sesiones anteriores.
    
    Usa esta herramienta cuando:
    - El usuario pregunte qué notas tiene guardadas
    - El usuario quiera revisar información guardada previamente
    - Necesites recordar contexto de investigaciones anteriores
    
    Returns:
        Lista formateada de notas guardadas o mensaje si no hay notas
    """
    # TODO: Implementar recuperación real desde store o base de datos
    
    # En una implementación real, recuperarías esto del store
    # Por ahora retornamos mensaje placeholder
    return "No hay notas guardadas aún. Usa 'guardar_nota' para crear una."


def get_research_tools() -> List:
    """
    Obtiene la lista de todas las herramientas de investigación.
    
    Returns:
        Lista de herramientas disponibles para el agente
    """
    return [
        buscar_documentos,
        buscar_web,
        guardar_nota,
        listar_notas
    ]