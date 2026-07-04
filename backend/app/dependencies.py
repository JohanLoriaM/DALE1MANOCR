from .repositories.ProyectoRepository import ProyectoRepository
from .repositories.AuthRepository import AuthRepository
from .services.ProyectoService import ProyectoService
from .services.AuthService import AuthService

_proyecto_repo = ProyectoRepository()
# Pasamos el parámetro de forma explícita por nombre (keyword argument)
_proyecto_service = ProyectoService(repository=_proyecto_repo)

_auth_repo = AuthRepository()
# Hacemos lo mismo para el servicio de autenticación
_auth_service = AuthService(repository=_auth_repo)

def get_proyecto_service() -> ProyectoService:
    """Retorna la instancia del servicio de proyectos con sus dependencias resueltas."""
    return _proyecto_service

def get_auth_service() -> AuthService:
    """Retorna la instancia del servicio de autenticación con sus dependencias resueltas."""
    return _auth_service