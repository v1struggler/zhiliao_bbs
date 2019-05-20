# 在主配置文件中我们不任何视图，将所有的视图都分类到app当中

from flask import Flask
# from apps.cms.views import bp as cms_bp
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp
import config

app = Flask(__name__)
app.config.from_object(config)

app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(common_bp)

if __name__ == '__main__':
    app.run()
