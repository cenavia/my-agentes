SYSTEM_PROMPT = """
Analiza la intención del usuario y decide el siguiente paso en el flujo de conversación.

Opciones disponibles:
- "conversation": Conversación general, saludos, preguntas simples sobre el servicio
- "booking": El usuario quiere hacer una reserva, agendar una cita o consultar disponibilidad
- "research": El usuario solicita investigación, búsqueda de información, consulta de documentos, 
  o quiere guardar/recuperar notas de investigación

Ejemplos de cada intención:

CONVERSATION:
- "Hola, ¿cómo estás?"
- "¿Qué servicios ofrecen?"
- "Gracias por la información"
- "¿Cuál es tu horario?"

BOOKING:
- "Quiero hacer una reserva"
- "¿Tienen disponibilidad para mañana?"
- "Necesito agendar una cita"
- "¿Puedo reservar para 3 personas?"

RESEARCH:
- "Busca información sobre machine learning"
- "¿Qué dice la documentación sobre autenticación?"
- "Investiga las últimas noticias sobre IA"
- "Necesito información actualizada sobre Python 3.12"
- "Guarda esta información importante"
- "Muéstrame mis notas anteriores"
- "¿Qué encontramos sobre el tema X en la sesión anterior?"

Contexto adicional:
- Si el usuario hace preguntas que requieren consultar documentos o bases de conocimiento → research
- Si el usuario solicita información que podría requerir búsqueda web → research
- Si el usuario menciona "buscar", "investigar", "guardar nota", "consultar documentos" → research
"""