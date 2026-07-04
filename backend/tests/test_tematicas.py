def test_listar_tematicas(client, mock_db):
    tematicas_mock = [
        {"id_tematica": 1, "nombre": "Salud", "descripcion": "Jornadas médicas", "estado": "ACTIVO"}
    ]
    mock_db['cursor'].fetchall.return_value = tematicas_mock
    
    response = client.get("/api/tematicas")
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert len(response.json["data"]) == 1
    assert response.json["data"][0]["nombre"] == "Salud"

def test_crear_tematica_exitosa(client, mock_db):
    mock_db['cursor'].fetchone.return_value = [0] # no existe duplicado
    
    payload = {"nombre": "Educación", "descripcion": "Tutorías"}
    response = client.post("/api/tematicas", json=payload)
    assert response.status_code == 201
    assert response.json["status"] == "success"
    assert "creada correctamente" in response.json["message"]

def test_crear_tematica_nombre_vacio(client):
    payload = {"nombre": "  ", "descripcion": "Tutorías"}
    response = client.post("/api/tematicas", json=payload)
    assert response.status_code == 400
    assert "obligatorio" in response.json["message"]

def test_crear_tematica_duplicada(client, mock_db):
    mock_db['cursor'].fetchone.return_value = [1] # ya existe
    
    payload = {"nombre": "Salud", "descripcion": "Jornadas médicas"}
    response = client.post("/api/tematicas", json=payload)
    assert response.status_code == 400
    assert "Ya existe" in response.json["message"]

def test_actualizar_tematica_exitosa(client, mock_db):
    mock_db['cursor'].fetchone.return_value = [1] # existe la temática
    
    payload = {"nombre": "Salud Dental", "descripcion": "Campañas de cepillado", "estado": "ACTIVO"}
    response = client.put("/api/tematicas/1", json=payload)
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert "actualizada correctamente" in response.json["message"]

def test_actualizar_tematica_no_encontrada(client, mock_db):
    mock_db['cursor'].fetchone.return_value = [0] # no existe
    
    payload = {"nombre": "Salud Dental"}
    response = client.put("/api/tematicas/999", json=payload)
    assert response.status_code == 404
    assert "no existe" in response.json["message"]

def test_actualizar_tematica_estado_invalido(client):
    payload = {"estado": "INACTIVO_INVAL"}
    response = client.put("/api/tematicas/1", json=payload)
    assert response.status_code == 400
    assert "Estado inválido" in response.json["message"]

def test_eliminar_tematica_exitosa(client, mock_db):
    mock_db['cursor'].fetchone.return_value = [1] # existe
    
    response = client.delete("/api/tematicas/1")
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert "eliminada correctamente" in response.json["message"]

def test_eliminar_tematica_no_encontrada(client, mock_db):
    mock_db['cursor'].fetchone.return_value = [0] # no existe
    
    response = client.delete("/api/tematicas/999")
    assert response.status_code == 404
    assert "no existe" in response.json["message"]
