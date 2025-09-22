from flask import Blueprint, request, jsonify
from application import db, limiter, cache
from application.models import Customer
from application.schemas import CustomerSchema

customers_bp = Blueprint('customers', __name__)
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

@customers_bp.route('/', methods=['GET'])
@limiter.limit("10 per minute")
@cache.cached(timeout=60)
def get_customers():
    customers = Customer.query.all()
    return customers_schema.jsonify(customers)

@customers_bp.route('/', methods=['POST'])
def add_customer():
    data = request.get_json()
    customer = customer_schema.load(data)
    db.session.add(customer)
    db.session.commit()
    return customer_schema.jsonify(customer), 201