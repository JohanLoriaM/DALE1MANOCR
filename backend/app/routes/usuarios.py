from flask import Blueprint, jsonify, request
from ..db import call_sp, db_instance

usuarios_bp = Blueprint('usuarios_bp', __name__)


@usuarios_bp.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    """
    Lista todos los usuarios de la base de datos con todos sus campos.
    Fallback a query directa si SP_BuscarUsuarios no devuelve 'estado'.
    """
    conn = db_instance.get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id_usuario, nombre_completo, correo, rol, es_miembro_oficial, "
            "fecha_registro, estado FROM Usuarios ORDER BY fecha_registro DESC"
        )
        resultados = cursor.fetchall()
        # Serializar datetime/date a string ISO para JSON
        for r in resultados:
            if r.get("fecha_registro"):
                r["fecha_registro"] = r["fecha_registro"].isoformat()
            # Convertir tinyint(1) a bool nativo Python
            r["es_miembro_oficial"] = bool(r.get("es_miembro_oficial", 0))
        return jsonify({"status": "success", "data": resultados}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        db_instance.close_connection(conn)


@usuarios_bp.route('/api/usuarios/<int:id_usuario>/promover', methods=['POST'])
def promover_usuario(id_usuario):
    """Promueve al usuario a miembro oficial (es_miembro_oficial = TRUE)."""
    conn = db_instance.get_connection()
    cursor = conn.cursor()
    try:
        # Verificar si el usuario existe
        cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE id_usuario = %s", (id_usuario,))
        if cursor.fetchone()[0] == 0:
            return jsonify({"status": "error", "message": "El usuario especificado no existe."}), 404

        cursor.execute(
            "UPDATE Usuarios SET es_miembro_oficial = TRUE WHERE id_usuario = %s",
            (id_usuario,)
        )
        conn.commit()
        return jsonify({"status": "success", "message": "Usuario promovido a miembro oficial correctamente."}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        db_instance.close_connection(conn)


@usuarios_bp.route('/api/usuarios/<int:id_usuario>/status', methods=['POST'])
def cambiar_estado(id_usuario):
    """Activa o inactiva la cuenta de un voluntario."""
    datos = request.get_json() or {}
    nuevo_estado = datos.get('estado')
    if nuevo_estado not in ('ACTIVO', 'INACTIVO'):
        return jsonify({"status": "error", "message": "Estado inválido."}), 400

    conn = db_instance.get_connection()
    cursor = conn.cursor()
    try:
        # Verificar si el usuario existe
        cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE id_usuario = %s", (id_usuario,))
        if cursor.fetchone()[0] == 0:
            return jsonify({"status": "error", "message": "El usuario especificado no existe."}), 404

        cursor.execute("UPDATE Usuarios SET estado = %s WHERE id_usuario = %s", (nuevo_estado, id_usuario))
        conn.commit()
        return jsonify({"status": "success", "message": "Estado de usuario actualizado correctamente."}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        db_instance.close_connection(conn)


@usuarios_bp.route('/api/usuarios/<int:id_usuario>/rol', methods=['POST'])
def cambiar_rol(id_usuario):
    """Cambia el rol del usuario entre ADMIN y USER."""
    datos = request.get_json() or {}
    nuevo_rol = datos.get('rol')
    if nuevo_rol not in ('ADMIN', 'USER'):
        return jsonify({"status": "error", "message": "Rol inválido."}), 400

    conn = db_instance.get_connection()
    cursor = conn.cursor()
    try:
        # Verificar si el usuario existe
        cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE id_usuario = %s", (id_usuario,))
        if cursor.fetchone()[0] == 0:
            return jsonify({"status": "error", "message": "El usuario especificado no existe."}), 404

        cursor.execute("UPDATE Usuarios SET rol = %s WHERE id_usuario = %s", (nuevo_rol, id_usuario))
        conn.commit()
        return jsonify({"status": "success", "message": "Rol de usuario actualizado correctamente."}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        db_instance.close_connection(conn)


@usuarios_bp.route('/api/asistencias', methods=['GET'])
def listar_asistencias():
    """Lista todas las asistencias/inscripciones de la base de datos."""
    conn = db_instance.get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id_asistencia, id_usuario, id_proyecto, fecha_inscripcion, asistio "
            "FROM Asistencias ORDER BY fecha_inscripcion DESC"
        )
        resultados = cursor.fetchall()
        for r in resultados:
            if r.get("fecha_inscripcion"):
                r["fecha_inscripcion"] = r["fecha_inscripcion"].isoformat()
            r["asistio"] = bool(r.get("asistio", 0))
        return jsonify({"status": "success", "data": resultados}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        db_instance.close_connection(conn)


@usuarios_bp.route('/api/top-voluntarios', methods=['GET'])
def top_voluntarios():
    """Retorna los 5 voluntarios con más asistencias confirmadas para el dashboard."""
    conn = db_instance.get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT u.id_usuario, u.nombre_completo, u.correo, u.es_miembro_oficial, "
            "COUNT(a.id_proyecto) AS total_asistencias "
            "FROM Usuarios u "
            "INNER JOIN Asistencias a ON u.id_usuario = a.id_usuario "
            "WHERE a.asistio = TRUE "
            "GROUP BY u.id_usuario, u.nombre_completo, u.correo, u.es_miembro_oficial "
            "ORDER BY total_asistencias DESC LIMIT 5"
        )
        resultados = cursor.fetchall()
        for r in resultados:
            r["es_miembro_oficial"] = bool(r.get("es_miembro_oficial", 0))
        return jsonify({"status": "success", "data": resultados}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        db_instance.close_connection(conn)
