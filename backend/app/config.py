import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env si existe localmente
load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dale1mano_secret_key_prod_2026')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secret_key_dale1mano_2026')
    JWT_EXPIRATION_H = int(os.getenv('JWT_EXPIRATION_H', 24))

    # Configuración de MySQL adaptada para las variables del docker-compose y .env local
    MYSQL_HOST = os.getenv('MYSQL_HOST') or os.getenv('DB_HOST') or 'd1mcr_mysql_db'
    MYSQL_USER = os.getenv('MYSQL_USER') or os.getenv('DB_USER') or 'root'
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD') or os.getenv('DB_PASSWORD') or ''
    MYSQL_DB = os.getenv('MYSQL_DB') or os.getenv('DB_NAME') or 'd1mcr_db'
    MYSQL_PORT = int(os.getenv('MYSQL_PORT') or os.getenv('DB_PORT') or 3306)
