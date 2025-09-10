from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select
from datetime import datetime
from typing import List

from marshmallow import ValidationError
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)  



class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(360), nullable=False, unique=True)
    phone = db.Column(db.String(100), nullable=False)

class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'
    id = db.Column(db.Integer, primary_key=True)
    vin = db.Column(db.String(17), nullable=False)
    service_date = db.Column(db.String(100), nullable=False)
    service_description = db.Column(db.String(500), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

class ServiceMechanic(db.Model):
    __tablename__ = 'service_mechanics'
    ticket_id = db.Column(db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True)
    mechanic_name = db.Column(db.String(100), nullable=False)

class Mechanic(db.Model):
    __tablename__ = 'mechanics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(360), nullable=False, unique=True)

ticket_inventory = db.Table(
    'ticket_inventory',
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('inventory_id', db.Integer, db.ForeignKey('inventory.id'), primary_key=True)
)

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    tickets = db.relationship('ServiceTicket', secondary=ticket_inventory, backref='parts')

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        include_relationships = True
        load_instance = True