import os
import ssl
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener la URL de conexión desde .env
database_url = os.getenv("SQLALCHEMY_DATABASE_URL")

if not database_url:
    raise ValueError("⚠️ No se encontró la variable SQLALCHEMY_DATABASE_URL en el .env")

# Obtener la ruta absoluta del certificado SSL
current_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio de db.py
ssl_cert_path = os.path.abspath(os.path.join(current_dir, "../../certs/aiven_cert.pem"))

# Verificar si el archivo de certificado existe
if not os.path.exists(ssl_cert_path):
    raise FileNotFoundError(f"⚠️ El archivo de certificado SSL no se encuentra en: {ssl_cert_path}")

print(f"🔍 Conectando a la base de datos con SSL: {ssl_cert_path}")

# Configuración de conexión con SSL utilizando ssl.SSLContext
ssl_context = ssl.create_default_context(cafile=ssl_cert_path)

# Crear motor de SQLAlchemy con SSL habilitado
engine = create_engine(database_url, connect_args={"ssl": ssl_context})

# Crear la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()
