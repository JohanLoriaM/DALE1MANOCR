import mysql.connector

def test_obtener_proyectos(client, mock_db):
    proyectos_mock = [
        {
            "id_proyecto": 1,
            "titulo": "Proyecto Bosque",
            "descripcion": "Sembrar arboles",
            "fecha_inicio": None,
            "fecha_fin": None,
            "tematica": "Medio Ambiente"
        }
    ]
    mock_db['db_instance'].execute_procedure.return_value = proyectos_mock
    
    response = client.get("/api/proyectos")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["titulo"] == "Proyecto Bosque"

def test_crear_proyecto_exitoso(client, mock_db):
    payload = {
        "id_tematica": 1,
        "titulo": "Nuevo Proyecto",
        "descripcion": "Descripción del proyecto",
        "fecha_inicio": "2026-07-04T10:00:00.000Z",
        "fecha_fin": "2026-07-04T12:00:00.000Z"
    }
    
    response = client.post("/api/proyectos", json=payload)
    assert response.status_code == 201
    assert response.json["status"] == "success"
    assert "creado exitosamente" in response.json["message"]

def test_crear_proyecto_tematica_invalida(client):
    payload = {
        "id_tematica": "invalido",
        "titulo": "Nuevo Proyecto",
        "descripcion": "Descripción",
        "fecha_inicio": "2026-07-04T10:00:00",
        "fecha_fin": "2026-07-04T12:00:00"
    }
    response = client.post("/api/proyectos", json=payload)
    assert response.status_code == 400
    assert "temática debe ser un número entero" in response.json["error"]

def test_crear_proyecto_faltan_campos(client):
    payload = {
        "titulo": "Proyecto incompleto"
    }
    response = client.post("/api/proyectos", json=payload)
    assert response.status_code == 400
    assert "obligatorios" in response.json["error"]

def test_actualizar_proyecto_exitoso(client, mock_db):
    # Mockear obtener_proyectos para que retorne el proyecto existente
    proyectos_mock = [{"id_proyecto": 1, "titulo": "Proyecto Viejo"}]
    mock_db['db_instance'].execute_procedure.return_value = proyectos_mock
    
    payload = {
        "id_tematica": 1,
        "titulo": "Proyecto Actualizado",
        "descripcion": "Nueva descripcion",
        "fecha_inicio": "2026-07-04T10:00:00",
        "fecha_fin": "2026-07-04T12:00:00"
    }
    
    response = client.put("/api/proyectos/1", json=payload)
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert "actualizado exitosamente" in response.json["message"]

def test_actualizar_proyecto_no_encontrado(client, mock_db):
    # Mockear obtener_proyectos para que no retorne el proyecto
    mock_db['db_instance'].execute_procedure.return_value = []
    
    payload = {
        "id_tematica": 1,
        "titulo": "Proyecto Actualizado",
        "descripcion": "Nueva descripcion",
        "fecha_inicio": "2026-07-04T10:00:00",
        "fecha_fin": "2026-07-04T12:00:00"
    }
    
    response = client.put("/api/proyectos/999", json=payload)
    assert response.status_code == 404
    assert "no existe" in response.json["error"]

def test_actualizar_estado_exitoso(client, mock_db):
    # Mockear que el proyecto existe
    proyectos_mock = [{"id_proyecto": 1, "titulo": "Proyecto"}]
    mock_db['db_instance'].execute_procedure.return_value = proyectos_mock
    
    payload = {"estado": "PASADO"}
    response = client.patch("/api/proyectos/1/status", json=payload)
    assert response.status_code == 200
    assert response.json["status"] == "success"

def test_actualizar_estado_invalido(client, mock_db):
    proyectos_mock = [{"id_proyecto": 1, "titulo": "Proyecto"}]
    mock_db['db_instance'].execute_procedure.return_value = proyectos_mock
    
    payload = {"estado": "ESTADO_INEXISTENTE"}
    response = client.patch("/api/proyectos/1/status", json=payload)
    assert response.status_code == 400
    assert "no permitido" in response.json["error"]

def test_actualizar_estado_no_encontrado(client, mock_db):
    mock_db['db_instance'].execute_procedure.return_value = []
    
    payload = {"estado": "PASADO"}
    response = client.patch("/api/proyectos/999/status", json=payload)
    assert response.status_code == 404
    assert "no existe" in response.json["error"]

def test_inscribir_usuario_exitoso(client, mock_db):
    payload = {"id_usuario": 1, "id_proyecto": 2}
    response = client.post("/api/proyectos/inscribir", json=payload)
    assert response.status_code == 200
    assert response.json["status"] == "success"

def test_inscribir_usuario_no_existente(client, mock_db):
    # Simular error de BD por fk inexistente (1452)
    err = mysql.connector.Error()
    err.errno = 1452
    mock_db['db_instance'].execute_procedure.side_effect = err
    
    payload = {"id_usuario": 999, "id_proyecto": 999}
    response = client.post("/api/proyectos/inscribir", json=payload)
    assert response.status_code == 400
    assert "no existe" in response.json["error"]

def test_marcar_asistencia_exitosa(client, mock_db):
    # Mockear que la inscripción existe en Asistencias
    mock_db['cursor'].fetchone.return_value = [1]
    
    payload = {"id_usuario": 1, "id_proyecto": 2, "asistio": True}
    response = client.post("/api/proyectos/asistencia", json=payload)
    assert response.status_code == 200
    assert response.json["status"] == "success"

def test_marcar_asistencia_voluntario_no_inscrito(client, mock_db):
    # Mockear que no existe inscripción en Asistencias
    mock_db['cursor'].fetchone.return_value = [0]
    
    payload = {"id_usuario": 1, "id_proyecto": 2, "asistio": True}
    response = client.post("/api/proyectos/asistencia", json=payload)
    assert response.status_code == 404
    assert "no está inscrito" in response.json["error"]

def test_marcar_asistencia_asistio_invalido(client):
    payload = {"id_usuario": 1, "id_proyecto": 2, "asistio": "no-booleano"}
    response = client.post("/api/proyectos/asistencia", json=payload)
    assert response.status_code == 400
    assert "debe ser booleano" in response.json["error"]
