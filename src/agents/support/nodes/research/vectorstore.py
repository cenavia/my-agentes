"""
Gestión del vector store con ChromaDB para búsqueda RAG.
"""

import os
from typing import Optional, List
from pathlib import Path

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from agents.support.nodes.research.config import (
    get_documentos_dir, 
    get_chroma_db_dir,
    get_research_stats
)

# ====================================
# Variables globales (singleton pattern)
# ====================================
_vectorstore: Optional[Chroma] = None
_retriever = None
_embeddings: Optional[OpenAIEmbeddings] = None


def get_embeddings() -> OpenAIEmbeddings:
    """Obtiene o crea el modelo de embeddings."""
    global _embeddings
    if _embeddings is None:
        _embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return _embeddings


def initialize_vectorstore(force_reload: bool = False) -> Chroma:
    """
    Inicializa o recarga el vector store.
    
    Args:
        force_reload: Si True, recarga todos los documentos incluso si el store existe
        
    Returns:
        Instancia de Chroma vector store
    """
    global _vectorstore, _retriever
    
    # Si ya existe y no se fuerza recarga, retornar existente
    if _vectorstore is not None and not force_reload:
        return _vectorstore
    
    embeddings = get_embeddings()
    chroma_dir = get_chroma_db_dir()
    docs_dir = get_documentos_dir()
    
    print(f"[Research] Inicializando vector store...")
    print(f"[Research] Directorio documentos: {docs_dir}")
    print(f"[Research] Directorio ChromaDB: {chroma_dir}")
    
    # Verificar si hay documentos para cargar
    txt_files = list(docs_dir.glob("*.txt"))
    
    # Excluir el README.txt generado automáticamente
    txt_files = [f for f in txt_files if f.name != "README.txt"]
    
    if txt_files or force_reload:
        print(f"[Research] Encontrados {len(txt_files)} documentos .txt")
        
        # Cargar documentos
        loader = DirectoryLoader(
            str(docs_dir),
            glob="*.txt",
            loader_cls=TextLoader,
            exclude=["README.txt"]  # Excluir el README
        )
        
        try:
            documents = loader.load()
            
            if documents:
                print(f"[Research] Cargados {len(documents)} documentos")
                
                # Dividir en chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    separators=["\n\n", "\n", ". ", " ", ""]
                )
                chunks = text_splitter.split_documents(documents)
                print(f"[Research] Generados {len(chunks)} chunks")
                
                # Crear vector store
                _vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=embeddings,
                    persist_directory=str(chroma_dir),
                    collection_name="base_conocimientos"
                )
                print(f"[Research] Vector store creado exitosamente")
            else:
                print(f"[Research] No se encontraron documentos válidos")
                _vectorstore = _create_empty_vectorstore(embeddings, chroma_dir)
                
        except Exception as e:
            print(f"[Research] Error cargando documentos: {e}")
            _vectorstore = _create_empty_vectorstore(embeddings, chroma_dir)
    else:
        print(f"[Research] No hay documentos para indexar")
        _vectorstore = _create_empty_vectorstore(embeddings, chroma_dir)
    
    # Crear retriever
    _retriever = _vectorstore.as_retriever(
        search_type="mmr",  # Maximum Marginal Relevance
        search_kwargs={
            "k": 4,           # Número de documentos a retornar
            "fetch_k": 10     # Número de documentos a considerar para MMR
        }
    )
    
    # Mostrar estadísticas
    stats = get_research_stats()
    print(f"[Research] Estadísticas: {stats}")
    
    return _vectorstore


def _create_empty_vectorstore(embeddings, chroma_dir: Path) -> Chroma:
    """Crea un vector store vacío."""
    return Chroma(
        embedding_function=embeddings,
        persist_directory=str(chroma_dir),
        collection_name="base_conocimientos"
    )


def get_retriever():
    """
    Obtiene el retriever, inicializando si es necesario.
    
    Returns:
        Retriever configurado para búsqueda MMR
    """
    global _retriever
    if _retriever is None:
        initialize_vectorstore()
    return _retriever


def search_documents(query: str, k: int = 4) -> List[Document]:
    """
    Busca documentos relevantes para una consulta.
    
    Args:
        query: Consulta de búsqueda
        k: Número de documentos a retornar
        
    Returns:
        Lista de documentos relevantes
    """
    retriever = get_retriever()
    retriever.search_kwargs["k"] = k
    return retriever.invoke(query)


def add_documents(documents: List[Document]) -> None:
    """
    Añade nuevos documentos al vector store.
    
    Args:
        documents: Lista de documentos a añadir
    """
    global _vectorstore
    if _vectorstore is None:
        initialize_vectorstore()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    _vectorstore.add_documents(chunks)
    print(f"[Research] Añadidos {len(chunks)} chunks al vector store")


def reset_vectorstore() -> None:
    """Reinicia el vector store (útil para testing o reindexación)."""
    global _vectorstore, _retriever
    _vectorstore = None
    _retriever = None
    print("[Research] Vector store reiniciado")