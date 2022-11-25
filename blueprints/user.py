from flask import Blueprint
from flask import request
import re
import schema
import flask
import uuid

from exts import db
from models import UserModel,CategoryModel,ProductModel,OrderModel

#/user/login
bp = Blueprint("user", __name__, url_prefix="/")

EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"



def is_email(email_address):
    return re.fullmatch(EMAIL_REGEX, email_address)

REGISTER_SCHEMA = schema.Schema(
    {
        "user_name": schema.And(str, len),
        "password": schema.And(str, len),
        "phone": schema.And(str, len),
        "email": schema.And(str, len, is_email),
    }
)

# GET:从服务器上获取数据
# POST：将客户端的数据提交给服务器
@bp.route("/register", methods=['POST'])
def register():
    if not isinstance(flask.request.json, dict):
        return {"status": "Bad request"}, 400
    try:
        request = REGISTER_SCHEMA.validate(flask.request.json.copy())
    except schema.SchemaError as error:
        return {"status": "Bad request", "message": str(error)}, 400
    #拿到app提交的注册参数
    email = request["email"]
    user_name = request["user_name"]
    password = request["password"]
    phone = request["phone"]

    result = {}

    if db.session.query(UserModel).filter(UserModel.email == email).first():
        return {"status": "Email is already exsit"}, 409

    user = UserModel()
    user.user_id = str(uuid.uuid4())
    user.email = email
    user.phone = phone
    user.role = 0
    user.user_name = user_name
    user.hash = str(password)
    db.session.merge(user)
    db.session.commit()

    user = db.session.get(UserModel, user.user_id)

    result = {
            'status': 1,
            'errorMsg' :'register success',
            'data' : user.to_dict()
        }

    return flask.jsonify(result)


LOGIN_SCHEMA = schema.Schema(
    {"email": schema.And(str, len), "password": schema.And(str, len)}
)

@bp.route("/login", methods=['POST'])
def login():
    if not isinstance(flask.request.json, dict):
        return {"status": "Bad request"}, 400
    try:
        request = LOGIN_SCHEMA.validate(flask.request.json.copy())
    except schema.SchemaError as error:
        return {"status": "Bad request", "message": str(error)}, 400

    email = request["email"]
    password = request["password"]
    result = {}

    # 存储查询结果
    user = db.session.query(UserModel).filter(UserModel.email == email).first()
    if user is None:
        result = {
            'status': 0,
            'Msg': 'cannot find account',
        }
        # return flask.jsonify(result)
    # if not (password == user.hash):
    elif password != user.hash:
        result = {
            'status': 0,
            'Msg': 'password is wrong',
        }
        # return flask.jsonify(result)
    else:
        result = {
            'status': 1,
            'Msg': 'login success',
            'data': user.to_dict()
        }
    return flask.jsonify(result)

UPDATE_USER_SCHEMA = schema.Schema(
    {
        "user_id": schema.And(str, len),
        "user_name": schema.And(str, len),
        "phone": schema.And(str, len),
        "email": schema.And(str, len, is_email),
        "profile_picture": schema.And(str, len),

    }
)

@bp.route("/updateProfile", methods=['PUT'])
def updateProfile():
    if not isinstance(flask.request.json, dict):
        return {"status": "Bad request"}, 400
    try:
        request = UPDATE_USER_SCHEMA.validate(flask.request.json.copy())
    except schema.SchemaError as error:
        return {"status": "Bad request", "message": str(error)}, 400


    current_user_id = request["user_id"]
    current_user = db.session.get(UserModel, current_user_id)
    current_user.user_name = request["user_name"]
    current_user.phone = request["phone"]
    current_user.email = request["email"]
    current_user.profile_picture = request["profile_picture"]

    db.session.merge(current_user)
    db.session.commit()
    result = {
        'status': 1,
        'Msg': 'successsful update',
        'data': current_user.to_dict()
    }
    # return flask.jsonify({"message": "success"})
    return  flask.jsonify(result)
