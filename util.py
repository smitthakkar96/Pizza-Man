from sqlalchemy import *
from sqlalchemy import create_engine, orm

metadata = MetaData()
db = create_engine('mysql://root@localhost/bot')

sm = orm.sessionmaker(bind=db, autoflush=True, autocommit=True, expire_on_commit=True)
session = orm.scoped_session(sm)
