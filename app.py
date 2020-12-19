from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity as identity_function
from datetime import timedelta
from db import db


from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'steve'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

db.init_app(app)

'''
default values
the authentication endpoint: /auth
the token expiration time: 5 min
the authentication key name: username
the authentication response body: access_token
'''

app.config['JWT_AUTH_URL_RULE'] = '/login' #1
jwt = JWT(app, authenticate, identity_function) # create a new end point
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })

'''
@jwt.error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code
'''    
    
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
   
    app.run(port=5000, debug=True)
