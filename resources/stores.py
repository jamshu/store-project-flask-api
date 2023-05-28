from flask import request
from db import stores
import uuid
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schemas import StoreSchema

blp = Blueprint("Stores", "stores", description="Operates on stores in database")


@blp.route('/store/<string:store_id>')
class Store(MethodView):

    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, "Store Not found")

    def put(self, store_id):
        data = request.get_json()
        try:
            store = stores[store_id]
            store |= data
            return store
        except KeyError:
            abort(404, "Store not Found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {}
        except KeyError:
            abort(404, "Store Not Found")


@blp.route("/store/")
class StoreList(MethodView):
    
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        print(stores.values())
        return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        print("store data",store_data)
        # store_data = request.get_json()
        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        return new_store, 201
