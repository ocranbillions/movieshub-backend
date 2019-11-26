from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
Movie
Have title and release year
'''
class Movie(db.Model):  
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_year = Column(String)

    def __init__(self, title, release_year):
        self.title = title
        self.release_year = release_year


    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            print(sys.exc_info())
            # raise
        finally:
            db.session.close()


    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            print(sys.exc_info())
            # raise
        finally:
            db.session.close()


    def update(self):
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            print(sys.exc_info())
            # raise
        finally:
            db.session.close()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year}
  


'''
Actor
Have name, age, and gender
'''
class Actor(db.Model):  
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
  
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
    
    def update(self):
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender}