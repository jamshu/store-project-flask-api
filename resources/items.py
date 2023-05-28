from flask import request
from db import items
import uuid
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", "items", description="Operates on items in database")


@blp.route('/items/<string:item_id>')
class Items(MethodView):

    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, "item Not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        # item_data = request.get_json()
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, "Item not Found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {}
        except KeyError:
            abort(404, "Item Not Found")


@blp.route("/items/")
class ItemsList(MethodView):
    
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)
    def post(self, data):
        # data = request.get_json()
        item_id = uuid.uuid4().hex
        new_item = {**data, "id": item_id}
        items[item_id] = new_item
        return new_item, 201
