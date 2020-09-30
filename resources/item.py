from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be empty."
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id."
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"{name} already exists."}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error ocurred while inserting item."}, 500

        return item.json(), 201

    def delete(self, name):
        try:
            item = ItemModel.find_by_name(name)
            if item:
                item.delete_from_db()
            else:
                return {"message": f"Item {name} not found"}, 404
        except:
            return {"message": "An error ocurred while deleting the item."}, 500

        return {"message": "Item deleted successfully"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        try:
            if item is None:
                item = ItemModel(name, **data)
            else:
                item.price = data["price"]
                item.store_id = data["store_id"]

            item.save_to_db()
        except:
            return {"message": "An error ocurred while updating the item."}, 500

        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
