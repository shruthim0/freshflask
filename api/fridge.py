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
            body = request.get_json()
            
            # error checking
            # validate recipename
            recname = body.get('recname')
            if recname is None or len(recname) < 2:
                return {'message': f'recname is missing, or is less than 2 characters'}, 400
            # validate recipelink
            reclink = body.get('reclink')
            if reclink is None or len(reclink) < 2:
                return {'message': f'reclink is missing, or is less than 2 characters'}, 400

            # sets up the recipe in the database
            ro = Fridge(recname=recname, 
                      reclink=reclink)
            
            # create recipe in database
            fridge = ro.create()
            # success returns json of recipe
            if fridge:
                return jsonify(fridge.read())
            # failure returns error
            return {'message': f'Error or User ID {recname} is duplicate'}, 400

    class _Read(Resource):
        def get(self):
            fridges = Fridge.query.all()    # extracts all recipes from database
            json_ready = [fridge.read() for fridge in fridges]  # prepares output in json
            return jsonify(json_ready) 
    
            # deletes recipes from table
    class _Delete(Resource):
        def delete(self):
            Fridge.session.query(self).delete()
            Fridge.session.commit()
            return {'message': 'All recipes have been deleted.'}

    class _Security(Resource):

        def post(self):
            body = request.get_json()
            
            # fetches the data
            _recname = body.get('recname')
            if _recname is None or len(_recname) < 2:
                return {'message': f'recipe name is missing, or is less than 2 characters'}, 400
            _reclink = body.get('reclink')
            
            # finds the recipe
            user = Fridge.query.filter_by(_recname).first()
            if user is None or not user.is_reclink(_reclink):
                return {'message': f"Invalid recipe or link"}, 400
            
            # authenticates the recipe
            return jsonify(user.read())

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_Delete, '/delete')
    api.add_resource(_Security, '/authenticate')