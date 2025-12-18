## Crear api-key en OpenAI
https://platform.openai.com/api-keys

## descarga cli
https://docs.langchain.com/langsmith/cli#langgraph-cli
uv add "langgraph-cli[inmem]" --dev

## Instlacion de dependencias
uv add langgraph langchain langchain-openai
uv add "langgraph-cli[inmem]" --dev

## ejcutar el servidor de langgraph
uv run langgraph dev
### abrimos el link
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
