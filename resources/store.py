from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()

    # @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {"message": "Store not found"}, 404


    def post(self, name):

        if StoreModel.find_by_name(name):
            return {"message": "Store with name '{}' already exists".format(name)}, 400

        data = Store.parser.parse_args()
        store = StoreModel(name, **data)

        try:
            store.save_to_db()
        except:
            return {"message": "Something went wrong. Error occurred inserting"}, 500

        return store.json(), 201


    def delete(self, name):
        store = StoreModel.find_by_name(name)
        try:
            if store is None:
                store.delete_from_db()
            else:
                return {"message": "Store not found"}, 400
        except:
            return {"message": "Something went wrong. Error occurred deleting"}, 500
        return {"message": "Store Deleted"}


class StoreList(Resource):

    @jwt_required()
    def get(self):
        return {'stores': StoreModel.get_all()}

