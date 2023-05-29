from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schemas import StoreSchema, PlainStoreSchema
from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

blp = Blueprint("Stores", "stores", description="Operates on stores in database")


@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, PlainStoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def put(self, store_id):
        data = request.get_json()
        try:
            store = stores[store_id]
            store |= data
            return store
        except KeyError:
            abort(404, "Store not Found")

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted successfully"}


@blp.route("/store/")
class StoreList(MethodView):
    @jwt_required()
    @blp.response(200, PlainStoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError as error:
            abort(500, message="Error while creating Store {}".format(error))
       
        return store
