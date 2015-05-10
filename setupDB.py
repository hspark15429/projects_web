import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Project(Base):
    __tablename__ = 'projects'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    project_id = Column(Integer,ForeignKey('projects.id'), nullable = False)
    project = relationship(Project)
 
class Entry(Base):
    __tablename__ = 'entries'

    description = Column(String(250), nullable = False)
    category_id = Column(Integer,ForeignKey('categories.id'), primary_key = True)
    project_id = Column(Integer,ForeignKey('projects.id'), primary_key = True)
    project = relationship(Project)
    category = relationship(Category)



    # @property
    # def serialize(self):
    #     return {
    #         "name" : self.name,
    #         'description' : self.description,
    #         'id' : self.id,
    #         'course' : self.course,
    #         'price': self.price,
    #     }


engine = create_engine('sqlite:///projects.db')
 

Base.metadata.create_all(engine)
