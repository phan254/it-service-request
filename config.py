import os
from dotenv import load_dotenv

# Load variables from .env if it exists
load_dotenv()

class Config:
    # Flask secret key
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

    # MySQL connection for PythonAnywhere
    MYSQL_HOST = os.getenv("MYSQL_HOST", "luyaka.mysql.pythonanywhere-services.com")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER = os.getenv("MYSQL_USER", "luyaka")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "phanacey")
    MYSQL_DB = os.getenv("MYSQL_DB", "luyaka$it_service_db")

    # SQLAlchemy connection string
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optional: external source for departments
    DEPARTMENTS_URL = os.getenv("DEPARTMENTS_URL", "")

    # Admin credentials
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
