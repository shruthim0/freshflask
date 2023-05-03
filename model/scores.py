""" database dependencies to support sqliteDB examples """
from random import randrange
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError


# Define the Score class to manage actions in the 'score' table
class Score(db.Model):
    __tablename__ = 'scores1' 

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=True, nullable=False)
    _score = db.Column(db.String(255), unique=False, nullable=False)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, score):
        self._name = name    # variables with self prefix become part of the object, 
        self._score = score

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, score):
        self._score = score
        
    def is_score(self, score):
        return self._score == score
    
    @property
    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            # creates a person object from Score(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "score": self.score
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", score=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(score) > 0:
            self.score = score
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

"""Database Creation and Testing """

def initScores():
    with app.app_context():
        """Create database and tables"""
        # db.init_app(app)
        db.create_all()
        """Tester data for table"""
        u1 = Score(name='Shruthi', score='2')
        u2 = Score(name='Lina', score='3')
        u3 = Score(name='Lydia', score='1')
        u4 = Score(name='Sarah', score='5')
        u5 = Score(name='Jake', score='6')

        users = [u1, u2, u3, u4, u5]

        """Builds sample user/note(s) data"""
        for user in users:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 4)):
                    note = "#### " + user.name + " note " + str(num) + ". \n Generated by test data."
                '''add user/post data to table'''
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.score}")