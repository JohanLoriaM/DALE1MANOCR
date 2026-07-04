# backend/app/exceptions.py

class ResourceNotFoundError(ValueError):
    """
    Excepción lanzada cuando un recurso solicitado no se encuentra en la base de datos.
    Hereda de ValueError para facilitar compatibilidad si se captura genéricamente.
    """
    pass
