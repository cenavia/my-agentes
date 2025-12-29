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

## Creacionde RAG con file tools de openAI
1. https://platform.openai.com/storage
2. Vector stores
3. + Create
4. Vector store = My Docs y click en el check
5. add files
6. Upload, selecciono el archivo y clic en abrir
7. Attach
8. copiamos el ID y lo introducimos en nuestro codigo.

## instalar libreria para hacer templating en promps
```bash
    uv add Jinja2
```

## Generar token de anthropic
https://console.anthropic.com/settings/keys

## instalacion de libreria 
```bash
    uv add langchain-anthropic
```

## Instlar dependencia de Tavili 
```bash
    uv add langchain-tavily langchain-openai
```

## Obtener API_KEY de Tavili 
https://www.tavily.com/

## Instalar base vectorial de Croma db
```bash
    uv add langchain-chroma langchain-community chromadb
```