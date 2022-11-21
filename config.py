from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker

SQLALCHEMY_TRACK_MODIFICATIONS = False

#数据库的配置信息
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'umdmarket'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# engine = create_engine(SQLALCHEMY_DATABASE_URI, echo = True)
#
# DBSession = sessionmaker(autocommit = False,bind=engine)
