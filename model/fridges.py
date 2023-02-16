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
class Fridge(db.Model):
    __tablename__ = 'recs'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, unique=True, primary_key=True)
    _recname = db.Column(db.String(255), unique=False, nullable=False)
    _reclink = db.Column(db.String(255), unique=False, nullable=False)

    # Defines a relationship between Recipe record and Notes table, one-to-many (one recipe to many notes)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, recname, reclink):
        self._recname = recname    # variables with self prefix become part of the object, 
        self._reclink = reclink

    # a name getter method, extracts name from object
    @property
    def recname(self):
        return self._recname
    # a setter function, allows name to be updated after initial object creation
    @recname.setter
    def recname(self, recname):
        self._recname = recname
        
    # a getter method, extracts link from object
    @property
    def reclink(self):
        return self._reclink
    # a setter function, allows link to be updated after initial object creation
    @reclink.setter
    def reclink(self, reclink):
        self._reclink = reclink
        
    
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
            "recipename" : self.recname,
            "recipelink" : self.reclink,
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, recname="", reclink=""):
        """only updates values with length"""
        if len(recname) > 0:
            self.recname = recname
        if len(reclink) > 0:
            self.reclink = reclink
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
def initRecs():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        r1 = Fridge(recname='Baked Feta Pasta', reclink='https://www.foodnetwork.com/recipes/food-network-kitchen/baked-feta-pasta-9867689')
        r2 = Fridge(recname='Kale Salad', reclink='https://www.loveandlemons.com/kale-salad/')
        r3 = Fridge(recname='Turkey Burgers', reclink='https://www.kimscravings.com/easy-turkey-burgers/')
        r4 = Fridge(recname='Lentil Soup', reclink='https://www.recipetineats.com/lentil-soup/')
        r5 = Fridge(recname='Caramelized Onion Mushroom Pizza', reclink='https://showmetheyummy.com/caramelized-onion-mushroom-pizza-recipe/')
        r6 = Fridge(recname='Banana Bread', reclink='https://www.simplyrecipes.com/recipes/banana_bread/')
        r7 = Fridge(recname='Chicken Fajitas', reclink='https://healthyrecipesblogs.com/easy-chicken-fajitas/')
        r8 = Fridge(recname='Quick Tacos', reclink='https://www.acouplecooks.com/quick-dinner-idea-5-minute-tacos/')
        r9 = Fridge(recname='Garlic Butter Shrimp', reclink='https://www.acouplecooks.com/garlic-butter-shrimp/')
        r10 = Fridge(recname='Mediterranean Tuna Salad', reclink='https://www.acouplecooks.com/mediterranean-tuna-salad/')
    
        recs = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]

        for rec in recs:
            try:
                rec.create()
            except IntegrityError:
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {rec.model}")