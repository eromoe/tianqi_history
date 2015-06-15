#-*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TEXT, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
import settings

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
    name = Column(String)                      # 地区名称
    zone_id = Column(Integer)                  # Location oid
    weather = Column(String)                   # 天气
    wind_direction = Column(String)            # 风向
    wind_power = Column(String)                # 风强
    max_t = Column(Integer)                    # 最高温度
    min_t = Column(Integer)                    # 最低温度
    date = Column(Date)                        # 日期



class SQLite(object):
    DBNAME = getattr(settings, 'DBNAME', 'weather')

    def __init__(self):
        try:
            engine = getattr(self, 'engine', None)
            if engine is None:
                self.engine = create_engine('sqlite:///%s.db' % self.DBNAME)
                self.Session = sessionmaker(bind=self.engine)
        except Exception as e:
            print "ERROR(SQLite): %s"%(str(e),)



if __name__ == "__main__":
    # 创建 之前所有 定义的 类 对应的 table
    # db = MysqlPipeline()
    # Base.metadata.create_all(bind=db.engine)
    sqlite = SQLite()
    Base.metadata.create_all(bind=sqlite.engine)
