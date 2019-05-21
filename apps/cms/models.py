# 定义模型

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# 定义后台用户模型
class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    # 密码：对外的字段名叫做password，对内的字段名叫做_password
    # 如果不加_，那么就命名冲突
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    # 重写构造函数，如果不重写：模型在实例化的时候指定字段为 _password，而此时 _password为受保护的
    # 外面在实例化的时候，还是使用的password，底层加密的东西都不用管
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property    # 将类中的方法定义成属性
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result
