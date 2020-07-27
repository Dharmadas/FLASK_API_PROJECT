from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,required=True, help="price is required.")

    # @jwt_required()
    @jwt_required
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {"message": "Store with name {0} not found".format(name)}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return {"message": "store with name {0} already exists".format(name)}

        store = StoreModel(name)
        try:
            store.save()
        except:
            return {"message": "something went wrong."}, 500
        return store.json(), 201

    # def put(self, name):
    #     store = StoreModel.find_by_name(name)

    #     if store:
    #         store.name = name
    #     else:
    #         store = StoreModel(name)

    #     store.save()
    #     return store.json()

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        store = StoreModel.find_by_name(name)
        if store:
            store.delete()
            return {"message": "store with name {0} deleted".format(name)}

class StoreList(Resource):
    # @jwt_required()
    @jwt_required
    def get(self):
        # return {'Stores': [store.json() for store in StoreModel.query.all()]}
        return {'Stores': [store.json() for store in StoreModel.find_all()]}
