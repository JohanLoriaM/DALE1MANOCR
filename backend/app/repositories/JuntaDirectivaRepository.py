from ..interfaces.IJuntaDirectivaRepository import IJuntaDirectivaRepository
from ..db import db_instance, call_sp


class JuntaDirectivaRepository(IJuntaDirectivaRepository):

    def __init__(self, db_provider=db_instance):
        self.db = db_provider

    def obtener_miembros(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc('SP_ObtenerJuntaDirectiva')
            resultados = next(cursor.stored_results()).fetchall()
            return resultados
        except Exception as e:
            raise e
        finally:
            cursor.close()
            self.db.close_connection(conn)

    def crear_miembro(self, nombre_completo: str, cargo: str, url_fotografia: str, orden_jerarquia: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Junta_Directiva (nombre_completo, cargo, url_fotografia, orden_jerarquia) VALUES (%s, %s, %s, %s)",
                (nombre_completo, cargo, url_fotografia, orden_jerarquia)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.db.close_connection(conn)

    def actualizar_miembro(self, id_miembro: int, nombre_completo: str, cargo: str, url_foto: str, orden_jerarquia: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            # Verificar si existe el miembro
            cursor.execute("SELECT COUNT(*) FROM Junta_Directiva WHERE id_miembro = %s", (id_miembro,))
            if cursor.fetchone()[0] == 0:
                from ..exceptions import ResourceNotFoundError
                raise ResourceNotFoundError("El miembro de la junta especificado no existe.")

            cursor.execute(
                "UPDATE Junta_Directiva SET nombre_completo = %s, cargo = %s, url_fotografia = %s, orden_jerarquia = %s WHERE id_miembro = %s",
                (nombre_completo, cargo, url_foto, orden_jerarquia, id_miembro)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.db.close_connection(conn)

    def eliminar_miembro(self, id_miembro: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            # Verificar si existe el miembro
            cursor.execute("SELECT COUNT(*) FROM Junta_Directiva WHERE id_miembro = %s", (id_miembro,))
            if cursor.fetchone()[0] == 0:
                from ..exceptions import ResourceNotFoundError
                raise ResourceNotFoundError("El miembro de la junta especificado no existe.")

            cursor.execute(
                "DELETE FROM Junta_Directiva WHERE id_miembro = %s",
                (id_miembro,)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.db.close_connection(conn)