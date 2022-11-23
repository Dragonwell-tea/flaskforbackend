import flask
import schema
from flask import Blueprint
from exts import db
from models import UserModel,CategoryModel,ProductModel,OrderModel
bp = Blueprint("item", __name__, url_prefix="/")

#http://127.0.0.1:5000
@bp.route("/category", methods=["GET"])
def get_categories_route():
    categories = db.session.query(CategoryModel)
    response = [{**m.to_dict()} for m in categories]
    return flask.jsonify(response)

@bp.route("/product", methods=["GET"])
def get_products_route():
    products = db.session.query(ProductModel)
    response = [{**m.to_dict()} for m in products]
    return flask.jsonify(response)
#
# @bp.route("/product/<product_id>", methods=["GET"])
# def get_product_route(product_id):
#     product = db.session.get(ProductModel, product_id)
#     if not product:
#         return {"status": "Not Found"}, 404
#     return flask.jsonify(product.to_dict())
#
# CREATE_PRODUCT_SCHEMA = schema.Schema(
#     {
#         "product_name": schema.And(str, len),
#         "picture": schema.And(str, len),
#         "selling_price": schema.And(schema.Use(float), lambda i: i >= 0),
#         "description": schema.And(str, len),
#         "category_id": schema.And(schema.Use(int), lambda i: i >= 0),
#     }
# )
#
# @bp.route("/product", methods=["POST"])
#
# def create_product_route():
#     try:
#         request = CREATE_PRODUCT_SCHEMA.validate(flask.request.json.copy())
#     except schema.SchemaError as error:
#         return {"status": "Bad request", "message": str(error)}, 400
#
#     product = ProductModel()
#     product.product_name = request["product_name"]
#     product.picture = request["picture"]
#     product.selling_price = request["selling_price"]
#     product.description = request["description"]
#     product.available = 0
#     product.category_id = request["category_id"]
#     product.user_id = flask.g.token["user_id"]
#     db.session.add(product)
#     db.session.commit()
#
#     return flask.jsonify({"message": "success"})
#
#
# UPDATE_PRODUCT_SCHEMA = schema.Schema(
#     {
#         "product_id": schema.And(schema.Use(int), lambda i: i >= 0),
#         "product_name": schema.And(str, len),
#         "picture": schema.And(str, len),
#         "selling_price": schema.And(schema.Use(float), lambda i: i >= 0),
#         "description": schema.And(str, len),
#         "category_id": schema.And(schema.Use(int), lambda i: i >= 0),
#     }
# )
#
#
# @bp.route("/product", methods=["PUT"])
#
# def update_product_route():
#     try:
#         request = UPDATE_PRODUCT_SCHEMA.validate(flask.request.json.copy())
#     except schema.SchemaError as error:
#         return {"status": "Bad request", "message": str(error)}, 400
#
#     current_user_id = flask.g.token["user_id"]
#     product = db.session.get(ProductModel, request["product_id"])
#     if not product:
#         return {"status": "Not Found"}, 404
#     if product.user_id != current_user_id:
#         return {"status": "Permission denied"}, 401
#
#     for k in request:
#         if k == "product_name":
#             product.product_name = request["product_name"]
#         elif k == "picture":
#             product.picture = request["picture"]
#         elif k == "selling_price":
#             product.selling_price = request["selling_price"]
#         elif k == "description":
#             product.description = request["description"]
#         elif k == "category_id":
#             product.category_id = request["category_id"]
#
#     db.session.merge(product)
#     db.session.commit()
#
#     return flask.jsonify({"message": "success"})
#
#
# @bp.route("/product/<product_id>", methods=["DELETE"])
#
# def delete_product_route(product_id):
#     product = db.session.get(ProductModel, product_id)
#     if not product:
#         return {"status": "Not Found"}, 404
#
#     current_user_id = flask.g.token["user_id"]
#     if product.user_id != current_user_id:
#         return {"status": "Permission denied"}, 401
#
#     db.session.delete(product)
#     db.session.commit()
#     return flask.jsonify({"message": "success"})