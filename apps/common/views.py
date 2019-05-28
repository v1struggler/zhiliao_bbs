# 定义视图

from flask import Blueprint, make_response
from utils.captcha import Captcha
from io import BytesIO
from utils import zlcache

bp = Blueprint("common", __name__, url_prefix='/common')


@bp.route('/')
def index():
    return "common index"


@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()      # 获取验证码
    zlcache.set(text.lower(), text.lower())
    out = BytesIO()                                 # 创建字节流
    image.save(out, 'png')                          # 将图片存储到字节流当中，格式为png
    out.seek(0)                                     # 将文件流的指针放在0的位置
    resp = make_response(out.read())                # 创建response对象
    resp.content_type = 'image/png'
    return resp
