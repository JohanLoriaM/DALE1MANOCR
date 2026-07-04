from unittest.mock import patch, MagicMock
import bcrypt
import jwt

def test_registro_exitoso(client, mock_db):
    # Mockear call_sp para registro (SP_RegistroUsuario)
    mock_db['db_instance'].execute_procedure.return_value = []
    
    payload = {
        "nombre": "Juan Perez",
        "email": "juan@example.com",
        "password": "securepassword123"
    }
    
    response = client.post("/api/auth/registro", json=payload)
    assert response.status_code == 201
    assert response.json["message"] == "Usuario registrado exitosamente."

def test_registro_campos_faltantes(client):
    payload = {
        "nombre": "Juan Perez"
        # falta correo y password
    }
    
    response = client.post("/api/auth/registro", json=payload)
    assert response.status_code == 400
    assert "obligatorios" in response.json["error"]

def test_registro_correo_invalido(client):
    payload = {
        "nombre": "Juan Perez",
        "email": "correo-invalido",
        "password": "password123"
    }
    
    response = client.post("/api/auth/registro", json=payload)
    assert response.status_code == 400
    assert "no es válido" in response.json["error"]

def test_registro_contrasena_corta(client):
    payload = {
        "nombre": "Juan Perez",
        "email": "juan@example.com",
        "password": "123"
    }
    
    response = client.post("/api/auth/registro", json=payload)
    assert response.status_code == 400
    assert "al menos 6 caracteres" in response.json["error"]

def test_login_exitoso(client, mock_db):
    # Generar hash de contraseña simulado
    contrasena = "mypassword"
    contrasena_hash = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    # Mockear el usuario devuelto por SP_ObtenerUsuarioLogin
    usuario_mock = {
        "id_usuario": 1,
        "nombre_completo": "Juan Perez",
        "contrasena_hash": contrasena_hash,
        "rol": "USER",
        "estado": "ACTIVO"
    }
    
    mock_db['db_instance'].execute_procedure.return_value = [usuario_mock]
    
    payload = {
        "email": "juan@example.com",
        "password": contrasena
    }
    
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 200
    assert "token" in response.json
    assert response.json["nombre"] == "Juan Perez"
    assert response.json["usuario"]["rol"] == "USER"

def test_login_credenciales_invalidas(client, mock_db):
    # Mockear que no se encuentra el usuario
    mock_db['db_instance'].execute_procedure.return_value = []
    
    payload = {
        "email": "noexiste@example.com",
        "password": "password"
    }
    
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 401
    assert "Credenciales inválidas" in response.json["error"]
