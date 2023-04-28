import uuid # for public id
from flask import Flask, request, jsonify, make_response
import jwt
from functools import wraps
from .models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, options={"verify_signature": False})
            current_user = User.query.filter_by(api_key=data['api_key']).first()
        except:
            return jsonify({
                'message': 'Token is invalid!'
            }), 401
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated
