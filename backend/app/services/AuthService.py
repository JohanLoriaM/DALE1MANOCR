import datetime
import bcrypt
import jwt
from flask import current_app
from typing import Optional
from ..interfaces.IAuthRepository import IAuthRepository
from ..repositories.AuthRepository import AuthRepository


class AuthService:
    """
    Servicio de autenticación (Lógica de Negocio).
    Sigue el principio de Inversión de Dependencias (DIP) al depender de IAuthRepository.
    """

    def __init__(self, repository: IAuthRepository = None):
        """Constructor corregido para aceptar inyección estándar o instanciar por defecto."""
        self.repository = repository if repository is not None else AuthRepository()

    def registrar_usuario(self, nombre: str, correo: str, contrasena: str) -> None:
        if not nombre or not correo or not contrasena:
            raise ValueError("Todos los campos (nombre, correo, contrasena) son obligatorios.")

        import re
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_correo, correo):
            raise ValueError("El formato de correo no es válido.")

        if len(contrasena) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")

        # Hashear la contraseña con bcrypt
        salt = bcrypt.gensalt()
        contrasena_hash = bcrypt.hashpw(contrasena.encode("utf-8"), salt).decode("utf-8")

        # Guardar en repositorio
        self.repository.registrar_usuario(nombre, correo, contrasena_hash)

    def login(self, correo: str, contrasena: str) -> dict:
        if not correo or not contrasena:
            raise ValueError("El correo y la contraseña son obligatorios.")

        # Obtener el usuario de la BD
        user = self.repository.obtener_usuario_por_correo(correo)
        if not user:
            raise ValueError("Credenciales inválidas o cuenta inactiva.")

        # Verificar contraseña
        hashed_password = user["contrasena_hash"]
        if not bcrypt.checkpw(contrasena.encode("utf-8"), hashed_password.encode("utf-8")):
            raise ValueError("Credenciales inválidas.")

        # Generar JWT Token
        secret = current_app.config["JWT_SECRET_KEY"]
        expiration_hours = current_app.config["JWT_EXPIRATION_H"]

        payload = {
            "id_usuario": user["id_usuario"],
            "nombre": user["nombre_completo"],
            "rol": user["rol"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=expiration_hours)
        }

        token = jwt.encode(payload, secret, algorithm="HS256")

        return {
            "token": token,
            "adminId": user["id_usuario"],
            "nombre": user["nombre_completo"],
            "usuario": {
                "id_usuario": user["id_usuario"],
                "nombre_completo": user["nombre_completo"],
                "correo": correo,
                "rol": user["rol"]
            }
        }