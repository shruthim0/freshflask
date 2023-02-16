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
    _recipetype = db.Column(db.String(255), unique=False, nullable=False)
    _recipecuisine = db.Column(db.String(255), unique=False, nullable=False)

    # Defines a relationship between Recipe record and Notes table, one-to-many (one recipe to many notes)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, recipename, recipelink, recipetype, recipecuisine):
        self._recipename = recipename    # variables with self prefix become part of the object, 
        self._recipelink = recipelink
        self._recipetype = recipetype
        self._recipecuisine = recipecuisine

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
        
    # a getter method, extracts link from object
    @property
    def recipetype(self):
        return self._recipetype
    # a setter function, allows link to be updated after initial object creation
    @recipetype.setter
    def recipetype(self, recipetype):
        self._recipetype = recipetype

    # a getter method, extracts link from object
    @property
    def recipecuisine(self):
        return self._recipecuisine
    # a setter function, allows link to be updated after initial object creation
    @recipecuisine.setter
    def recipecuisine(self, recipecuisine):
        self._recipecuisine = recipecuisine
        
    
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
            "recipetype" : self.recipetype,
            "recipecuisine" : self.recipecuisine,
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, recipename="", recipelink="", recipetype="", recipecuisine=""):
        """only updates values with length"""
        if len(recipename) > 0:
            self.recipename = recipename
        if len(recipelink) > 0:
            self.recipelink = recipelink
        if len(recipetype) > 0:
            self.recipetype = recipetype
        if len(recipecuisine) > 0:
            self.recipecuisine = recipecuisine
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
        r1 = Recipe(recipename='Avocado Toast', recipelink='link1', recipetype='Breakfast', recipecuisine='American')
        r2 = Recipe(recipename='Scrambled Eggs', recipelink='link2', recipetype='Breakfast', recipecuisine='American')
        r3 = Recipe(recipename='Pancake', recipelink='link3', recipetype='Breakfast', recipecuisine='American')
        r4 = Recipe(recipename='Mac and Cheese', recipelink='link4', recipetype='Lunch', recipecuisine='American')
        r5 = Recipe(recipename='Panini Sandwich', recipelink='link5', recipetype='Lunch', recipecuisine='French')
        r6 = Recipe(recipename='Salad', recipelink='link6', recipetype='Lunch', recipecuisine='Mediterranean')
        r7 = Recipe(recipename='Minestrone Soup', recipelink='link7', recipetype='Dinner', recipecuisine='Italian')
        r8 = Recipe(recipename='Lasagna', recipelink='link8', recipetype='Dinner', recipecuisine='Italian')
        r9 = Recipe(recipename='Pasta', recipelink='link9', recipetype='Dinner', recipecuisine='Italian')
        r10 = Recipe(recipename='Brownies', recipelink='link10', recipetype='Dessert', recipecuisine='German')
        r11 = Recipe(recipename='Chocolate Chip Cookies', recipelink='link11', recipetype='Dessert', recipecuisine='American')
        r12 = Recipe(recipename='Custard Pudding', recipelink='link12', recipetype='Dessert', recipecuisine='German')
    
        recipes = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12]

        """Builds sample user/note(s) data"""
        for recipe in recipes:
            try:
                recipe.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {recipe.model}")