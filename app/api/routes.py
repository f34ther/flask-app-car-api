from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/cars', methods=['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    vin = request.json['vin']
    year = request.json['year']
    user_token = current_user_token.token

    print(f'Test: {current_user_token}')

    cars = Car(make, model, vin, year, user_token=user_token)

    db.session.add(cars)
    db.session.commit()

    response = car_schema.dump(cars)
    return jsonify(response)


@api.route('/cars', methods=['GET'])
@token_required
def get_cars(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token=a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)


@api.route('/cars/id', methods=['GET'])
@token_required
def get_single_car(current_user_token, id):
    car = Car.query.get(id)
    car.user_token = current_user_token.token
    response = car_schema.dump(car)
    return jsonify(response)


@api.route('/cars/<id>', methods=['PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.vin = request.json['vin']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)


@api.route('/cars/<id>', methods=['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    car.user_token = current_user_token.token
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)
