class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///myshop.db'  # Or your MySQL URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'

APPLICATION_STRUCTURE = {
    'blueprints': [
        'customers',
        'tickets',
        'service_mechanics',
        'mechanics',
        'inventory',
        # ... other blueprints ...
    ],
    # ... other application parts ...
}