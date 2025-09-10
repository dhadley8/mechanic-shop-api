from flask import Blueprint, request
from marshmallow import ValidationError
from app import db
from app.models import Mechanic
from app.schemas import MechanicSchema

mechanics_bp = Blueprint('mechanics', __name__)
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    mechanics = db.session.query(Mechanic).all()
    return mechanics_schema.jsonify(mechanics)

@mechanics_bp.route('/', methods=['POST'])
def add_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

@mechanics_bp.route('/<int:mechanic_id>', methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return {"message": "Mechanic not found"}, 404
    return mechanic_schema.jsonify(mechanic)

@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return {"message": "Mechanic not found"}, 404
    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True)
    except ValidationError as err:
        return {"errors": err.messages}, 400
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic)

@mechanics_bp.route('/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return {"message": "Mechanic not found"}, 404
    db.session.delete(mechanic)
    db.session.commit()
    return {"message": "Mechanic deleted"}