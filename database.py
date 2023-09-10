from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL_DATABASE = 'postgresql://fastapi_9kej_user:y8NTBeTo0FKqa2v0cAFAxkRlfgzQRhd4@dpg-cjslmum8b8as73d5lfhg-a:5432/fastapi_9kej'
URL_DATABASE = 'postgresql://postgres:postgres123@localhost:5432/postgres'


engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)
Base = declarative_base()