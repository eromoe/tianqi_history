#-*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TEXT, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Province(Base):
    __tablename__ = 'province'
    id = Column(Integer, primary_key=True)
    oid = Column(Integer, unique=True)  #原始id
    name = Column(String)               #中文名
    py = Column(String)                 #拼音



class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    oid = Column(Integer, unique=True)
    province_id = Column(ForeignKey('province.id'), nullable=False, index=True)
    name = Column(String)
    py = Column(String)


    province = relationship(Province)

class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    oid = Column(Integer, unique=True)
    city_id = Column(ForeignKey('city.id'), nullable=False, index=True)
    name = Column(String)
    py = Column(String)


    city = relationship(City)


class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    zone_id = Column(Integer)                  # Location oid
    weather = Column(String)                   # 天气
    wind_direction = Column(String)            # 风向
    wind_power = Column(String)                # 风强
    max_t = Column(Integer)                    # 最高温度
    min_t = Column(Integer)                    # 最低温度
    date = Column(Date)                        # 日期





