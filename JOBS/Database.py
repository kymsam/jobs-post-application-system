from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.declarative  import declarative_base
from sqlalchemy.engine import create_engine
from .config import settings



DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(DATABASE_URL)
sessionlocal = sessionmaker(autoflush=False,bind=engine,autocommit=False)
Base = declarative_base()


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

