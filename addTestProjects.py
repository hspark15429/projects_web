from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from setupDB import Base, Project, Category, Entry
 
engine = create_engine('sqlite:///projects.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()




project1 = Project(name = "TEST PROJECT")
session.add(project1)
session.commit()

category1 = Category(name = "TEST CATEGORY", project_id = 1)
session.add(category1)
session.commit()

entry1 = Entry(description = "THIS IS A TEST DESCRIPTION.", category_id = 1, project_id = 1)
session.add(entry1)
session.commit()