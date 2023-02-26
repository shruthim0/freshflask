""" database dependencies to support sqliteDB examples """
from random import randrange
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''


# Define the Recipe class to manage actions in the 'recipes' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) Recipe represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Nutrition(db.Model):
    __tablename__ = ' nutritions'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, unique=True, primary_key=True)
    _nutritionname = db.Column(db.String(255), unique=False, nullable=False)
    _nutritioncalories = db.Column(db.String(255), unique=False, nullable=False)
    _nutritionfat = db.Column(db.String(255), unique=False, nullable=False)
    _nutritioncarbs = db.Column(db.String(255), unique=False, nullable=False)

    # Defines a relationship between Recipe record and Notes table, one-to-many (one recipe to many notes)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, nutritionname, nutritioncalories,nutritionfat, nutritioncarbs):
        self._nutritionname = nutritionname    # variables with self prefix become part of the object, 
        self._nutritioncalories = nutritioncalories
        self._nutritionfat = nutritionfat
        self._nutritioncarbs = nutritioncarbs

    # a name getter method, extracts name from object
    @property
    def nutritionname(self):
        return self._nutritionname
    # a setter function, allows name to be updated after initial object creation
    @nutritionname.setter
    def nutritionname(self, nutritionname):
        self._nutritionname = nutritionname
        
    # a getter method, extracts link from object
    @property
    def nutritioncalories(self):
        return self._nutritioncalories
    # a setter function, allows link to be updated after initial object creation
    @nutritioncalories.setter
    def recipelink(self, nutritioncalories):
        self._nutritioncalories = nutritioncalories
        
    # a getter method, extracts link from object
    @property
    def nutritionfat(self):
        return self._nutritionfat
    # a setter function, allows link to be updated after initial object creation
    @nutritionfat.setter
    def recipetype(self, nutritionfat):
        self._nutritionfat = nutritionfat

    # a getter method, extracts link from object
    @property
    def nutritioncarbs(self):
        return self._nutritioncarbs
    # a setter function, allows link to be updated after initial object creation
    @nutritioncarbs.setter
    def recipecuisine(self, nutritioncarbs):
        self._nutritioncarbs = nutritioncarbs
        
    
    @property
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
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
            "nutritionname" : self.nutritionname,
            "nutritioncalories" : self.nutritioncalories,
            "nutritionfat" : self.nutritionfat,
            "nutritioncarbs" : self.nutritioncarbs,
        }
    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, nutritionname="", nutritioncalories="", nutritionfat="", nutritioncarbs=""):
        """only updates values with length"""
        if len(nutritionname) > 0:
            self.nutritionname = nutritionname
        if len(nutritioncalories) > 0:
            self.nutritioncalories = nutritioncalories
        if len(nutritionfat) > 0:
            self.nutritionfat = nutritionfat
        if len(nutritioncarbs) > 0:
            self.nutritioncarbs = nutritioncarbs
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initNutrition():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        r1 = Nutrition(nutritionname='Apple', nutritioncalories='94 cal', nutritionfat='0.31g', nutritioncarbs='20.77 g')
        r2 = Nutrition(nutritionname='Flour', nutritioncalories='455.00 kcal', nutritionfat=' 1.23 g', nutritioncarbs='92.01 g')
        r3 = Nutrition(nutritionname='Orange', nutritioncalories=' 61.57 kcal', nutritionfat='0.16 g', nutritioncarbs='12.25 g')
        r4 = Nutrition(nutritionname='Milk', nutritioncalories='148.84 kcal', nutritionfat='7.93 g', nutritioncarbs=' 11.71 g')
        r5 = Nutrition(nutritionname='Egg', nutritioncalories='61.49 kcal', nutritionfat='4.09 g', nutritioncarbs=' 0.31 g')
        
    
        nutritions = [r1, r2, r3, r4, r5]

        """Builds sample user/note(s) data"""
        for nutrition in nutritions:
            try:
                nutrition.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {nutrition.model}")