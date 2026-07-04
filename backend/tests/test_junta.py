from unittest.mock import MagicMock

def test_listar_miembros_junta(client, mock_db):
    miembros_mock = [
        {"id_miembro": 1, "nombre_completo": "Miembro Uno", "cargo": "Presidente", "url_fotografia": "http://foto.jpg"}
    ]
    # Configurar mock para stored_results del cursor
    mock_result = MagicMock()
    mock_result.fetchall.return_value = miembros_mock
    mock_db['cursor'].stored_results.return_value = iter([mock_result])
    
    response = client.get("/api/junta")
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert len(response.json["data"]) == 1
    assert response.json["data"][0]["nombre_completo"] == "Miembro Uno"

def test_crear_miembro_junta_exitoso(client, mock_db):
    payload = {
        "nombre_completo": "Nuevo Miembro",
        "cargo": "Secretario",
        "url_foto": "http://foto.jpg",
        "orden_jerarquia": 2
    }
    response = client.post("/api/junta", json=payload)
    assert response.status_code == 201
    assert response.json["status"] == "success"
    assert "creado correctamente" in response.json["message"]

def test_crear_miembro_junta_datos_invalidos(client):
    payload = {
        "nombre_completo": "", # vacío
        "cargo": "Secretario",
        "orden_jerarquia": 0 # menor a 1
    }
    response = client.post("/api/junta", json=payload)
    assert response.status_code == 400
    assert response.json["status"] == "error"

def test_crear_miembro_junta_jerarquia_invalida(client):
    payload = {
        "nombre_completo": "Miembro",
        "cargo": "Vocal",
        "orden_jerarquia": "no-es-entero"
    }
    response = client.post("/api/junta", json=payload)
    assert response.status_code == 400
    assert "número entero válido" in response.json["message"]

def test_actualizar_miembro_junta_exitoso(client, mock_db):
    # Mockear existencia
    mock_db['cursor'].fetchone.return_value = [1] # existe 1
    
    payload = {
        "nombre_completo": "Miembro Actualizado",
        "cargo": "Tesorero",
        "url_fotografia": "http://nueva-foto.jpg",
        "orden_jerarquia": 1
    }
    
    response = client.put("/api/junta/1", json=payload)
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert "actualizado correctamente" in response.json["message"]

def test_actualizar_miembro_junta_no_encontrado(client, mock_db):
    # Mockear inexistencia
    mock_db['cursor'].fetchone.return_value = [0] # existe 0
    
    payload = {
        "nombre_completo": "Miembro Actualizado",
        "cargo": "Tesorero",
        "orden_jerarquia": 1
    }
    
    response = client.put("/api/junta/999", json=payload)
    assert response.status_code == 404
    assert "no existe" in response.json["message"]

def test_eliminar_miembro_junta_exitoso(client, mock_db):
    # Mockear existencia
    mock_db['cursor'].fetchone.return_value = [1]
    
    response = client.delete("/api/junta/1")
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert "eliminado correctamente" in response.json["message"]

def test_eliminar_miembro_junta_no_encontrado(client, mock_db):
    # Mockear inexistencia
    mock_db['cursor'].fetchone.return_value = [0]
    
    response = client.delete("/api/junta/999")
    assert response.status_code == 404
    assert "no existe" in response.json["message"]
