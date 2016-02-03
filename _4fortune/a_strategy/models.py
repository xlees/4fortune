# from django.db import models
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
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
