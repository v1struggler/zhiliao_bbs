# 数据库迁移脚本

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from zhiliao_bbs import create_app
from exts import db
from apps.cms import models as cms_models  # 只要导入模块就能映射模块里面的所有模型
from apps.front import models as front_models
from apps.models import BannerModel, BoardModel

app = create_app()
manager = Manager(app)              # 创建manager需要绑定app
Migrate(app, db)                    # 将app、db与Migrate绑定
manager.add_command('db', MigrateCommand)           # 将MigrateCommand中的命令添加到manager对象中


CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPersmission
FrontUser = front_models.FrontUser

# 通过flask_script中的manager，利用运行脚本的形式来创建cms用户
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功！')


# 利用脚本(命令)的方式来创建角色：因为角色定义好就不会有太大的改变，所以用这种方式创建
@manager.command
def create_role():
    # 1. 访问者（可以修改个人信息）
    visitor = CMSRole(name='访问者', desc='只能相关数据，不能修改。')
    visitor.permissions = CMSPermission.VISITOR

    # 2. 运营角色（修改个人个人信息，管理帖子，管理评论，管理前台用户）
    operator = CMSRole(name='运营', desc='管理帖子，管理评论,管理前台用户。')    # 使用二进制的或运算将不同的权限组合到一起
    operator.permissions = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.COMMENTER | CMSPermission.FRONTUSER

    # 3. 管理员（拥有绝大部分权限）
    admin = CMSRole(name='管理员', desc='拥有本系统所有权限。')
    admin.permissions = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.CMSUSER | CMSPermission.COMMENTER | CMSPermission.FRONTUSER | CMSPermission.BOARDER

    # 4. 开发者
    developer = CMSRole(name='开发者', desc='开发人员专用角色。')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()


# 添加权限
@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def add_user_to_role(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('用户添加到角色成功！')
        else:
            print('没有这个角色：%s' % role)
    else:
        print('%s邮箱没有这个用户!' % email)

# 测试权限
@manager.command
def test_permission():                                    # 测试权限
    user = CMSUser.query.first()
    if user.is_developer:
        print('这个用户有访问者的权限！')
    else:
        print('这个用户没有访问者权限！')


# 创建front用户
@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
    user = FrontUser(telephone=telephone, username=username, password=password)
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    # python manage.py db init   初始化
    # python manage.py db migrate    创建迁移脚本
    # python manage.py db upgrade    映射到数据库中

    # python manage.py create_cms_user -u zhiliao -p 123456 -e 714464655@qq.com    创建cms用户
    # python manage.py create_role          创建角色
    # python manage.py test_permission   测试权限
    # python manage.py add_user_to_role -e 714464655@qq.com -n 开发者     添加权限

    # python manage.py create_cms_user -u 我是访问者 -p 123456 -e 714464656@qq.com           # 7 运营 8 管理员
    # python manage.py add_user_to_role -e 714464656@qq.com -n 访问者

    # python manage.py create_front_user -t 13309567820 -u zhiliao -p 123456
    manager.run()
