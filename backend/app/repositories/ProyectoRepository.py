from typing import Optional
import mysql.connector
from ..interfaces.IProyectoRepository import IProyectoRepository
from ..db import call_sp, db_instance


class ProyectoRepository(IProyectoRepository):
    """
    Implementación concreta de IProyectoRepository usando MySQL stored procedures.
    """

    def clean_datetime(self, iso_str: str) -> str:
        if not iso_str:
            return ""
        # Convierte "2026-07-15T09:00:00.000Z" a "2026-07-15 09:00:00"
        return iso_str.replace("T", " ").replace("Z", "").split(".")[0]

    def obtener_proyectos(self, estado: Optional[str]) -> list:
        # call_sp recibe el nombre del SP y sus argumentos como tupla
        # SP_ObtenerProyectos(IN p_estado VARCHAR(20))
        return call_sp("SP_ObtenerProyectos", (estado,))

    def obtener_por_id(self, id_proyecto: int) -> Optional[dict]:
        proyectos = self.obtener_proyectos(None)
        for p in proyectos:
            if p["id_proyecto"] == id_proyecto:
                return p
        return None

    def crear_proyecto(self, id_tematica: Optional[int], titulo: str, descripcion: str, fecha_inicio: str, fecha_fin: str) -> None:
        call_sp("SP_CrearProyecto", (id_tematica, titulo, descripcion, self.clean_datetime(fecha_inicio), self.clean_datetime(fecha_fin)))

    def actualizar_proyecto(self, id_proyecto: int, id_tematica: Optional[int], titulo: str, descripcion: str, fecha_inicio: str, fecha_fin: str) -> None:
        if not self.obtener_por_id(id_proyecto):
            from ..exceptions import ResourceNotFoundError
            raise ResourceNotFoundError("El proyecto especificado no existe.")
        call_sp("SP_ActualizarProyecto", (id_proyecto, id_tematica, titulo, descripcion, self.clean_datetime(fecha_inicio), self.clean_datetime(fecha_fin)))

    def inscribir_usuario(self, id_usuario: int, id_proyecto: int) -> None:
        call_sp("SP_InscribirProyecto", (id_usuario, id_proyecto))

    def actualizar_estado(self, id_proyecto: int, estado: str) -> None:
        if not self.obtener_por_id(id_proyecto):
            from ..exceptions import ResourceNotFoundError
            raise ResourceNotFoundError("El proyecto especificado no existe.")

        connection = None
        cursor = None
        try:
            connection = db_instance.get_connection()
            cursor = connection.cursor()
            cursor.execute("UPDATE Proyectos SET estado = %s WHERE id_proyecto = %s", (estado, id_proyecto))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error actualizando estado del proyecto: {err}")
            raise err
        finally:
            if cursor:
                cursor.close()
            db_instance.close_connection(connection)