from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

db = SQLAlchemy()
ma = Marshmallow()
limiter = Limiter(get_remote_address, default_limits=["100 per hour"])
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Dodobird8!@localhost/mechanic_db'
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    from .blueprints.customers import customers_bp
    from .blueprints.tickets import tickets_bp
    from .blueprints.service_mechanics import service_mechanics_bp
    from .blueprints.mechanics import mechanics_bp

    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(tickets_bp, url_prefix='/tickets')
    app.register_blueprint(service_mechanics_bp, url_prefix='/service_mechanics')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')

    with app.app_context():
        db.create_all()

    return app