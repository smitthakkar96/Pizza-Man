from sqlalchemy import *
from sqlalchemy.orm import mapper
from util import *
from datetime import datetime

user = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(1024), nullable=False),
    Column('location',String(1024)),
    Column('latitude',Float),
    Column('longitude',Float),
    Column('contact_number',String(1024))
)

pizza = Table('pizza',metadata,
    Column('id',Integer,primary_key=True,autoincrement=True),
    Column('name', String(1024), nullable=False),
    Column('image_url', String(1024)),
    Column('description',String(1024))
)

orders = Table('orders',metadata,
    Column('oid',Integer,primary_key=True,autoincrement=True),
    Column('user',ForeignKey("users.id")),
    Column('pizza',ForeignKey('pizza.id')),
    Column('datetime',DATETIME(timezone=False))
)

class User(object):
    def __init__(self, id, name, location, latitude, longitude,contact_number):
        self.id = id
        self.name = name
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.contact_number = contact_number

    def __repr__(self):
        return "%s(%r,%r,%r,%r)" % (self.__class__.name,str(self.id),self.name,self.location,str(self.latitude),str(self.longitude),str(contact_number))

class Pizza(object):
    def __init__(self, id, name, image_url, description):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.description = description

    def __repr__(self):
        return "%s(%r,%r,%r,%r)" % (self.__class__.name,self.id,self.name,self.image_url,self.description)

class Orders(object):
    def __init__(self, id, user, pizza, _datetime):
        self.id = None
        self.user = user
        self.pizza = pizza
        self.datetime = datetime.now()
    def __repr__(self):
        return "%s(%r,%r,%r,%r)" % (self.__class__.name,self.id,self.user,self.pizza,self.datetime)


mapper(User, user)
mapper(Pizza,pizza)
mapper(Orders,orders)

# metadata.create_all(db)
# sm = orm.sessionmaker(bind=db, autoflush=True, autocommit=True, expire_on_commit=True)
# session = orm.scoped_session(sm)
# new_prod = Product("1","Product1")
# session.add(new_prod)
# session.flush()
