import os 
from decouple import config
from dotenv import load_dotenv
from datetime import timedelta
load_dotenv()

# BASE_DIR = os.path.dirname(os.path.realpath(__file__))

import os
import re


DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}


uri = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}" # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

class Config:
    SECRET_KEY =config('SECRET_KEY','secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_SECRET_KEY =config('JWT_SECRET_KEY')

    
class DevConfig(Config):
    DEBUG = config('DEBUG',cast=bool)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"

    
class TestConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI="sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True
class ProdConfig(Config):
     SQLALCHEMY_ECHO = True
     SQLALCHEMY_DATABASE_URI = uri
     SQLALCHEMY_TRACK_MODIFICATIONS=False
     DEBUG = config('DEBUG',cast=bool)


config_dict ={
    'dev':DevConfig,
    'testing':TestConfig,
    'production':ProdConfig
}