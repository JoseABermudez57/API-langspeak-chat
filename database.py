import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB.HOST_MYSQL")
port = os.getenv("DB.PORT_MYSQL")
user = os.getenv("DB.USER_MYSQL")
password = os.getenv("DB.PASSWORD_MYSQL")
database = os.getenv("DB.DATABASE_MYSQL")

# DataBase configuration
# DATABASE_URL = f"mysql://admin:Corazon666@database-1.cxo9hmgwb5h3.us-east-1.rds.amazonaws.com:3306/chats_db_langspeak"
DATABASE_URL = f"mysql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
