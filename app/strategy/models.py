#coding: utf-8
#
# from django.db import models
from sqlalchemy import *
# from sqlalchemy import Table, Column, Integer, String, Date,MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Language(Base):
    __tablename__ = 'languages'

    # columns
    id = Column(Integer, primary_key=True)
    name = Column(String)
    extension = Column(String)

    def __init__(self, name, extension):
        self.name = name
        self.extension = extension

    def __repr__(self):
        return u"Language(%s, %s)" % (self.name, self.extension)

class StockInfo(Base):
    __tablename__ = 'stock_info'

    # columns
    code = Column(String, primary_key=True)
    name = Column(String)
    # 所属行业
    industry = Column(String)
    # 地区
    area = Column(String)
    # 上市日期
    timeToMarket = Column(Date)

    # 总股本（万）
    totalStock = Column(Float)
    # 流通股本（万）
    outstanding = Column(Float)
    # 总资产（万）
    totalAsset = Column(Float)
    # 流动资产（万）
    liquidAssets = Column(Float)
    # 固定资产（万）
    fixedAssets = Column(Float)
    # 公积金(万)
    reserved = Column(Float)

    # # 每股收益
    # eps = Column(Float)
    # # 每股净资产
    # bvps = Column(Float)
    #  # 每股公积金
    # reservedPerShare = Column(Float)

    # # 市盈率
    # pe = Column(Float)
    # # 市净率
    # pa = Column(Float)
    

    def __init__(self, code, name):
        self.name = name
        self.code = code

    def __repr__(self):
        return u"Stock(%s, %s, %s)" % (self.code, self.name, self.industry)
   


