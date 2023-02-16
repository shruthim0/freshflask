import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.recipes import Recipe

recipe_api = Blueprint('recipe_api', __name__,
                   url_prefix='/api/recipes')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(recipe_api)

class RecipeAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate recipename
            recipename = body.get('recipename')
            if recipename is None or len(recipename) < 2:
                return {'message': f'recipename is missing, or is less than 2 characters'}, 400
            # validate recipelink
            recipelink = body.get('recipelink')
            if recipelink is None or len(recipelink) < 2:
                return {'message': f'recipelink is missing, or is less than 2 characters'}, 400
            # validate recipetype
            recipetype = body.get('recipetype')
            if recipetype is None or len(recipetype) < 2:
                return {'message': f'recipetype is missing, or is less than 2 characters'}, 400

            ''' #1: Key code block, setup USER OBJECT '''
            ro = Recipe(recipename=recipename, 
                      recipelink=recipelink,
                      recipetype=recipetype)
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            recipe = ro.create()
            # success returns json of user
            if recipe:
                return jsonify(recipe.read())
            # failure returns error
            return {'message': f'Processed {recipetype}, either a format error or User ID {recipename} is duplicate'}, 400

    class _Read(Resource):
        def get(self):
            recipes = Recipe.query.all()    # read/extract all users from database
            json_ready = [recipe.read() for recipe in recipes]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')