import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-desarrollo')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'sqlite:///tienda.db'
    ).replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join('app', 'static', 'Assets')