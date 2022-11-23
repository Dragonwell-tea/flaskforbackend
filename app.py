from flask import Flask, render_template
import config
from exts import db
from blueprints.user import bp as user_bp
from blueprints.item import bp as item_bp
from models import UserModel, CategoryModel, ProductModel, OrderModel
from flask_migrate import Migrate
#11.24新加入
from flask_cors import CORS


app = Flask(__name__)
#绑定配置文件
app.config.from_object(config)

#11.24新加入
CORS(app)


#ORM模型映射成表的三步
#1.flask db init：这步只需要执行一次，执行完后会自动添加一个迁移脚本
#2.flask db migrate: 识别ORM模型的改变，生成迁移脚本，在version文件夹下能看见
#3.flask db upgrade：运行迁移脚本到数据库中，alembic_version是migrate自己创的，用来记录数据库迁移的版本号
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp)
app.register_blueprint(item_bp)
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host=app.config['HOST_IP'], port=app.config['FLASK_PORT'], debug=app.config['DEBUG'])
