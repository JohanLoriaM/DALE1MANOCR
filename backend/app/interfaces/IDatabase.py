from abc import ABC, abstractmethod


class IDatabase(ABC):
    """
    Interfaz abstracta para el gestor de base de datos.
    """

    @abstractmethod
    def get_connection(self):
        """Retorna la conexión activa a la base de datos."""
        pass

    @abstractmethod
    def close_connection(self):
        """Cierra la conexión a la base de datos de forma segura."""
        pass
