import flask
import schema

from datetime import datetime

from flask import Blueprint
from exts import db
from models import UserModel,CategoryModel,ProductModel,OrderModel,ProductStatus, UserRole
bp = Blueprint("item", __name__, url_prefix="/")

#http://127.0.0.1:5000
@bp.route("/category", methods=["GET"])
def get_categories_route():
    categories = db.session.query(CategoryModel)
    response = [{**m.to_dict()} for m in categories]
    return flask.jsonify(response)


# GET_CATEGORY_SCHEMA = schema.Schema(
#     {
#         "category_id": schema.And(schema.Use(int)),
#     }
# )
# #获取指定接口的商品
# @bp.route("/categorydetail", methods=["GET"])
# def get_catedetail_route():
#     if not isinstance(flask.request.json, dict):
#         return {"status": "Bad request"}, 400
#     try:
#         request = GET_CATEGORY_SCHEMA.validate(flask.request.json.copy())
#     except schema.SchemaError as error:
#         return {"status": "Bad request", "message": str(error)}, 400
#     current_category_id = request["category_id"]
#
#
#     product = db.session.query(ProductModel).filter(ProductModel.category_id == current_category_id).all()
#     if product is None:
#         result = {
#             "nothing found in this cate"
#         }
#     result = [{**m.to_dict()} for m in product]
#     return flask.jsonify(result)

#获取指定接口的商品
@bp.route("/categorydetail/<category_id>", methods=["GET"])
def get_catedetail_route(category_id):
    product = db.session.query(ProductModel).filter(ProductModel.category_id == category_id).all()
    if product is None:
        result = {
            "nothing found in this cate"
        }
    result = [{**m.to_dict()} for m in product]
    return flask.jsonify(result)



READ_PRODUCT_SCHEMA = schema.Schema(
    {
        schema.Optional("category_id"): schema.And(str, schema.Use(str.split)),
    }
)

@bp.route("/product", methods=["GET"])
def get_products_route():
    try:
        request = READ_PRODUCT_SCHEMA.validate(flask.request.args.copy())
    except:
        return {"status": "Bad request"}, 400

    category_id = request["category_id"] if "category_id" in request else None
    if category_id:
        products = db.session.query(ProductModel).filter(
            ProductModel.status == ProductStatus.posted.value,
        )
    products = db.session.query(ProductModel).filter(ProductModel.status == ProductStatus.posted.value)
    response = [{**m.to_dict()} for m in products]
    return flask.jsonify(response)

#点击量按降序排列传回给web
##############商品的status必须是1且点击次数不能是0
@bp.route("/productHot", methods=["GET"])
def get_products_hot__route():
    products = db.session.query(ProductModel).filter(
        ProductModel.status == ProductStatus.posted.value, ProductModel.views > 0
    ).order_by(ProductModel.views.desc())
    response = [{**m.to_dict()} for m in products]
    return flask.jsonify(response)

#view增加，商品详情页
#例如http://127.0.0.1:5000/product/5 就是product_id
#为5的产品，浏览次数+1
@bp.route("/product/<product_id>", methods=["GET"])
def get_product_route(product_id):
    product = db.session.get(ProductModel, product_id)
    if not product:
        return {"status": "Not Found"}, 404
    product.views = product.views + 1
    db.session.merge(product)
    db.session.commit()
    return flask.jsonify(product.to_dict())



CREATE_PRODUCT_SCHEMA = schema.Schema(
    {
        "user_id": schema.And(str, len),
        "name": schema.And(str, len),
        "picture": schema.And(str, len),
        "sold_price": schema.And(schema.Use(float), lambda i: i >= 0),
        "description": schema.And(str, len),
        "category_id": schema.And(schema.Use(int), lambda i: i >= 0),
    }
)

