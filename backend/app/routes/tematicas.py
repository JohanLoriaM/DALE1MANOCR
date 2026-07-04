from flask import Blueprint, jsonify, request
from ..db import db_instance

tematicas_bp = Blueprint('tematicas_bp', __name__)


@tematicas_bp.route('/api/tematicas', methods=['GET'])
def listar_tematicas():
    """Lista todas las temáticas de la base de datos."""
    conn = db_instance.get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_tematica, nombre, descripcion, estado FROM Tematicas ORDER BY nombre ASC")
        resultados = cursor.fetchall()
        return jsonify({"status": "success", "data": resultados}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        db_instance.close_connection(conn)


@tematicas_bp.route('/api/tematicas', methods=['POST'])
def crear_tematica():
    """Crea una nueva temática en la base de datos."""
    datos = request.get_json() or {}
    nombre = datos.get('nombre')
    descripcion = datos.get('descripcion', '')

    if not nombre or not nombre.strip():
        return jsonify({"status": "error", "message": "El nombre de la temática es obligatorio."}), 400

    conn = db_instance.get_connection()
    cursor = conn.cursor()
    try:
        # Verificar duplicados
        cursor.execute("SELECT COUNT(*) FROM Tematicas WHERE nombre = %s", (nombre.strip(),))
        if cursor.fetchone()[0] > 0:
            return jsonify({"status": "error", "message": "Ya existe una temática con este nombre."}), 400

        cursor.execute(
            "INSERT INTO Tematicas (nombre, descripcion, estado) VALUES (%s, %s, 'ACTIVO')",
            (nombre.strip(), descripcion)
        )
        conn.commit()
        return jsonify({"status": "success", "message": "Temática creada correctamente."}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        db_instance.close_connection(conn)


@tematicas_bp.route('/api/tematicas/<int:id_tematica>', methods=['PUT'])
def actualizar_tematica(id_tematica):
    """Actualiza una temática existente."""
    datos = request.get_json() or {}
    nombre = datos.get('nombre')
    descripcion = datos.get('descripcion')
    estado = datos.get('estado')

    if nombre is not None and not nombre.strip():
        return jsonify({"status": "error", "message": "El nombre de la temática no puede estar vacío."}), 400

    if estado is not None and estado not in ('ACTIVO', 'INACTIVO'):
        return jsonify({"status": "error", "message": "Estado inválido."}), 400

    conn = db_instance.get_connection()
    cursor = conn.cursor()
    try:
        # Verificar si la temática existe
        cursor.execute("SELECT COUNT(*) FROM Tematicas WHERE id_tematica = %s", (id_tematica,))
        if cursor.fetchone()[0] == 0:
            return jsonify({"status": "error", "message": "La temática especificada no existe."}), 404

        # Construir campos a actualizar dinámicamente
        updates = []
        params = []
        if nombre is not None:
            updates.append("nombre = %s")
            params.append(nombre.strip())
        if descripcion is not None:
            updates.append("descripcion = %s")
            params.append(descripcion)
        if estado is not None:
            updates.append("estado = %s")
            params.append(estado)

        if not updates:
            return jsonify({"status": "success", "message": "No se especificaron cambios."}), 200

        params.append(id_tematica)
        cursor.execute(f"UPDATE Tematicas SET {', '.join(updates)} WHERE id_tematica = %s", tuple(params))
        conn.commit()
        return jsonify({"status": "success", "message": "Temática actualizada correctamente."}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        db_instance.close_connection(conn)


@tematicas_bp.route('/api/tematicas/<int:id_tematica>', methods=['DELETE'])
def eliminar_tematica(id_tematica):
    """Elimina físicamente una temática de la base de datos."""
    conn = db_instance.get_connection()
    cursor = conn.cursor()
    try:
        # Verificar si la temática existe
        cursor.execute("SELECT COUNT(*) FROM Tematicas WHERE id_tematica = %s", (id_tematica,))
        if cursor.fetchone()[0] == 0:
            return jsonify({"status": "error", "message": "La temática especificada no existe."}), 404

        cursor.execute("DELETE FROM Tematicas WHERE id_tematica = %s", (id_tematica,))
        conn.commit()
        return jsonify({"status": "success", "message": "Temática eliminada correctamente."}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        db_instance.close_connection(conn)
