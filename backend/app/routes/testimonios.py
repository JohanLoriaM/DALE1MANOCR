from flask import Blueprint, jsonify, request
from ..services.TestimoniosService import TestimoniosService
from ..exceptions import ResourceNotFoundError

testimonios_bp = Blueprint('testimonios_bp', __name__)
service = TestimoniosService()


@testimonios_bp.route('/api/testimonios', methods=['GET'])
def get_testimonios():
    try:
        # Por simplicidad, retornamos todos los testimonios (aprobados y pendientes)
        # El frontend se encarga de filtrarlos (Home filtra solo aprobados, Admin clasifica ambos)
        datos = service.obtener_todos()
        return jsonify({"status": "success", "data": datos}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@testimonios_bp.route('/api/testimonios', methods=['POST'])
def crear_testimonio():
    try:
        datos = request.get_json() or {}
        
        # Validar y castear id_usuario e id_proyecto
        try:
            id_usuario = int(datos.get('id_usuario'))
            id_proyecto = int(datos.get('id_proyecto'))
        except (ValueError, TypeError):
            return jsonify({"status": "error", "message": "El usuario y el proyecto especificados deben ser números enteros válidos."}), 400

        contenido = datos.get('contenido')
        url_video = datos.get('url_video')

        service.crear_testimonio(id_usuario, id_proyecto, contenido, url_video)
        return jsonify({"status": "success", "message": "Testimonio registrado para revisión."}), 201
    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as e:
        if getattr(e, 'errno', None) == 1452:
            return jsonify({"status": "error", "message": "El usuario o proyecto especificado no existe."}), 400
        return jsonify({"status": "error", "message": str(e)}), 500


@testimonios_bp.route('/api/testimonios/<int:id_testimonio>/aprobar', methods=['POST'])
def aprobar_testimonio(id_testimonio):
    try:
        service.aprobar_testimonio(id_testimonio)
        return jsonify({"status": "success", "message": "Testimonio aprobado correctamente"}), 200
    except ResourceNotFoundError as rne:
        return jsonify({"status": "error", "message": str(rne)}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@testimonios_bp.route('/api/testimonios/<int:id_testimonio>', methods=['DELETE'])
def eliminar_testimonio(id_testimonio):
    try:
        service.eliminar_testimonio(id_testimonio)
        return jsonify({"status": "success", "message": "Testimonio rechazado/eliminado correctamente"}), 200
    except ResourceNotFoundError as rne:
        return jsonify({"status": "error", "message": str(rne)}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500