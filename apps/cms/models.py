# 定义模型

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# 不能通过用户直接拿到权限，而是：用户—角色—权限
class CMSPersmission(object):
    # 255的二进制方式来表示 0b1111 1111
    ALL_PERMISSION = 0b11111111
    # 1. 访问者权限
    VISITOR = 0b00000001
    # 2. 管理帖子权限
    POSTER = 0b00000010
    # 3. 管理评论的权限
    COMMENTER = 0b00000100
    # 4. 管理板块的权限
    BOARDER = 0b00001000
    # 5. 管理前台用户的权限
    FRONTUSER = 0b00010000
    # 6. 管理后台用户的权限
    CMSUSER = 0b00100000
    # 7. 管理后台管理员的权限
    ADMINER = 0b01000000


# 多对多：定义角色和用户模型
cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True)
)


# 定义角色模型
class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=CMSPersmission.VISITOR)                 # 二进制在数据库中表示其实就是一个数字

    users = db.relationship('CMSUser', secondary=cms_role_user, backref='roles')        #(引用表，中间表，反向引用)


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

    @property  # 将类中的方法定义成属性
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result