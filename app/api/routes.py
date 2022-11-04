from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}


@api.route('/cars', methods=['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    vin = request.json['vin']
    year = request.json['year']
    user_token = current_user_token.token

    print(f'Big Test: {current_user_token.token}')

    car = Car(make, model, vin, year)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(current_user_token.token, car)
    return jsonify(response)


@api.route('/cars', methods=['GET'])
@token_required
def get_car(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token=a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)
