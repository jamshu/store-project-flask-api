from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError
blp = Blueprint("Items", "items", description="Operates on items in database")


@blp.route('/items/<string:item_id>')
class Items(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data.get('price', item.price)
            item.name = item_data.get('name', item.name)

        else:
            item = ItemModel(id=item_id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item

    def delete(self, item_id):
        item = ItemModel.query.get(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted successfully"}


@blp.route("/items/")
class ItemsList(MethodView):
    
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, data):
        item = ItemModel(**data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, "Error {} occured while inserting an item".format(e))
        
        return item
