from abc import ABC, abstractmethod


class ITestimoniosRepository(ABC):

    @abstractmethod
    def obtener_todos_aprobados(self):
        pass

    @abstractmethod
    def obtener_todos(self):
        pass

    @abstractmethod
    def aprobar(self, id_testimonio: int):
        pass

    @abstractmethod
    def eliminar(self, id_testimonio: int):
        pass

    @abstractmethod
    def crear(self, id_usuario: int, id_proyecto: int, contenido: str, url_video: str):
        pass