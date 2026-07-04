from flask import Blueprint, jsonify, request
from ..services.JuntaDirectivaService import JuntaDirectivaService
from ..exceptions import ResourceNotFoundError

junta_bp = Blueprint('junta_bp', __name__)
service = JuntaDirectivaService()


@junta_bp.route('/api/junta', methods=['GET'])
def listar_miembros():
    try:
        miembros = service.listar_miembros()
        return jsonify({"status": "success", "data": miembros}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@junta_bp.route('/api/junta', methods=['POST'])
def crear_miembro():
    try:
        datos = request.get_json() or {}
        nombre_completo = datos.get('nombre_completo')
        cargo = datos.get('cargo')
        url_fotografia = datos.get('url_fotografia') or datos.get('url_foto')
        
        # Validar y castear orden_jerarquia
        try:
            orden_jerarquia = int(datos.get('orden_jerarquia', 1))
        except (ValueError, TypeError):
            return jsonify({"status": "error", "message": "El orden de jerarquía debe ser un número entero válido."}), 400

        service.crear_miembro(nombre_completo, cargo, url_fotografia, orden_jerarquia)
        return jsonify({"status": "success", "message": "Miembro creado correctamente"}), 201
    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@junta_bp.route('/api/junta/<int:id_miembro>', methods=['PUT'])
def actualizar_miembro(id_miembro):
    try:
        datos = request.get_json() or {}
        nombre_completo = datos.get('nombre_completo')
        cargo = datos.get('cargo')
        url_foto = datos.get('url_fotografia') or datos.get('url_foto')

        # Validar y castear orden_jerarquia
        try:
            orden_jerarquia = int(datos.get('orden_jerarquia', 1))
        except (ValueError, TypeError):
            return jsonify({"status": "error", "message": "El orden de jerarquía debe ser un número entero válido."}), 400

        service.modificar_perfil_miembro(id_miembro, nombre_completo, cargo, url_foto, orden_jerarquia)
        return jsonify({"status": "success", "message": "Miembro actualizado correctamente"}), 200
    except ResourceNotFoundError as rne:
        return jsonify({"status": "error", "message": str(rne)}), 404
    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@junta_bp.route('/api/junta/<int:id_miembro>', methods=['DELETE'])
def eliminar_miembro(id_miembro):
    try:
        service.eliminar_miembro(id_miembro)
        return jsonify({"status": "success", "message": "Miembro eliminado correctamente"}), 200
    except ResourceNotFoundError as rne:
        return jsonify({"status": "error", "message": str(rne)}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500