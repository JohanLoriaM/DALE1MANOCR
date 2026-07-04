from flask import Flask
from flask_cors import CORS
from .config import Config
from .routes.proyectos import proyectos_bp
from .routes.auth import auth_bp
from .routes.testimonios import testimonios_bp
from .routes.junta import junta_bp
from .routes.usuarios import usuarios_bp
from .routes.tematicas import tematicas_bp

def create_app():
    """
    Factory function para inicializar la aplicación Flask.
    Configura CORS, carga los parámetros del sistema y registra los blueprints de rutas.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Habilitar CORS para permitir solicitudes del Frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Registrar rutas (Blueprints) del sistema modular
    app.register_blueprint(proyectos_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(testimonios_bp)
    app.register_blueprint(junta_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(tematicas_bp)

    # Siembra de temáticas por defecto para cumplir con restricciones FK en Docker
    from .db import db_instance
    try:
        connection = db_instance.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Tematicas")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("INSERT INTO Tematicas (id_tematica, nombre, descripcion, estado) VALUES (1, 'Educación', 'Programas y tutorías', 'ACTIVO')")
            cursor.execute("INSERT INTO Tematicas (id_tematica, nombre, descripcion, estado) VALUES (2, 'Salud', 'Jornadas médicas', 'ACTIVO')")
            cursor.execute("INSERT INTO Tematicas (id_tematica, nombre, descripcion, estado) VALUES (3, 'Medio Ambiente', 'Reforestación', 'ACTIVO')")
            cursor.execute("INSERT INTO Tematicas (id_tematica, nombre, descripcion, estado) VALUES (4, 'Justicia Social', 'Derechos', 'ACTIVO')")
            connection.commit()
            print("Base de datos sembrada con temáticas por defecto.")
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Advertencia al sembrar temáticas: {e}")

    # Siembra de admin por defecto
    try:
        connection = db_instance.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE correo = 'admin@dale1mano.org'")
        admin_count = cursor.fetchone()[0]
        if admin_count == 0:
            import bcrypt
            contrasena_hash = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            cursor.execute(
                "INSERT INTO Usuarios (nombre_completo, correo, contrasena_hash, rol) VALUES (%s, %s, %s, %s)",
                ("Administrador Dale1Mano", "admin@dale1mano.org", contrasena_hash, "ADMIN")
            )
            connection.commit()
            print("Administrador sembrado en la base de datos.")
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Advertencia al sembrar administrador: {e}")

    return app