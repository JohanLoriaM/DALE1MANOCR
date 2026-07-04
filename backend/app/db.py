import mysql.connector
from .config import Config
from .interfaces.IDatabase import IDatabase

class MySQLDatabase(IDatabase):
    """
    Implementación concreta de IDatabase usando mysql-connector-python.
    """
    def __init__(self):
        self.config = {
            'host': Config.MYSQL_HOST,
            'user': Config.MYSQL_USER,
            'password': Config.MYSQL_PASSWORD,
            'database': Config.MYSQL_DB,
            'port': Config.MYSQL_PORT
        }

    def get_connection(self):
        """Cumple con el contrato de IDatabase para abrir conexiones."""
        return mysql.connector.connect(**self.config)

    def close_connection(self, connection):
        """Cumple con el contrato de IDatabase para liberar conexiones."""
        if connection and connection.is_connected():
            connection.close()

    def execute_procedure(self, procedure_name, params=()):
        """Ejecuta un procedimiento almacenado de forma segura."""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)

            # Ejecutar el SP
            cursor.callproc(procedure_name, params)

            # Recuperar los resultados de los datasets devueltos
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())

            connection.commit()
            return results
        except mysql.connector.Error as err:
            print(f"Error en Base de Datos: {err}")
            raise err
        finally:
            if cursor:
                cursor.close()
            self.close_connection(connection)

# Instancia global corregida para que los repositorios la importen correctamente
db_instance = MySQLDatabase()

def call_sp(procedure_name, params=()):
    """Función puente para mantener compatibilidad con los repositorios existentes."""
    return db_instance.execute_procedure(procedure_name, params)