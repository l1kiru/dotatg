from dbconfig import host, user, password, db_name, port
from dbconfig import DBsettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

settings = DBsettings(host,user,password,db_name,port)

engine = create_engine(
    url=settings.DatabaseUrl(),
    echo=False,
    pool_size=5,
    max_overflow=10,
)

session_factory = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)