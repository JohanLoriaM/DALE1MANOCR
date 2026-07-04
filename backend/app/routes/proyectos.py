from flask import Blueprint, request, jsonify
from ..dependencies import get_proyecto_service
from ..db import call_sp, db_instance
from ..exceptions import ResourceNotFoundError

proyectos_bp = Blueprint("proyectos", __name__, url_prefix="/api/proyectos")


@proyectos_bp.route("", methods=["GET"], strict_slashes=False)
def obtener_proyectos():
    """
    Ruta para obtener la lista de proyectos, opcionalmente filtrada por estado.
    """
    estado = request.args.get("estado")  # Puede ser ACTIVO, PASADO o None
    proyecto_service = get_proyecto_service()
    try:
        proyectos = proyecto_service.obtener_proyectos(estado)
        return jsonify(proyectos), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al obtener proyectos", "details": str(e)}), 500


@proyectos_bp.route("", methods=["POST"], strict_slashes=False)
def crear_proyecto():
    """
    Ruta para crear un proyecto (CU-09).
    """
    data = request.get_json() or {}
    id_tematica = data.get("id_tematica")
    titulo = data.get("titulo")
    descripcion = data.get("descripcion")
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")

    # Validar id_tematica si es proporcionado
    if id_tematica is not None:
        try:
            id_tematica = int(id_tematica)
        except (ValueError, TypeError):
            return jsonify({"error": "El ID de temática debe ser un número entero válido."}), 400

    proyecto_service = get_proyecto_service()
    try:
        proyecto_service.crear_proyecto(id_tematica, titulo, descripcion, fecha_inicio, fecha_fin)
        return jsonify({"status": "success", "message": "Proyecto creado exitosamente."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        if getattr(e, 'errno', None) == 1644:
            return jsonify({"error": e.msg if hasattr(e, 'msg') else str(e)}), 400
        return jsonify({"error": "Error al crear proyecto", "details": str(e)}), 500


@proyectos_bp.route("/<int:id_proyecto>", methods=["PUT"], strict_slashes=False)
def actualizar_proyecto(id_proyecto):
    """
    Ruta para actualizar un proyecto (CU-09).
    """
    data = request.get_json() or {}
    id_tematica = data.get("id_tematica")
    titulo = data.get("titulo")
    descripcion = data.get("descripcion")
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")

    # Validar id_tematica si es proporcionado
    if id_tematica is not None:
        try:
            id_tematica = int(id_tematica)
        except (ValueError, TypeError):
            return jsonify({"error": "El ID de temática debe ser un número entero válido."}), 400

    proyecto_service = get_proyecto_service()
    try:
        proyecto_service.actualizar_proyecto(id_proyecto, id_tematica, titulo, descripcion, fecha_inicio, fecha_fin)
        return jsonify({"status": "success", "message": "Proyecto actualizado exitosamente."}), 200
    except ResourceNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        if getattr(e, 'errno', None) == 1644:
            return jsonify({"error": e.msg if hasattr(e, 'msg') else str(e)}), 400
        return jsonify({"error": "Error al actualizar proyecto", "details": str(e)}), 500


@proyectos_bp.route("/<int:id_proyecto>/status", methods=["PATCH"], strict_slashes=False)
def actualizar_estado(id_proyecto):
    """
    Ruta para actualizar el estado del proyecto (ACTIVO, PASADO, CANCELADO).
    """
    data = request.get_json() or {}
    estado = data.get("estado")

    proyecto_service = get_proyecto_service()
    try:
        proyecto_service.actualizar_estado(id_proyecto, estado)
        return jsonify({"status": "success", "message": "Estado del proyecto actualizado."}), 200
    except ResourceNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al actualizar estado del proyecto", "details": str(e)}), 500


@proyectos_bp.route("/inscribir", methods=["POST"], strict_slashes=False)
def inscribir_usuario():
    """
    Ruta para inscribir un voluntario en un proyecto (CU-14) con patrón Observer.
    """
    data = request.get_json() or {}
    try:
        id_usuario = int(data.get("id_usuario"))
        id_proyecto = int(data.get("id_proyecto"))
    except (ValueError, TypeError):
        return jsonify({"error": "El usuario y el proyecto especificados deben ser números enteros válidos."}), 400

    proyecto_service = get_proyecto_service()
    try:
        proyecto_service.inscribir_usuario(id_usuario, id_proyecto)
        return jsonify({"status": "success", "message": "Usuario inscrito exitosamente."}), 200
    except Exception as e:
        if getattr(e, 'errno', None) == 1452:
            return jsonify({"error": "El usuario o proyecto especificado no existe."}), 400
        return jsonify({"error": str(e)}), 400


@proyectos_bp.route("/asistencia", methods=["POST"], strict_slashes=False)
def marcar_asistencia():
    """
    Ruta para marcar la asistencia de un voluntario (CU-14).
    """
    data = request.get_json() or {}
    try:
        id_usuario = int(data.get("id_usuario"))
        id_proyecto = int(data.get("id_proyecto"))
    except (ValueError, TypeError):
        return jsonify({"error": "El usuario y el proyecto especificados deben ser números enteros válidos."}), 400

    asistio = data.get("asistio")
    if asistio not in (True, False, 1, 0):
        return jsonify({"error": "El valor de asistencia debe ser booleano (true/false)."}), 400

    try:
        # Verificar inscripción
        conn = db_instance.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM Asistencias WHERE id_usuario = %s AND id_proyecto = %s",
            (id_usuario, id_proyecto)
        )
        exists = cursor.fetchone()[0] > 0
        cursor.close()
        db_instance.close_connection(conn)

        if not exists:
            return jsonify({"error": "El voluntario no está inscrito en este proyecto."}), 404

        call_sp("SP_MarcarAsistencia", (id_usuario, id_proyecto, asistio))
        return jsonify({"status": "success", "message": "Asistencia registrada exitosamente."}), 200
    except Exception as e:
        if getattr(e, 'errno', None) == 1452:
            return jsonify({"error": "El usuario o proyecto especificado no existe."}), 400
        return jsonify({"error": "Error al registrar asistencia", "details": str(e)}), 500