# 定义视图

from flask import Blueprint

bp = Blueprint("common", __name__, url_prefix='/common')


@bp.route('/')
def index():
    # g.cms_user
    return "common index"
