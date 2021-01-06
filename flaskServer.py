from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps
import json
from flask_cors import CORS

import sqlConnections

app = Flask(__name__)

cors = CORS(app)

app.config['SECRET_KEY'] = 'ItsSecret'


def token_required(f):
    @wraps(f)
    def checkToken(*args, **kwargs):

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            payload = jwt.decode(token, app.config.get(
                'SECRET_KEY'), algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token Expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(payload, *args, **kwargs)

    return checkToken


@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    if data['username'] == '' or data['password'] == "":
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    if sqlConnections.authUser(data['username'], data['password']):
        token = jwt.encode({'username': data['username'], 'password': data['password'], 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=60)}, app.config.get('SECRET_KEY'), algorithm='HS256')
        return jsonify({'token': token})
    else:
        return jsonify({"message": "Invalid Credentials"})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/list')
@token_required
def list(userDetails):
    if sqlConnections.authUser(userDetails['username'], userDetails["password"]):
        placesList = sqlConnections.getList()
        # places = ""
        # for place in placesList:
        #     places += '<h1> {} </h1>'.format(place)
        # print(places)
        return jsonify(placesList)
    else:
        return jsonify({'message': 'Validation Error!'})


@app.route('/count')
@token_required
def count(userDetails):
    count = sqlConnections.getCount()
    return jsonify(count)  # '<h1> {} </h1>'.format(count)


@app.route('/stats')
@token_required
def stats(userDetails):
    return sqlConnections.getStats()


@app.route('/search')
@token_required
def search(userDetails):
    king = request.args.get('king', None)
    location = request.args.get('location', None)
    type = request.args.get('type', None)
    if king is None:
        return '<h1> Parameter king is required </h1>'
    if location is not None and type != None:
        return sqlConnections.getBattlesByNameLocationType(king, location, type)
    if location != None:
        return sqlConnections.getBattlesByNameLocation(king, location)
    if type != None:
        return sqlConnections.getBattlesByNameType(king, type)
    return sqlConnections.getBattlesByName(king)


@app.route('/api/battle', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def battle(userDetails):
    data = request.get_json()
    if 'battleName' in data.keys():
        if request.method == 'POST':
            result = sqlConnections.createBattle(data['battleName'])
            return jsonify({"status": result})
        if request.method == 'GET':
            result = sqlConnections.readBattle(data['battleName'])
            return jsonify({"status": result})
        if request.method == 'DELETE':
            result = sqlConnections.deleteBattle(data['battleName'])
            return jsonify({"status": result})
        if request.method == 'PUT' and 'newBattleName' in data.keys():
            result = sqlConnections.updateBattle(
                data['battleName'], data['newBattleName'])
            return jsonify({"status": result})
        else:
            return jsonify({"message": "Parameters Invalid"})
    else:
        return jsonify({"message": "Parameters Invalid"})


app.run(debug=True)
