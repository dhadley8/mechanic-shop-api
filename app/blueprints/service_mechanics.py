from flask import Blueprint, request
from marshmallow import ValidationError
from app import db
from app.models import ServiceMechanic, ServiceTicket
from app.schemas import ServiceMechanicSchema

service_mechanics_bp = Blueprint('service_mechanics', __name__)
service_mechanic_schema = ServiceMechanicSchema()
service_mechanics_schema = ServiceMechanicSchema(many=True)

@service_mechanics_bp.route('/', methods=['GET'])
def get_service_mechanics():
    service_mechanics = db.session.query(ServiceMechanic).all()
    return service_mechanics_schema.jsonify(service_mechanics)

@service_mechanics_bp.route('/', methods=['POST'])
def add_service_mechanic():
    try:
        service_mechanic_data = service_mechanic_schema.load(request.json)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    ticket = db.session.get(ServiceTicket, service_mechanic_data['ticket_id'])
    if not ticket:
        return {"message": "Ticket not found"}, 404

    new_service_mechanic = ServiceMechanic(**service_mechanic_data)
    db.session.add(new_service_mechanic)
    db.session.commit()
    return service_mechanic_schema.jsonify(new_service_mechanic), 201

@service_mechanics_bp.route('/<int:ticket_id>', methods=['GET'])
def get_service_mechanic(ticket_id):
    service_mechanic = db.session.get(ServiceMechanic, ticket_id)
    if not service_mechanic:
        return {"message": "Service Mechanic not found"}, 404
    return service_mechanic_schema.jsonify(service_mechanic)

@service_mechanics_bp.route('/<int:ticket_id>', methods=['PUT'])
def update_service_mechanic(ticket_id):
    service_mechanic = db.session.get(ServiceMechanic, ticket_id)
    if not service_mechanic:
        return {"message": "Service Mechanic not found"}, 404
    try:
        service_mechanic_data = service_mechanic_schema.load(request.json, partial=True)
    except ValidationError as err:
        return {"errors": err.messages}, 400
    for key, value in service_mechanic_data.items():
        setattr(service_mechanic, key, value)
    db.session.commit()
    return service_mechanic_schema.jsonify(service_mechanic)

@service_mechanics_bp.route('/<int:ticket_id>', methods=['DELETE'])
def delete_service_mechanic(ticket_id):
    service_mechanic = db.session.get(ServiceMechanic, ticket_id)
    if not service_mechanic:
        return {"message": "Service Mechanic not found"}, 404
    db.session.delete(service_mechanic)
    db.session.commit()
    return {"message": "Service Mechanic deleted"}