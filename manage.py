# 数据库迁移脚本

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from zhiliao_bbs import create_app
from exts import db
from apps.cms import models as cms_models   # 只要导入模块就能映射模块里面的所有模型

app = create_app()
manager = Manager(app)  # 创建manager需要绑定app
Migrate(app, db)  # 将app、db与Migrate绑定
manager.add_command('db', MigrateCommand)  # 将MigrateCommand中的命令添加到manager对象中

CMSUser = cms_models.CMSUser

# 通过flask_script中的manager，利用运行脚本的形式来创建用户
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功！')


if __name__ == '__main__':
    # python manage.py db init   初始化
    # python manage.py db migrate    创建迁移脚本
    # python manage.py db upgrade    映射到数据库中
    # python manage.py create_cms_user -u zhiliao -p 123456 -e 714464655@qq.com    映射到数据库中
    manager.run()