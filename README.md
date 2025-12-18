## Crear api-key en OpenAI
https://platform.openai.com/api-keys

## descarga cli
https://docs.langchain.com/langsmith/cli#langgraph-cli
```bash
uv add "langgraph-cli[inmem]" --dev
```
## Instlacion de dependencias
```bash
uv add langgraph langchain langchain-openai
uv add "langgraph-cli[inmem]" --dev
```


## ejcutar el servidor de langgraph
```bash
uv run langgraph dev
```
### abrimos el link
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

## Instalacion de Jupyter notebooks
```bash
uv add ipykernel --dev
```

# desde la raíz del repo
```bash
uv pip install -e .
```
## ejcutar el servidor de langgraph
```bash
uv run langgraph dev
```