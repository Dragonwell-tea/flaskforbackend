from sqlalchemy import Integer,String

from exts import db
from enum import Enum

class UserRole(Enum):
    user = 0
    admin = 1

class ProductAvailable(Enum):
    unsold: 0
    sold: 1


class OrderStatus(Enum):
    waitCheck: 0
    checked: 1
    finish: 2

class UserModel(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.VARCHAR(100), primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.VARCHAR(100), nullable=False)
    role = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True)
    profile_picture = db.Column(db.TEXT)
    hash = db.Column(db.String(100))

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "phone": self.phone,
            "role": self.role,
            "email": self.email,
            "profile_picture": self.profile_picture,
        }

class CategoryModel(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.BIGINT, primary_key=True)
    category_name = db.Column(db.TEXT)

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "category_name": self.category_name,
        }


class ProductModel(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.BIGINT, primary_key=True)
    product_name = db.Column(db.TEXT)
    picture = db.Column(db.TEXT)
    selling_price = db.Column(db.FLOAT)
    description = db.Column(db.TEXT)
    available = db.Column(db.INTEGER)
    user_id = db.Column(db.ForeignKey(UserModel.user_id))
    category_id = db.Column(db.ForeignKey(CategoryModel.category_id))
    category = db.relationship("CategoryModel")

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "picture": self.picture,
            "selling_price": self.selling_price,
            "description": self.description,
            "available": self.available,
            "user_id": self.user_id,
            "category": self.category.category_name,
        }


class OrderModel(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.BIGINT, primary_key=True)
    status = db.Column(db.INTEGER)
    create_date = db.Column(db.TIMESTAMP)
    user_id = db.Column(db.ForeignKey(UserModel.user_id))
    product_id = db.Column(db.ForeignKey(ProductModel.product_id))
    product = db.relationship("ProductModel")

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "status": self.status,
            "create_date": self.create_date,
            "user_id": self.user_id,
            "product_id": self.product_id,
        }