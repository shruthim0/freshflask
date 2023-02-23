import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.nutritions import Nutrition

nutrition_api = Blueprint('nutriton_api', __name__,
                   url_prefix='/api/nutriitons')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(nutrition_api)

class RecipeAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate nutritionname
            nutritionname = body.get('nutritionname')
            if nutritionname is None or len(nutritionname) < 2:
                return {'message': f'nutritionname is missing, or is less than 2 characters'}, 400
            # validate nutritioncalories
            nutritioncalories = body.get('nutritioncalories')
            if nutritioncalories is None or len(nutritioncalories) < 2:
                return {'message': f'nutritioncalories is missing, or is less than 2 characters'}, 400
            # validate nutritionfat
            nutritionfat = body.get('nutritionfat')
            if nutritionfat is None or len(nutritionfat) < 2:
                return {'message': f'nutritionfat is missing, or is less than 2 characters'}, 400
            # validate nutritioncarbs
            nutritioncarbs = body.get('nutritioncarbs')
            if nutritioncarbs is None or len(nutritioncarbs) < 2:
                return {'message': f'nutritioncarbs is missing, or is less than 2 characters'}, 400

            ''' #1: Key code block, setup USER OBJECT '''
            ro = Nutrition(nutritionname=nutritionname, 
                      nutritioncalories=nutritioncalories,
                      nutritionfat=nutritionfat,
                      nutritioncarbs=nutritioncarbs)
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            nutrition = ro.create()
            # success returns json of user
            if nutrition:
                return jsonify(nutrition.read())
            # failure returns error
            return {'message': f' User ID {nutritionname} is duplicate'}, 400

    class _Read(Resource):
        def get(self):
            nutritions = Nutrition.query.all()    # read/extract all users from database
            json_ready = [nutrition.read() for nutrition in nutritions]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')