import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.fridges import Fridge

rec_api = Blueprint('rec_api', __name__,
                   url_prefix='/api/recs')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(rec_api)

class FridgeAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate recipename
            recname = body.get('recipename')
            if recname is None or len(recname) < 2:
                return {'message': f'recipename is missing, or is less than 2 characters'}, 400
            # validate recipelink
            reclink = body.get('recipelink')
            if reclink is None or len(reclink) < 2:
                return {'message': f'recipelink is missing, or is less than 2 characters'}, 400

            ''' #1: Key code block, setup USER OBJECT '''
            ro = Fridge(recname=recname, 
                      reclink=reclink)
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            rec = ro.create()
            # success returns json of user
            if rec:
                return jsonify(rec.read())
            # failure returns error
            return {'message': f'Error or User ID {recname} is duplicate'}, 400

    class _Read(Resource):
        def get(self):
            recs = Fridge.query.all()    # read/extract all users from database
            json_ready = [rec.read() for rec in recs]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')