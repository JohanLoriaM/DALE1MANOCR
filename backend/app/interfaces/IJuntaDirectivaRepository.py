from abc import ABC, abstractmethod


class IJuntaDirectivaRepository(ABC):

    @abstractmethod
    def obtener_miembros(self):
        pass

    @abstractmethod
    def crear_miembro(self, nombre_completo: str, cargo: str, url_fotografia: str, orden_jerarquia: int):
        pass

    @abstractmethod
    def actualizar_miembro(self, id_miembro: int, nombre_completo: str, cargo: str, url_foto: str, orden_jerarquia: int):
        pass

    @abstractmethod
    def eliminar_miembro(self, id_miembro: int):
        pass