#添加商品
@bp.route("/addProduct", methods=["POST"])
def create_product_route():
    try:
        request = CREATE_PRODUCT_SCHEMA.validate(flask.request.json.copy())
    except schema.SchemaError as error:
        return {"status": "Bad request", "message": str(error)}, 400

    product = ProductModel()
    product.product_name = request["name"]
    product.picture = request["picture"]
    product.selling_price = request["sold_price"]
    product.description = request["description"]
    product.status = ProductStatus.pending.value
    product.views = 0
    product.category_id = request["category_id"]
    product.user_id = request["user_id"]
    db.session.add(product)
    db.session.commit()

    return flask.jsonify({"message": "The product has been successfully released,we will review it as soon"})


CHECK_PRODUCT_SCHEMA = schema.Schema(
    {
        "product_id": schema.And(schema.Use(int), lambda i: i >= 0),
        "status": schema.And(schema.Use(int)),
        "role": schema.And(schema.Use(int)),
    }
)
#传入要审核的商品的id, status传1就代表审核通过
# role如果不是1，会返回权限不够
@bp.route("/check", methods=["POST"])
def check_product_route():
    try:
        request = CHECK_PRODUCT_SCHEMA.validate(flask.request.json.copy())
    except schema.SchemaError as error:
        return {"status": "Bad request", "message": str(error)}, 400

    current_user_role = request["role"]
    # current_user = db.session.get(UserModel, current_user_role)
    if current_user_role != UserRole.admin.value:
        return {"status": "Insufficient authority"}, 401

    product = db.session.get(ProductModel, request["product_id"])
    product.status = request["status"]
    db.session.merge(product)
    db.session.commit()
    return flask.jsonify({"message": "The review is successful"})

PRODUCT_PENDING_SCHEMA = schema.Schema(
    {
        # "user_id": schema.And(schema.Use(int)),
        "user_id": schema.And(str, len),
    }
)


#待审核商品列表
@bp.route("/productPending", methods=["GET"])
def get_products_pending_rout():
    request = PRODUCT_PENDING_SCHEMA.validate(flask.request.json.copy())
    current_user_id = request["user_id"]
    current_user = db.session.get(UserModel, current_user_id)
    if current_user.role != UserRole.admin.value:
        return {"status": "Permission denied"}, 401
    products = db.session.query(ProductModel).filter(
        ProductModel.status == ProductStatus.pending.value)
    response = [{**m.to_dict()} for m in products]
    return flask.jsonify(response)

CREATE_ORDER_SCHEMA = schema.Schema(
    {
        "product_id": schema.And(schema.Use(int), lambda i: i >= 0),
        "user_id": schema.And(str, len),
    }
)

#用户下单
@bp.route("/order",methods=["POST"])
def creat_order_route():
    try:
        request = CREATE_ORDER_SCHEMA.validate(flask.request.json.copy())
    except schema.SchemaError as error:
        return {"status": "Bad request", "message": str(error)}, 400
    current_user_id = request["user_id"]
    current_product_id = request["product_id"]
    product = db.session.get(ProductModel, current_product_id)
    product.status = 2 #下单物品状态变为2,
    db.session.merge(product)
    db.session.commit()

    order = OrderModel()
    # order.create_date = datetime.now()
    d1 = datetime.now()
    order.create_date = d1.strftime("%Y-%m-%d %H:%M:%S")
    order.product_id = current_product_id
    order.user_id = current_user_id
    db.session.add(order)
    db.session.commit()
    return flask.jsonify({"message": "success"})


ORDER_HISTORY_SCHEMA = schema.Schema(
    {
        "user_id": schema.And(str, len),
    }
)

#订单历史
@bp.route("/currentUserOrder", methods=["GET"])

def current_user_order_route():
    try:
        request = ORDER_HISTORY_SCHEMA.validate(flask.request.json.copy())
    except schema.SchemaError as error:
        return {"status": "Bad request", "message": str(error)}, 400
    current_user_id = request["user_id"]
    orders = db.session.query(OrderModel).filter(OrderModel.user_id == current_user_id)
    return flask.jsonify([{**m.to_dict()} for m in orders])
