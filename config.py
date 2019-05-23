# 配置文件
import os


DEBUG = True

# 数据库配置信息
DB_USERNAME = 'root'
DB_PASSWORD = '123456'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'zlbbs'

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 与跟踪相关，True：一旦模型被改变都会给你发送信号；

# 使用session就需要设置SECRET_KEY
SECRET_KEY = os.urandom(24)


CMS_USER_ID = 'ASDFASDFSA'