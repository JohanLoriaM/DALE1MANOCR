from abc import ABC, abstractmethod
from typing import Optional


class IProyectoRepository(ABC):
    """
    Interfaz del repositorio de proyectos.
    Define el contrato que cualquier implementación de acceso a datos debe cumplir.
    Principio: DIP — la lógica de negocio depende de esta abstracción, no de MySQL.
    """

    @abstractmethod
    def obtener_proyectos(self, estado: Optional[str]) -> list:
        """Retorna todos los proyectos, filtrados por estado si se indica."""
        pass

    @abstractmethod
    def obtener_por_id(self, id_proyecto: int) -> Optional[dict]:
        """Retorna un proyecto por su ID, o None si no existe."""
        pass

    @abstractmethod
    def crear_proyecto(self, id_tematica: Optional[int], titulo: str, descripcion: str, fecha_inicio: str, fecha_fin: str) -> None:
        """Crea un nuevo proyecto en la base de datos."""
        pass

    @abstractmethod
    def actualizar_proyecto(self, id_proyecto: int, id_tematica: Optional[int], titulo: str, descripcion: str, fecha_inicio: str, fecha_fin: str) -> None:
        """Actualiza un proyecto existente en la base de datos."""
        pass

    @abstractmethod
    def inscribir_usuario(self, id_usuario: int, id_proyecto: int) -> None:
        """Inscribe un usuario en un proyecto."""
        pass

    @abstractmethod
    def actualizar_estado(self, id_proyecto: int, estado: str) -> None:
        """Actualiza el estado de un proyecto."""
        pass
