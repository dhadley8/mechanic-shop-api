import os
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify, current_app

SECRET_KEY = os.environ.get("SECRET_KEY") or 'your_secret_key'

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(tz=timezone.utc) + timedelta(hours=1),
        'iat': datetime.now(tz=timezone.utc),
        'sub': customer_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split(" ")
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            customer_id = data['sub']
        except ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except JWTError:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(customer_id, *args, **kwargs)
    return decorated