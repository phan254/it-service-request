import os

class Config:
    # Flask secret key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')

    #  Update these values with your actual MySQL credentials
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://luyaka:phanacey@luyaka.mysql.pythonanywhere-services.com/luyaka$itservicedb'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Admin login
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin123'

    # Optional: external source for departments
    DEPARTMENTS_URL = ''

