from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
ma = Marshmallow()
limiter = Limiter(get_remote_address, default_limits=["100 per hour"])
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Mechanic Shop API"}
)

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    # Register blueprints for your API
    from application.blueprints.customers import customers_bp
    from application.blueprints.tickets import tickets_bp
    from application.blueprints.service_mechanics import service_mechanics_bp
    from application.blueprints.mechanics import mechanics_bp
    from application.blueprints.inventory import inventory_bp

    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(tickets_bp, url_prefix='/tickets')
    app.register_blueprint(service_mechanics_bp, url_prefix='/service_mechanics')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    with app.app_context():
        db.create_all()

    return app

# Blueprints are now defined in their respective files under application/blueprints/

from flask import Blueprint

inventory_bp = Blueprint('inventory', __name__)

# Define your inventory routes here
@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    return