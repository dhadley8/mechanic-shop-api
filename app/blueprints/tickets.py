from flask import Blueprint, request
from sqlalchemy import select
from marshmallow import ValidationError
from app import db
from app.models import ServiceTicket, Customer
from app.schemas import TicketSchema
from app.utils.util import token_required

tickets_bp = Blueprint('tickets', __name__)
ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)

@tickets_bp.route('/', methods=['GET'])
def get_tickets():
    tickets = db.session.query(ServiceTicket).all()
    return tickets_schema.jsonify(tickets)

@tickets_bp.route('/', methods=['POST'])
def add_ticket():
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    customer = db.session.get(Customer, ticket_data['customer_id'])
    if not customer:
        return {"message": "Customer not found"}, 404

    new_ticket = ServiceTicket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.jsonify(new_ticket), 201

@tickets_bp.route('/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return {"message": "Ticket not found"}, 404
    return ticket_schema.jsonify(ticket)

@tickets_bp.route('/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return {"message": "Ticket not found"}, 404
    try:
        ticket_data = ticket_schema.load(request.json, partial=True)
    except ValidationError as err:
        return {"errors": err.messages}, 400
    if 'customer_id' in ticket_data:
        customer = db.session.get(Customer, ticket_data['customer_id'])
        if not customer:
            return {"message": "Customer not found"}, 404
    for key, value in ticket_data.items():
        setattr(ticket, key, value)
    db.session.commit()
    return ticket_schema.jsonify(ticket)

@tickets_bp.route('/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return {"message": "Ticket not found"}, 404
    db.session.delete(ticket)
    db.session.commit()
    return {"message": "Ticket deleted"}

@tickets_bp.route('/my-tickets', methods=['GET'])
@token_required
def my_tickets(customer_id):
    tickets = db.session.query(ServiceTicket).filter_by(customer_id=customer_id).all()
    return tickets_schema.jsonify(tickets)