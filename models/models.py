from sqlalchemy import Column, Float, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Steps(Base):
    __tablename__ = "steps"

    datauuid = Column(String, primary_key=True)
    binning_data = Column(String)
    update_time = Column(String)
    create_time = Column(String)
    source_pkg_name = Column(String)
    source_type = Column(Integer)
    count = Column(Integer)
    speed = Column(Float)
    distance = Column(Float)
    calorie = Column(Float)
    deviceuuid = Column(String)
    pkg_name = Column(String)
    day_time = Column(Integer)


class Weather(Base):
    __tablename__ = "weather"

    time = Column(String)
    location = Column(String)
    tavg = Column(Float)
    tmin = Column(Float)
    tmax = Column(Float)
    prcp = Column(Float)
    snow = Column(Float)
    wdir = Column(Float)
    wspd = Column(Float)
    wpgt = Column(Float)
    pres = Column(Float)
    tsun = Column(Float)

    __table_args__ = (PrimaryKeyConstraint("time", "location"),)
