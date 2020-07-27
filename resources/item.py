import sqlite3
from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price', type=float,
        required=True, 
        help="price is required."
        )
    parser.add_argument(
        'store_id', type=int,
        required=True, 
        help="every item requires a store id."
        )

    # @jwt_required()
    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        
        return {'message': 'Item with name {0} does not exist.'.format(name)}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': 'Item with name {0} does already exists.'.format(name)}, 400

        request_data = Item.parser.parse_args()
        # request_data = request.get_json()
        # price = request_data['price']
        # store_id = request_data['store_id']
        # item = ItemModel(name, price, store_id)
        item = ItemModel(name, **request_data)
        try:
            # item.insert()
            item.save()
        except:
            return {'message': 'something went wrong.'}, 500
        return item.json(), 201

    def put(self, name):
        request_data = Item.parser.parse_args()
        # request_data = request.get_json()
        price = request_data['price']
        # store_id = request_data['store_id']
        item = ItemModel.find_by_name(name)

        if item:
            item.price = price
        else:
            # item = ItemModel(name, price, store_id)
            item = ItemModel(name, **request_data)

        try:
            item.save()
            return item.json()
        except:
            return {'message': 'something went wrong.'}, 500



        # updated_item = ItemModel(name, price)
        # item = ItemModel.find_by_name(name)
        # if item:
        #     try:
        #         updated_item.update()
        #     except:
        #         return {'message': 'something went wrong.'}, 500
        # else:
        #     try:
        #         updated_item.insert()
        #     except:
        #         return {'message': 'something went wrong.'}, 500
        # return updated_item.json()

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        item = ItemModel.find_by_name(name)
        if item is None:
            return {'message': "Item with name {0} not found".format(name)}, 404

        try:
            item.delete()
            return {'message': "Item with name {0} deleted".format(name)}
        except:
            return {"message": "Unable to delete item with name {0}".format(name)}, 500

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # sql = "DELETE FROM items WHERE name =?"
        # cursor.execute(sql, (name,))
        # connection.commit()
        # connection.close()
        # return {'message': "Item with name {0} deleted".format(name)}


class ItemList(Resource):
    # @jwt_required()
    @jwt_required
    def get(self):
        # return {'Items': [item.json() for item in ItemModel.query.all()]}
        return {'Items': [item.json() for item in ItemModel.find_all()]}
        # return {'Items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # sql = "SELECT * FROM items"
        # result = cursor.execute(sql)
        # items = []
        # for item in result:
        #     items.append({'name': item[0], 'price': item[1]})
        # connection.close()
        # return {'Items': items}

