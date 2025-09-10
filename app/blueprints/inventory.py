from flask import Blueprint, request, jsonify
from app import db
from app.models import Inventory
from app.schemas import InventorySchema

inventory_bp = Blueprint('inventory', __name__)
inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)

@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    parts = db.session.query(Inventory).all()
    return inventories_schema.jsonify(parts)

@inventory_bp.route('/', methods=['POST'])
def add_inventory():
    data = request.get_json()
    part = inventory_schema.load(data)
    db.session.add(part)
    db.session.commit()
    return inventory_schema.jsonify(part), 201

@inventory_bp.route('/<int:part_id>', methods=['PUT'])
def update_inventory(part_id):
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({'message': 'Part not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(part, key, value)
    db.session.commit()
    return inventory_schema.jsonify(part)

@inventory_bp.route('/<int:part_id>', methods=['DELETE'])
def delete_inventory(part_id):
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({'message': 'Part not found'}), 404
    db.session.delete(part)
    db.session.commit()
    return jsonify({'message': 'Part deleted'})

from app import app
app.register_blueprint(inventory_bp, url_prefix='/inventory')