import os, sys
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all ,setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

#-----------------------------------------------------------------------------------------------!
# @TODO uncomment the following line to initialize the datbase
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
# !! Running this funciton will add one

# completed
# This drops existing database and creates new database!
#-----------------------------------------------------------------------------------------------!
with app.app_context():
    db_drop_and_create_all()
    
    
#-----------------------------------------------------------------------------------------------!
# ROUTES
#-----------------------------------------------------------------------------------------------!
#-----------------------------------------------------------------------------------------------!
# GET/ get short drink list
#-----------------------------------------------------------------------------------------------!
#-----------------------------------------------------------------------------------------------!
# @TODO implement endpoint
#     GET /drinks
#         it should be a public endpoint
#         it should contain only the drink.short() data representation
#     returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
#         or appropriate status code indicating reason for failure

# completed
# This endpoint return short list of the drink details
# All users, baristas, Managers can access this endpoint withour authorization.
#-----------------------------------------------------------------------------------------------!
@app.route('/drinks')
def get_short_drinks_list():
    all_drinks = Drink.query.all()
    try:
        if len(all_drinks) == 0:
            abort(404)
        short_list = [drink.short() for drink in all_drinks]
        return jsonify({
            'success': True,
            'drinks': short_list
        }), 200
    except AuthError:
        abort(422)

#-----------------------------------------------------------------------------------------------!
# GET/ get detailed drink list
#-----------------------------------------------------------------------------------------------!
#-----------------------------------------------------------------------------------------------!
# @TODO implement endpoint
#     GET /drinks-detail
#         it should require the 'get:drinks-detail' permission
#         it should contain the drink.long() data representation
#         returns status code 200 and json {"success": True, "drinks": drinks} 
#         where drinks is the list of drinks
#         or appropriate status code indicating reason for failure

# completed
# This endpoint returns the detailed or long list of the drinks.
# Baristas and Managers can access this endpoint. 
# Permission - "get:drinks-detail"
#-----------------------------------------------------------------------------------------------!
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_long_drinks_list(payload):
    try:
        all_drinks = Drink.query.all()
        if len(all_drinks) == 0:
            abort(404)
        long_list = [drink.long() for drink in all_drinks]
        return jsonify({
            'success': True,
            'drinks': long_list
        }), 200
    except AuthError:
        abort(422)

#-----------------------------------------------------------------------------------------------!
# POST/ Add New Drink
#-----------------------------------------------------------------------------------------------!
#-----------------------------------------------------------------------------------------------!
# @TODO implement endpoint
#     POST /drinks
#         it should create a new row in the drinks table
#         it should require the 'post:drinks' permission
#         it should contain the drink.long() data representation
#         returns status code 200 and json {"success": True, "drinks": drink} 
#         where drink an array containing only the newly created drink
#         or appropriate status code indicating reason for failure

# completed
# This endpoint allows to create new drink.
# Only Managers can access this endpoint.
# Permission - "post:drinks"
#-----------------------------------------------------------------------------------------------!
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(payload):
    new_drink_title = request.get_json().get('title')
    new_drink_recipe = json.dumps(request.get_json().get('recipe'))
    try:
        if new_drink_title is None or new_drink_recipe is None:
            abort(404)
        add_new_drink = Drink(title=new_drink_title,recipe=new_drink_recipe)
        add_new_drink.insert()
        drink_list = Drink.query.filter(Drink.title==new_drink_title).one()
        return jsonify({
            'success': True,
            'drinks': [drink_list.long()]
        }), 200
    except AuthError:
        abort(403)
    
    
#-----------------------------------------------------------------------------------------------!
# PATCH/ Edit Drink
#-----------------------------------------------------------------------------------------------!
#-----------------------------------------------------------------------------------------------!
# @TODO implement endpoint
#     PATCH /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should update the corresponding row for <id>
#         it should require the 'patch:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
#         or appropriate status code indicating reason for failure

# completed
# This endpoint allows to update the drink name or its receipe.
# Only Manager can access this endpoint
# Permission - "patch:drinks"
#-----------------------------------------------------------------------------------------------!
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def change_data(payload, id):
    get_drink = Drink.query.filter(Drink.id==id).one_or_none()
    try:
        updated_title = request.get_json().get('title')
        updated_recipe = json.dumps(request.get_json().get('recipe'))
        get_drink.recipe = updated_recipe
        get_drink.title = updated_title
        get_drink.update()
        
        return jsonify({
            'success': True,
            'drinks': [get_drink.long()]
        }), 200
    except AuthError:
        abort(422)


#-----------------------------------------------------------------------------------------------!
# DELETE/ Delete Drink
#-----------------------------------------------------------------------------------------------!
#-----------------------------------------------------------------------------------------------!
# @TODO implement endpoint
#     DELETE /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should delete the corresponding row for <id>
#         it should require the 'delete:drinks' permission
#     returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
#         or appropriate status code indicating reason for failure

# completed
# This endpoint allows to delete any drink.
# Only Manager can access this endpoint.
# Permission - "delete:drinks"
#-----------------------------------------------------------------------------------------------!
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_a_drink(payload, id):
    drink_to_be_deleted = Drink.query.filter(Drink.id==id).one_or_none()
    try:
        drink_to_be_deleted.delete()
        return jsonify({
            'success': True,
            'delete_id': id
        }), 200
    except AuthError:
        abort(422)

#-----------------------------------------------------------------------------------------------!
# Error Handling
#-----------------------------------------------------------------------------------------------!
#-----------------------------------------------------------------------------------------------!
# @TODO implement error handlers using the @app.errorhandler(error) decorator
#     each error handler should return (with approprate messages):
#              jsonify({
#                     "success": False,
#                     "error": 404,
#                     "message": "resource not found"
#                     }), 404
# @TODO implement error handler for 404
#     error handler should conform to general task above

# completed
# Errors handled - 400, 401, 403, 404, 422, 500 
#-----------------------------------------------------------------------------------------------!
@app.errorhandler(400)
def bad_request(error):
    print(sys.exc_info())
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400
    
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401
    
@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'forbidden to access'
    }), 403
    
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Requested Resource Not Found'
    }), 404
    
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500


#-----------------------------------------------------------------------------------------------!
# @TODO implement error handler for AuthError
#     error handler should conform to general task above

# completed
# This handles any error raising AuthError.
# reference from https://knowledge.udacity.com/questions/538174
#-----------------------------------------------------------------------------------------------!
@app.errorhandler(AuthError)
def auth_error_handler(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response