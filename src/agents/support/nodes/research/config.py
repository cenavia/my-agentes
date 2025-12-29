"""
Configuración de rutas para el módulo de investigación.

Soporta tres modos de operación:
1. Variables de entorno (producción)
2. Rutas relativas al proyecto (desarrollo)
3. Rutas absolutas personalizadas
"""

import os
from pathlib import Path
from typing import Dict

class ResearchConfig:
    """Configuración centralizada del módulo de investigación."""
    
    def __init__(self):
        self._project_root = self._find_project_root()
        self._paths = self._initialize_paths()
    
    def _find_project_root(self) -> Path:
        """Encuentra la raíz del proyecto (donde está pyproject.toml)."""
        current = Path(__file__).resolve()
        
        # Buscar hacia arriba hasta encontrar pyproject.toml
        for parent in [current, *current.parents]:
            if (parent / "pyproject.toml").exists():
                return parent
        
        # Fallback: 5 niveles arriba desde este archivo
        return Path(__file__).parent.parent.parent.parent.parent
    
    def _initialize_paths(self) -> Dict[str, Path]:
        """Inicializa las rutas según configuración."""
        
        # 1. Intentar leer de variables de entorno
        documentos_dir = os.getenv("RESEARCH_DOCUMENTOS_DIR")
        datos_dir = os.getenv("RESEARCH_DATOS_DIR")
        
        # 2. Si no hay env vars, usar defaults en la raíz del proyecto
        if not documentos_dir:
            documentos_dir = self._project_root / "documentos"
        else:
            documentos_dir = Path(documentos_dir)
        
        if not datos_dir:
            datos_dir = self._project_root / "datos"
        else:
            datos_dir = Path(datos_dir)
        
        chroma_db_dir = datos_dir / "chroma_db"
        
        # 3. Crear directorios si no existen
        documentos_dir.mkdir(parents=True, exist_ok=True)
        datos_dir.mkdir(parents=True, exist_ok=True)
        chroma_db_dir.mkdir(parents=True, exist_ok=True)
        
        # 4. Crear archivo de ejemplo si el directorio está vacío
        readme_file = documentos_dir / "README.txt"
        if not list(documentos_dir.glob("*.txt")) and not readme_file.exists():
            readme_file.write_text(
                "=== DOCUMENTOS DE INVESTIGACIÓN ===\n\n"
                "Coloca aquí tus documentos de investigación en formato .txt o .pdf\n"
                "Estos archivos serán indexados automáticamente por el sistema RAG.\n\n"
                "Formatos soportados:\n"
                "- .txt (texto plano)\n"
                "- .pdf (archivos PDF)\n\n"
                "Los documentos se procesarán la próxima vez que inicies el agente.\n"
            )
        
        return {
            "project_root": self._project_root,
            "documentos": documentos_dir,
            "datos": datos_dir,
            "chroma_db": chroma_db_dir,
        }
    
    @property
    def documentos_dir(self) -> Path:
        """Directorio donde el usuario coloca sus documentos."""
        return self._paths["documentos"]
    
    @property
    def datos_dir(self) -> Path:
        """Directorio raíz de datos generados."""
        return self._paths["datos"]
    
    @property
    def chroma_db_dir(self) -> Path:
        """Directorio de la base de datos vectorial."""
        return self._paths["chroma_db"]
    
    @property
    def project_root(self) -> Path:
        """Raíz del proyecto."""
        return self._paths["project_root"]
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas de los directorios."""
        
        def count_files(directory: Path, pattern: str = "*") -> int:
            return len(list(directory.glob(pattern)))
        
        def dir_size(directory: Path) -> int:
            """Calcula el tamaño total del directorio en bytes."""
            total = 0
            for path in directory.rglob("*"):
                if path.is_file():
                    total += path.stat().st_size
            return total
        
        return {
            "documentos": {
                "path": str(self.documentos_dir),
                "txt_files": count_files(self.documentos_dir, "*.txt"),
                "pdf_files": count_files(self.documentos_dir, "*.pdf"),
                "total_files": count_files(self.documentos_dir),
            },
            "chroma_db": {
                "path": str(self.chroma_db_dir),
                "exists": self.chroma_db_dir.exists(),
                "size_mb": dir_size(self.chroma_db_dir) / (1024 * 1024) if self.chroma_db_dir.exists() else 0,
            }
        }


# ====================================
# Singleton global
# ====================================
_config = None

def get_config() -> ResearchConfig:
    """Obtiene la configuración singleton."""
    global _config
    if _config is None:
        _config = ResearchConfig()
    return _config


# ====================================
# Exports convenientes
# ====================================
def get_documentos_dir() -> Path:
    """Obtiene el directorio de documentos."""
    return get_config().documentos_dir

def get_datos_dir() -> Path:
    """Obtiene el directorio de datos."""
    return get_config().datos_dir

def get_chroma_db_dir() -> Path:
    """Obtiene el directorio de ChromaDB."""
    return get_config().chroma_db_dir

def get_research_stats() -> Dict:
    """Obtiene estadísticas de uso."""
    return get_config().get_stats()