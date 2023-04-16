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
    __tablename__ = 'fridges'  # creates the table

    # defines the User schema
    id = db.Column(db.Integer, unique=True, primary_key=True)
    _recname = db.Column(db.String(255), unique=False, nullable=False)
    _reclink = db.Column(db.String(255), unique=False, nullable=False)



    # initializes the instance variables within object (self)
    def __init__(self, recname, reclink):
        self._recname = recname    # variables with self prefix become part of the object, 
        self._reclink = reclink

    # extracts the recipe name
    @property
    def recname(self):
        return self._recname
    # allows the name to be updated
    @recname.setter
    def recname(self, recname):
        self._recname = recname
        
    # axtracts the recipe link
    @property
    def reclink(self):
        return self._reclink
    # allows the link to be updated
    @reclink.setter
    def reclink(self, reclink):
        self._reclink = reclink
        
    
    @property
    # readable output
    # prep for API response
    def __str__(self):
        return json.dumps(self.read())

    # Create: adds a new recipe to the table
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None # returns "none" or what is enetered if there is an error

    # Read: converts the data into a dictionary
    def read(self):
        return {
            "id": self.id,
            "recname" : self.recname,
            "reclink" : self.reclink,
        }

    # Update: updates recipe entered
    def update(self, recname="", reclink=""):
        if len(recname) > 0:
            self.recname = recname
        if len(reclink) > 0:
            self.reclink = reclink
        db.session.commit()
        return self

    # Delete: removes recipe
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initFridges():
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
    
        fridges = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]

        # creates sample table of data
        for fridge in fridges:
            try:
                fridge.create()
            except IntegrityError:
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {fridge.model}")