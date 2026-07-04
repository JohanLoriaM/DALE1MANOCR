from typing import Optional
from ..interfaces.IObserver import ISubject, IObserver
from ..patterns.observers import AuditLogObserver, EmailNotificationObserver
from ..repositories.ProyectoRepository import ProyectoRepository


class ProyectoService(ISubject):
    def __init__(self, repository=None):
        """Constructor corregido y adaptado para la inyección de dependencias en Docker."""
        super().__init__()
        self._observers = []
        # Si no nos pasan un repositorio, instanciamos el predeterminado
        self.repository = repository if repository is not None else ProyectoRepository()

        self.attach(AuditLogObserver())
        self.attach(EmailNotificationObserver())

    def attach(self, observer: IObserver):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IObserver):
        self._observers.remove(observer)

    def notify(self, event_type: str, data: dict):
        for observer in self._observers:
            observer.update(event_type, data)

    def obtener_proyectos(self, estado: Optional[str] = None):
        return self.repository.obtener_proyectos(estado)

    def crear_proyecto(self, id_tematica: Optional[int], titulo: str, descripcion: str, fecha_inicio: str, fecha_fin: str):
        if not titulo or not descripcion or not fecha_inicio or not fecha_fin:
            raise ValueError("El título, descripción y fechas de inicio/fin son obligatorios.")
        return self.repository.crear_proyecto(id_tematica, titulo, descripcion, fecha_inicio, fecha_fin)

    def actualizar_proyecto(self, id_proyecto: int, id_tematica: Optional[int], titulo: str, descripcion: str, fecha_inicio: str, fecha_fin: str):
        if not id_proyecto or not titulo or not descripcion or not fecha_inicio or not fecha_fin:
            raise ValueError("El ID, título, descripción y fechas son obligatorios.")
        return self.repository.actualizar_proyecto(id_proyecto, id_tematica, titulo, descripcion, fecha_inicio, fecha_fin)

    def actualizar_estado(self, id_proyecto: int, estado: str):
        if not id_proyecto or not estado:
            raise ValueError("El ID del proyecto y el estado son obligatorios.")
        if estado not in ["ACTIVO", "PASADO", "CANCELADO"]:
            raise ValueError("Estado no permitido.")
        return self.repository.actualizar_estado(id_proyecto, estado)

    def inscribir_usuario(self, id_usuario: int, id_proyecto: int):
        try:
            resultado = self.repository.inscribir_usuario(
                id_usuario, id_proyecto)

            self.notify("NUEVA_INSCRIPCION", {
                "id_usuario": id_usuario,
                "id_proyecto": id_proyecto
            })

            return resultado
        except Exception as e:
            raise e
