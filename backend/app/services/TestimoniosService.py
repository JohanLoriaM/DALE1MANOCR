from ..repositories.TestimoniosRepository import TestimoniosRepository
from ..interfaces.ITestimoniosRepository import ITestimoniosRepository


class TestimoniosService:

    def __init__(self, repository: ITestimoniosRepository = None):
        """Constructor corregido con importaciones relativas."""
        self.repository = repository if repository is not None else TestimoniosRepository()

    def obtener_testimonios_publicos(self):
        try:
            return self.repository.obtener_todos_aprobados()
        except Exception as e:
            raise e

    def obtener_todos(self):
        try:
            return self.repository.obtener_todos()
        except Exception as e:
            raise e

    def aprobar_testimonio(self, id_testimonio: int):
        try:
            return self.repository.aprobar(id_testimonio)
        except Exception as e:
            raise e

    def eliminar_testimonio(self, id_testimonio: int):
        try:
            return self.repository.eliminar(id_testimonio)
        except Exception as e:
            raise e

    def crear_testimonio(self, id_usuario: int, id_proyecto: int, contenido: str, url_video: str):
        try:
            if not id_usuario or not id_proyecto or not contenido:
                raise ValueError("El usuario, el proyecto y el contenido son obligatorios.")
            return self.repository.crear(id_usuario, id_proyecto, contenido, url_video)
        except Exception as e:
            raise e