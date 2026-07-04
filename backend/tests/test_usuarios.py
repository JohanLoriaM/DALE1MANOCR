def test_listar_usuarios(client, mock_db):
    usuarios_mock = [
        {
            "id_usuario": 1,
            "nombre_completo": "Juan Perez",
            "correo": "juan@example.com",
            "rol": "USER",
            "es_miembro_oficial": 0,
            "fecha_registro": None,
            "estado": "ACTIVO"
        }
    ]
    mock_db['cursor'].fetchall.return_value = usuarios_mock
    
    response = client.get("/api/usuarios")
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert len(response.json["data"]) == 1
    assert response.json["data"][0]["nombre_completo"] == "Juan Perez"

def test_promover_usuario_exitoso(client, mock_db):
    mock_db['cursor'].fetchone.return_value = [1] # existe el usuario
    
    response = client.post("/api/usuarios/1/promover")
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert "promovido a miembro oficial" in response.json["message"]

def test_promover_usuario_no_encontrado(client, mock_db):
    mock_db['cursor'].fetchone.return_value = [0] # no existe el usuario
    
    response = client.post("/api/usuarios/999/promover")
    assert response.status_code == 404
    assert "no existe" in response.json["message"]

def test_cambiar_estado_exitoso(client, mock_db):
    mock_db['cursor'].fetchone.return_value = [1]
    
    payload = {"estado": "INACTIVO"}
    response = client.post("/api/usuarios/1/status", json=payload)
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert "actualizado correctamente" in response.json["message"]

def test_cambiar_estado_invalido(client):
    payload = {"estado": "OTRO_ESTADO"}
    response = client.post("/api/usuarios/1/status", json=payload)
    assert response.status_code == 400
    assert "Estado inválido" in response.json["message"]

def test_cambiar_estado_no_encontrado(client, mock_db):
    mock_db['cursor'].fetchone.return_value = [0]
    
    payload = {"estado": "INACTIVO"}
    response = client.post("/api/usuarios/999/status", json=payload)
    assert response.status_code == 404
    assert "no existe" in response.json["message"]

def test_cambiar_rol_exitoso(client, mock_db):
    mock_db['cursor'].fetchone.return_value = [1]
    
    payload = {"rol": "ADMIN"}
    response = client.post("/api/usuarios/1/rol", json=payload)
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert "Rol de usuario actualizado correctamente" in response.json["message"]

def test_cambiar_rol_invalido(client):
    payload = {"rol": "SUPERADMIN"}
    response = client.post("/api/usuarios/1/rol", json=payload)
    assert response.status_code == 400
    assert "Rol inválido" in response.json["message"]

def test_cambiar_rol_no_encontrado(client, mock_db):
    mock_db['cursor'].fetchone.return_value = [0]
    
    payload = {"rol": "ADMIN"}
    response = client.post("/api/usuarios/999/rol", json=payload)
    assert response.status_code == 404
    assert "no existe" in response.json["message"]

def test_listar_asistencias(client, mock_db):
    asistencias_mock = [
        {
            "id_asistencia": 1,
            "id_usuario": 1,
            "id_proyecto": 2,
            "fecha_inscripcion": None,
            "asistio": 0
        }
    ]
    mock_db['cursor'].fetchall.return_value = asistencias_mock
    
    response = client.get("/api/asistencias")
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert len(response.json["data"]) == 1

def test_top_voluntarios(client, mock_db):
    top_mock = [
        {
            "id_usuario": 1,
            "nombre_completo": "Juan Perez",
            "correo": "juan@example.com",
            "es_miembro_oficial": 1,
            "total_asistencias": 5
        }
    ]
    mock_db['cursor'].fetchall.return_value = top_mock
    
    response = client.get("/api/top-voluntarios")
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert len(response.json["data"]) == 1
    assert response.json["data"][0]["total_asistencias"] == 5
