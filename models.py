from sqlalchemy import create_engine as ca
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

engine = ca("postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Location(Base):
    __tablename__ = 'location'

    key = Column(String, primary_key = True)
    place_name = Column(String, nullable=False)
    admin_name1 = Column(String, nullable=False)
    latitude = Column(Float, unique = True)
    longtitude = Column(Float, unique = True)
    accuracy = Column(Integer, nullable = True)


    def __init__(self, key, place_name, admin_name, lat, lon, acc):
        self.key = key
        self.place_name = place_name
        self.admin_name1 = admin_name
        self.longtitude = lat
        self.latitude = lon
        self.accuracy = acc

Base.metadata.create_all(engine)
#session = sessionmaker()
