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
class Recipe(db.Model):
    __tablename__ = 'recipes'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, unique=True, primary_key=True)
    _recipename = db.Column(db.String(255), unique=False, nullable=False)
    _recipelink = db.Column(db.String(255), unique=False, nullable=False)

    # Defines a relationship between Recipe record and Notes table, one-to-many (one recipe to many notes)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, recipename, recipelink, recipetype):
        self._recipename = recipename    # variables with self prefix become part of the object, 
        self._recipelink = recipelink

    # a name getter method, extracts name from object
    @property
    def recipename(self):
        return self._recipename
    # a setter function, allows name to be updated after initial object creation
    @recipename.setter
    def recipename(self, recipename):
        self._recipename = recipename
        
    # a getter method, extracts link from object
    @property
    def recipelink(self):
        return self._recipelink
    # a setter function, allows link to be updated after initial object creation
    @recipelink.setter
    def recipelink(self, recipelink):
        self._recipelink = recipelink
        
    
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
            "recipename" : self.recipename,
            "recipelink" : self.recipelink,
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, recipename="", recipelink=""):
        """only updates values with length"""
        if len(recipename) > 0:
            self.recipename = recipename
        if len(recipelink) > 0:
            self.recipelink = recipelink
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
def initRecipes():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        r1 = Recipe(recipename='Baked Feta Pasta', recipelink='https://www.foodnetwork.com/recipes/food-network-kitchen/baked-feta-pasta-9867689')
        r2 = Recipe(recipename='Kale Salad', recipelink='https://www.loveandlemons.com/kale-salad/')
        r3 = Recipe(recipename='Turkey Burgers', recipelink='https://www.kimscravings.com/easy-turkey-burgers/')
        r4 = Recipe(recipename='Lentil Soup', recipelink='https://www.recipetineats.com/lentil-soup/')
        r5 = Recipe(recipename='Caramelized Onion Mushroom Pizza', recipelink='https://showmetheyummy.com/caramelized-onion-mushroom-pizza-recipe/')
        r6 = Recipe(recipename='Banana Bread', recipelink='https://www.simplyrecipes.com/recipes/banana_bread/')
        r7 = Recipe(recipename='Chicken Fajitas', recipelink='https://healthyrecipesblogs.com/easy-chicken-fajitas/')
        r8 = Recipe(recipename='Quick Tacos', recipelink='https://www.acouplecooks.com/quick-dinner-idea-5-minute-tacos/')
        r9 = Recipe(recipename='Garlic Butter Shrimp', recipelink='https://www.acouplecooks.com/garlic-butter-shrimp/')
        r10 = Recipe(recipename='Mediterranean Tuna Salad', recipelink='https://www.acouplecooks.com/mediterranean-tuna-salad/')
    
        recipes = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]

        for recipe in recipes:
            try:
                recipe.create()
            except IntegrityError:
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {recipe.model}")