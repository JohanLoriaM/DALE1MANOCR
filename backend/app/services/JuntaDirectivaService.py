from ..repositories.JuntaDirectivaRepository import JuntaDirectivaRepository
from ..interfaces.IJuntaDirectivaRepository import IJuntaDirectivaRepository


class JuntaDirectivaService:

    def __init__(self, repository: IJuntaDirectivaRepository = None):
        # Si no se inyecta un repositorio, se utiliza la implementación concreta por defecto
        self.repository = repository if repository is not None else JuntaDirectivaRepository()

    def listar_miembros(self):
        try:
            return self.repository.obtener_miembros()
        except Exception as e:
            raise e

    def crear_miembro(self, nombre_completo: str, cargo: str, url_fotografia: str, orden_jerarquia: int):
        try:
            if not nombre_completo or not cargo or orden_jerarquia < 1:
                raise ValueError("El nombre, cargo y orden de jerarquía son obligatorios.")
            return self.repository.crear_miembro(nombre_completo, cargo, url_fotografia, orden_jerarquia)
        except Exception as e:
            raise e

    def modificar_perfil_miembro(self, id_miembro: int, nombre_completo: str, cargo: str, url_foto: str, orden_jerarquia: int):
        try:
            if not cargo or not nombre_completo or orden_jerarquia < 1:
                raise ValueError("El nombre, cargo y orden de jerarquía son obligatorios.")
            return self.repository.actualizar_miembro(id_miembro, nombre_completo, cargo, url_foto, orden_jerarquia)
        except Exception as e:
            raise e

    def eliminar_miembro(self, id_miembro: int):
        try:
            return self.repository.eliminar_miembro(id_miembro)
        except Exception as e:
            raise e