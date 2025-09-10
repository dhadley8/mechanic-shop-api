from flask import Flask
from .extensions import ma, limiter
from .models import db

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    #initialize extensions
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)

   
    #register blueprints
    return app