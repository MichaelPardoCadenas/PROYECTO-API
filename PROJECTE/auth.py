from functools import wraps
from flask import request, jsonify

VALID_APIKEY = "mysecretapikey"

def require_apikey(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        apikey = request.args.get('apikey')
        if not apikey or apikey != VALID_APIKEY:
            return jsonify({'message': 'API key no válida o no proporcionada'}), 403
        return f(*args, **kwargs)
    return decorated
