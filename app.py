from flask import Flask
from flask_restful import Api
# from flask_jwt import JWT
# from security import authenticate, identity
from  flask_jwt_extended import JWTManager
# from user import UserRegister
# from item import Item, ItemList
from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'dharmadas'
# app.config['JWT_SECRET_KEY'] = 'mohite'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

# jwt = JWT(app, authenticate, identity)  # /auth endpoint is created automatically
jwt = JWTManager(app)  # /auth endpoint is not created

@jwt.user_claims_loader
def add_claims_to_jwt(identity):  # Remember identity is what we define when creating the access token
    if identity == 1:   # instead of hard-coding, we should read from a config file or database to get a list of admins instead
        return {'is_admin': True}
    return {'is_admin': False}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)