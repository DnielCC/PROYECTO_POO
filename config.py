import os

class Config:
    SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345@localhost:3306/bolsa_trabajo'
    # Alternativa: SQLite para desarrollo rápido (sin MySQL)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///bolsa_trabajo.db'

class ProductionConfig(Config):
    DEBUG = False
    # Configuración para producción (cambiar credenciales)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://usuario:contraseña@servidor/bolsa_trabajo'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 