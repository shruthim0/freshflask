import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.fridges import Fridge

fridge_api = Blueprint('fridge_api', __name__,
                   url_prefix='/api/fridges')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(fridge_api)

class FridgeAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate recipename
            recname = body.get('recname')
            if recname is None or len(recname) < 2:
                return {'message': f'recname is missing, or is less than 2 characters'}, 400
            # validate recipelink
            reclink = body.get('reclink')
            if reclink is None or len(reclink) < 2:
                return {'message': f'reclink is missing, or is less than 2 characters'}, 400

            ''' #1: Key code block, setup USER OBJECT '''
            ro = Fridge(recname=recname, 
                      reclink=reclink)
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            fridge = ro.create()
            # success returns json of user
            if fridge:
                return jsonify(fridge.read())
            # failure returns error
            return {'message': f'Error or User ID {recname} is duplicate'}, 400

    class _Read(Resource):
        def get(self):
            fridges = Fridge.query.all()    # read/extract all users from database
            json_ready = [fridge.read() for fridge in fridges]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')