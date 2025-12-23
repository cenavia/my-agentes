from langchain.agents import create_agent
from agents.support.nodes.booking.tools import tools

system_prompt = """
Eres un asistente de ventas que ayuda a los clientes a encontrar los productos que necesitan y dar el clima de la ciudad

Tus tools son:
- get_products: para obtener los productos que ofreces en la tienda
- get_weather: para obtener el clima de la ciudad
"""

booking_node = create_agent(
    model="openai:gpt-4o-mini",
    tools=tools,
    system_prompt=system_prompt,
)