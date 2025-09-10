from flask import Blueprint, request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from app import db, limiter, cache
from app.models import Customer
from app.schemas import CustomerSchema, LoginSchema
from app.utils.util import encode_token
from werkzeug.security import check_password_hash
from limits import Limiter
from limits.util import get_remote_address

limiter = Limiter(get_remote_address, default_limits=["100 per hour"])

customers_bp = Blueprint('customers', __name__)
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()

@customers_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = login_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    customer = db.session.query(Customer).filter_by(email=data['email']).first()
    if not customer or not check_password_hash(customer.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    token = encode_token(customer.id)
    return jsonify({'token': token})

@customers_bp.route('/', methods=['GET'])
@limiter.limit("10 per minute")
@cache.cached(timeout=60)
def get_customers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    customers = db.session.query(Customer).paginate(page=page, per_page=per_page, error_out=False)
    return customers_schema.jsonify(customers.items)

@customers_bp.route('/', methods=['POST'])
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

@customers_bp.route('/<int:customer_id>', methods=['GET'])
@limiter.limit("53 per hour")
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return {"message": "Customer not found"}, 404
    return customer_schema.jsonify(customer)

@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return {"message": "Customer not found"}, 404
    try:
        customer_data = customer_schema.load(request.json, partial=True)
    except ValidationError as err:
        return {"errors": err.messages}, 400
    for key, value in customer_data.items():
        setattr(customer, key, value)
    db.session.commit()
    return customer_schema.jsonify(customer)

@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return {"message": "Customer not found"}, 404
    db.session.delete(customer)
    db.session.commit()
    return {"message": "Customer deleted"}