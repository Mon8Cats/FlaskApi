import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        type=str,
        required=True,
        help="this filed cannot be blank!"
    )
    parser.add_argument('password', 
        type=str,
        required=True,
        help="this filed cannot be blank!"
    )
    
    def post(self):
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists."}, 400
        
        #user = UserModel(data['username'], data['password'])
        user = UserModel(**data)
        user.save_to_db()
        
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))
        
        connection.commit()
        connection.close()
        
        return {"message": "User created successfully."}, 201
        '''

    @jwt_required()
    def get(self):
        user = current_identity
