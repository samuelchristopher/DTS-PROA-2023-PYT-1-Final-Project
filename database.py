from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

config = dotenv_values(".env")
# Create MySQL engine instance
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://" + \
    config['username'] + ":" + config['password'] + "@" + \
    config['host'] + ":" + config['port'] + "/" + config['database'] + ""

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
# Create declaritive base meta instance
Base = declarative_base()
# Create session local class for session maker
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
