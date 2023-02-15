""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Recipe(db.Model):
    __tablename__ = 'recipes'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    recipeId = db.Column(db.Integer, primary_key=True)
    _recipeName = db.Column(db.String(255), unique=False, nullable=False)
    _recipeLink = db.Column(db.String(255), unique=False, nullable=False)
    _recipeType = db.Column(db.String(255), unique=False, nullable=False)
    _reciperecipeCalories = db.Column(db.Integer, unique=False, nullable=False)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, recipeName, recipeId, recipeLink, recipeType, reciperecipeCalories):
        self._recipeName = recipeName    # variables with self prefix become part of the object, 
        self._recipeLink = recipeLink
        self._recipeType = recipeType
        self._recipeCalories = reciperecipeCalories

    # a name getter method, extracts name from object
    @property
    def recipeName(self):
        return self._recipeName
    
    # a setter function, allows name to be updated after initial object creation
    @recipeName.setter
    def recipeName(self, recipe):
        self._recipeName = recipeName
    
    # a getter method, extracts email from object
    @property
    def recipeId(self):
        return self._recipeId
    
    # a setter function, allows name to be updated after initial object creation
    @recipeId.setter
    def recipeId(self, recipeId):
        self._recipeId = recipeId
        
    # check if uid parameter matches user id in object, return boolean
    def is_recipeId(self, recipeId):
        return self._recipeId == recipeId
    
    # link
    @property
    def recipeLink(self):
        return self._recipeLink
    
    @recipeLink.setter
    def recipeName(self, recipeLink):
        self._recipeLink = recipeLink
    
    # type
    @property
    def recipeType(self):
        return self._recipeType
 
    @recipeType.setter
    def recipeType(self, recipeType):
        self._recipeType = recipeType
        
    # recipeCalories
    @property
    def reciperecipeCalories(self):
        return self._reciperecipeCalories
    
    @reciperecipeCalories.setter
    def reciperecipeCalories(self, reciperecipeCalories):
        self._reciperecipeCalories = reciperecipeCalories
        
        
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
            "recipeId": self.recipeId,
            "recipeName": self.recipeName,
            "recipeLink": self.recipeLink,
            "recipeType": self.recipeType,
            "reciperecipeCalories": self.reciperecipeCalories
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, recipeName="", recipeLink="", recipeType=""):
        """only updates values with length"""
        if len(recipeName) > 0:
            self.recipeName = recipeName
        if len(recipeLink) > 0:
            self.recipeLink = recipeLink
        if len(recipeType) > 0:
            self.recipeType(recipeType)
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
    """Create database and tables"""
    db.drop_all()
    db.create_all()
    """Tester data for table"""
    r1 = Recipe(recipeName='Avocado Toast', recipeLink='https://californiaavocado.com/recipes', recipeType='Breakfast', recipeCalories=100)
    r2 = Recipe(recipeName='Scrambled Eggs', recipeLink='https://californiaavocado.com/recipes', recipeType='Breakfast', recipeCalories=100)
    r3 = Recipe(recipeName='Pancake', recipeLink='https://californiaavocado.com/recipes', recipeType='Breakfast', recipeCalories=100)
    r4 = Recipe(recipeName='Mac and Cheese', recipeLink='https://californiaavocado.com/recipes', recipeType='Lunch', recipeCalories=2000)
    r5 = Recipe(recipeName='Panini Sandwich', recipeLink='https://californiaavocado.com/recipes', recipeType='Lunch', recipeCalories=2000)
    r6 = Recipe(recipeName='Salad', recipeLink='https://californiaavocado.com/recipes', recipeType='Lunch', recipeCalories=2000)
    r7 = Recipe(recipeName='Minestrone Soup', recipeLink='https://californiaavocado.com/recipes', recipeType='Dinner', recipeCalories=3000)
    r8 = Recipe(recipeName='Lasagna', recipeLink='https://californiaavocado.com/recipes', recipeType='Dinner', recipeCalories=3000)
    r9 = Recipe(recipeName='Pasta', recipeLink='https://californiaavocado.com/recipes', recipeType='Dinner', recipeCalories=3000)
    r10 = Recipe(recipeName='Brownies', recipeLink='https://californiaavocado.com/recipes', recipeType='Dessert', recipeCalories=400)
    r11 = Recipe(recipeName='Chocolate Chip Cookies', recipeLink='https://californiaavocado.com/recipes', recipeType='Dessert', recipeCalories=400)
    r12 = Recipe(recipeName='Custard Pudding', recipeLink='https://californiaavocado.com/recipes', recipeType='Dessert', recipeCalories=400)
 
    recipes = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12]

    # adding my own tester data for the table
    
    # adding my own tests for bookings class
    bookingID = 1
    """Builds sample user/note(s) data"""
    for recipe in recipes:
        try:
            
            '''add a few 1 to 4 notes per user'''
            '''add user/post data to table'''
            recipe.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {recipe.uid}")
    
    