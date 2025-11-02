import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # Correct MySQL credentials for PythonAnywhere
    MYSQL_HOST = "luyaka.mysql.pythonanywhere-services.com"
    MYSQL_PORT = 3306
    MYSQL_USER = "luyaka"
    MYSQL_PASSWORD = "phanacey"
    MYSQL_DB = "luyaka$it_service_db"

    #  SQLAlchemy connection URI
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Admin login credentials
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin123"
