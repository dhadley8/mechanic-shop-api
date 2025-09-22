from application import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(360), nullable=False, unique=True)
    phone = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Mechanic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(360), nullable=False, unique=True)
    phone = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)

class ServiceTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vin = db.Column(db.String(17), nullable=False)
    service_date = db.Column(db.String(100), nullable=False)
    service_description = db.Column(db.String(500), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)