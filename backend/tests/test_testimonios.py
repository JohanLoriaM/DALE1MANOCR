import mysql.connector

def test_get_testimonios(client, mock_db):
    testimonios_mock = [
        {
            "id_testimonio": 1,
            "id_usuario": 2,
            "id_proyecto": 3,
            "nombre_completo": "Juan Perez",
            "proyecto": "Proyecto Reforestacion",
            "contenido": "Excelente actividad!",
            "url_video": None,
            "fecha_publicacion": None,
            "aprobado": True
        }
    ]
    mock_db['cursor'].fetchall.return_value = testimonios_mock
    
    response = client.get("/api/testimonios")
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert len(response.json["data"]) == 1
    assert response.json["data"][0]["contenido"] == "Excelente actividad!"

def test_crear_testimonio_exitoso(client, mock_db):
    payload = {
        "id_usuario": 1,
        "id_proyecto": 1,
        "contenido": "Me encantó participar.",
        "url_video": ""
    }
    
    response = client.post("/api/testimonios", json=payload)
    assert response.status_code == 201
    assert response.json["status"] == "success"
    assert "registrado para revisión" in response.json["message"]

def test_crear_testimonio_ids_invalidos(client):
    payload = {
        "id_usuario": "invalido",
        "id_proyecto": 1,
        "contenido": "Me encantó participar."
    }
    
    response = client.post("/api/testimonios", json=payload)
    assert response.status_code == 400
    assert "enteros válidos" in response.json["message"]

def test_crear_testimonio_sin_contenido(client):
    payload = {
        "id_usuario": 1,
        "id_proyecto": 1,
        "contenido": ""
    }
    
    response = client.post("/api/testimonios", json=payload)
    assert response.status_code == 400
    assert "obligatorios" in response.json["message"]

def test_crear_testimonio_recursos_no_existen(client, mock_db):
    # Mockear error de llave foránea de mysql
    err = mysql.connector.Error()
    err.errno = 1452
    mock_db['cursor'].execute.side_effect = err
    
    payload = {
        "id_usuario": 999,
        "id_proyecto": 999,
        "contenido": "Buen proyecto!"
    }
    
    response = client.post("/api/testimonios", json=payload)
    assert response.status_code == 400
    assert "no existe" in response.json["message"]

def test_aprobar_testimonio_exitoso(client, mock_db):
    mock_db['cursor'].fetchone.return_value = [1]
    
    response = client.post("/api/testimonios/1/aprobar")
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert "aprobado correctamente" in response.json["message"]

def test_aprobar_testimonio_no_encontrado(client, mock_db):
    mock_db['cursor'].fetchone.return_value = [0]
    
    response = client.post("/api/testimonios/999/aprobar")
    assert response.status_code == 404
    assert "no existe" in response.json["message"]

def test_eliminar_testimonio_exitoso(client, mock_db):
    mock_db['cursor'].fetchone.return_value = [1]
    
    response = client.delete("/api/testimonios/1")
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert "rechazado/eliminado correctamente" in response.json["message"]

def test_eliminar_testimonio_no_encontrado(client, mock_db):
    mock_db['cursor'].fetchone.return_value = [0]
    
    response = client.delete("/api/testimonios/999")
    assert response.status_code == 404
    assert "no existe" in response.json["message"]
