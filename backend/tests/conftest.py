import sys
import os
from unittest.mock import MagicMock, patch
import pytest

# Asegurar que el backend esté en el PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(autouse=True)
def mock_db():
    from app.db import db_instance
    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    # Configurar respuestas por defecto para la siembra de base de datos en create_app
    mock_cursor.fetchone.return_value = [0] 
    
    # Mockear los métodos en la instancia real importada (singleton)
    with patch.object(db_instance, 'get_connection', return_value=mock_conn) as mock_get_conn, \
         patch.object(db_instance, 'execute_procedure', return_value=[]) as mock_exec_proc:
        
        yield {
            'db_instance': db_instance,
            'conn': mock_conn,
            'cursor': mock_cursor,
            'execute_procedure': mock_exec_proc
        }

@pytest.fixture
def app():
    from app import create_app
    flask_app = create_app()
    flask_app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test_secret",
        "JWT_SECRET_KEY": "test_jwt_secret",
        "JWT_EXPIRATION_H": 1
    })
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()
