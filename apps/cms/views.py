# 定义视图

from flask import Blueprint

bp = Blueprint("cms",__name__,url_prefix='/cms')


@bp.route('/')
def index():
    # g.cms_user
    return "cms index"