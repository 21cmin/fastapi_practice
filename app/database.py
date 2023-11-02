from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg://postgres:1234@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL) #autocommit=Fasel autoflush=False

Session = sessionmaker(engine)

def get_db():
  session = Session()
  try:
    yield session
  finally:
    session.close()
    
class Base(DeclarativeBase):
  pass
