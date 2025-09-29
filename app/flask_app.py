from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select
from datetime import datetime
from typing import List

from marshmallow import ValidationError

# Define your SQLAlchemy models here if not already defined elsewhere
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Mechanic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Similarly, define Customer, ServiceTicket, and ServiceMechanic models if not already defined

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class ServiceTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vin = db.Column(db.String(50), nullable=False)
    service_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    service_description = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

class ServiceMechanic(db.Model):
    ticket_id = db.Column(db.Integer, db.ForeignKey('service_ticket.id'), primary_key=True)
    mechanic_name = db.Column(db.String(100), nullable=False)









#=========schema definitions=========
class CustomerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer
    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    phone = ma.auto_field()
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


@app.route('/customers', methods=['GET'])
def get_customers():
    customers = db.session.query(Customer).all()
    return customers_schema.jsonify(customers)

@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query).scalars().first()
    if existing_customer:
        return {"message": "Customer with this email already exists."}, 400

    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return {"message": "Customer not found."}, 404
    return customer_schema.jsonify(customer)

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return {"message": "Customer not found."}, 404
    try:
        customer_data = customer_schema.load(request.json, partial=True)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    for key, value in customer_data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer)
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return {"message": "Customer not found."}, 404
    db.session.delete(customer)
    db.session.commit()
    return {"message": "Customer deleted."}, 200


class TicketSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ServiceTicket
    id = ma.auto_field()
    vin = ma.auto_field()
    service_date = ma.auto_field()
    service_description = ma.auto_field()
    customer_id = ma.auto_field()

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)   
@app.route('/tickets', methods=['GET'])
def get_tickets():
    tickets = db.session.query(ServiceTicket).all()
    return tickets_schema.jsonify(tickets)
@app.route('/tickets', methods=['POST'])
def add_ticket():
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    customer = db.session.get(Customer, ticket_data['customer_id'])
    if not customer:
        return {"message": "Customer not found."}, 404

    new_ticket = ServiceTicket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.jsonify(new_ticket), 201
@app.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return {"message": "Ticket not found."}, 404
    return ticket_schema.jsonify(ticket)
@app.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return {"message": "Ticket not found."}, 404
    try:
        ticket_data = ticket_schema.load(request.json, partial=True)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    if 'customer_id' in ticket_data:
        customer = db.session.get(Customer, ticket_data['customer_id'])
        if not customer:
            return {"message": "Customer not found."}, 404

    for key, value in ticket_data.items():
        setattr(ticket, key, value)

    db.session.commit()
    return ticket_schema.jsonify(ticket)
@app.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return {"message": "Ticket not found."}, 404
    db.session.delete(ticket)
    db.session.commit()
    return {"message": "Ticket deleted."}, 200

class service_mechanicshema(ma.SQLAlchemySchema):
    class Meta:
        model = ServiceMechanic
    ticket_id = ma.auto_field()
    mechanic_name = ma.auto_field()
service_mechanic_schema = service_mechanicshema()
service_mechanics_schema = service_mechanicshema(many=True)
@app.route('/service_mechanics', methods=['GET'])
def get_service_mechanics():    
    service_mechanics = db.session.query(ServiceMechanic).all()
    return service_mechanics_schema.jsonify(service_mechanics)
@app.route('/service_mechanics', methods=['POST'])
def add_service_mechanic():  
    try:
        service_mechanic_data = service_mechanic_schema.load(request.json)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    ticket = db.session.get(ServiceTicket, service_mechanic_data['ticket_id'])
    if not ticket:
        return {"message": "Ticket not found."}, 404

    new_service_mechanic = ServiceMechanic(**service_mechanic_data)
    db.session.add(new_service_mechanic)
    db.session.commit()
    return service_mechanic_schema.jsonify(new_service_mechanic), 201
@app.route('/service_mechanics/<int:ticket_id>', methods=['GET'])
def get_service_mechanic(ticket_id):
    service_mechanic = db.session.get(ServiceMechanic, ticket_id)
    if not service_mechanic:
        return {"message": "Service Mechanic not found."}, 404
    return service_mechanic_schema.jsonify(service_mechanic)
@app.route('/service_mechanics/<int:ticket_id>', methods=['PUT'])
def update_service_mechanic(ticket_id):
    service_mechanic = db.session.get(ServiceMechanic, ticket_id)
    if not service_mechanic:
        return {"message": "Service Mechanic not found."}, 404
    try:
        service_mechanic_data = service_mechanic_schema.load(request.json, partial=True)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    if 'ticket_id' in service_mechanic_data:
        ticket = db.session.get(ServiceTicket, service_mechanic_data['ticket_id'])
        if not ticket:
            return {"message": "Ticket not found."}, 404

    for key, value in service_mechanic_data.items():
        setattr(service_mechanic, key, value)

    db.session.commit()
    return service_mechanic_schema.jsonify(service_mechanic)
@app.route('/service_mechanics/<int:ticket_id>', methods=['DELETE'])
def delete_service_mechanic(ticket_id):
    service_mechanic = db.session.get(ServiceMechanic, ticket_id)
    if not service_mechanic:
        return {"message": "Service Mechanic not found."}, 404
    db.session.delete(service_mechanic)
    db.session.commit()
    return {"message": "Service Mechanic deleted."}, 200

class MechanicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Mechanic
    id = ma.auto_field()
    name = ma.auto_field()
    salary = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
@app.route('/mechanics', methods=['GET'])
def get_mechanics():
    mechanics = db.session.query(Mechanic).all()
    return mechanics_schema.jsonify(mechanics)
@app.route('/mechanics', methods=['POST'])
def add_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    query = select(Mechanic).where(Mechanic.email == mechanic_data['email'])
    existing_mechanic = db.session.execute(query).scalars().first()
    if existing_mechanic:
        return {"message": "Mechanic with this email already exists."}, 400

    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201
@app.route('/mechanics/<int:mechanic_id>', methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return {"message": "Mechanic not found."}, 404
    return mechanic_schema.jsonify(mechanic)
@app.route('/mechanics/<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return {"message": "Mechanic not found."}, 404
    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    if 'email' in mechanic_data:
        query = select(Mechanic).where(Mechanic.email == mechanic_data['email'], Mechanic.id != mechanic_id)
        existing_mechanic = db.session.execute(query).scalars().first()
        if existing_mechanic:
            return {"message": "Mechanic with this email already exists."}, 400

    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic)
@app.route('/mechanics/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return {"message": "Mechanic not found."}, 404
    db.session.delete(mechanic)
    db.session.commit()
    return {"message": "Mechanic deleted."}, 200


with app.app_context():
     db.create_all()
if __name__ == "__main__":
    app.run(debug=True)

