from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DataBase configuration
DATABASE_URL = "mysql+pymysql://admin:Corazon666@database-1.cxo9hmgwb5h3.us-east-1.rds.amazonaws.com:3306/chats_db_langspeak"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
