import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.recipes import Recipe

recipe_api = Blueprint('recipe_api', __name__,
                   url_prefix='/api/recipe')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(recipe_api)

class RecipeAPI:       
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            recipeName = body.get('recipeName')
            if recipeName is None or len(recipeName) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            # validate uid
            recipeId = body.get('recipeId')
            if recipeId is None or len(recipeId) < 2:
                return {'message': f'Recipe ID is missing, or is less than 2 characters'}, 210
            # look for password and dob
            #password = body.get('password')
            #dob = body.get('dob')
            recipeLink = body.get('recipeLink')
            recipeType = body.get('recipeType')
            recipeCalories = body.get('recipeCalories')
           
            ''' #1: Key code block, setup Recipe OBJECT '''
            ro = recipe(recipename=recipeName, 
                      recipeid=recipeId,recipeLink=recipeLink,recipeType=recipeType,recipeCalories=recipeCalories)
            
            ''' Additional garbage error checking '''
            # set password if provided
           # if password is not None:
            #    uo.set_password(password)
            # convert to date type
            # if dob is not None:
            #     try:
            #         uo.dob = datetime.strptime(dob, '%m-%d-%Y').date()
            #     except:
            #         return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 210
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            recipe = ro.create()
            # success returns json of user
            if recipe:
                return jsonify(recipe.read())
            # failure returns error
            return {'message': f'Processed {recipeName}, either a format error or Recipe ID {recipeId} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            recipes = Recipe.query.all()    # read/extract all users from database
            json_ready = [recipe.read() for recipe in recipes]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')