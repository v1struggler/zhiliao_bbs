# 定义视图

from flask import Blueprint, make_response, request
from utils import restful, zlcache, demo
from utils.captcha import Captcha
from io import BytesIO
from .forms import SMSCaptchaForm
from exts import alidayu

bp = Blueprint("common", __name__, url_prefix='/common')


@bp.route('/')
def index():
    return "common index"


# 图片验证码
@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()  # 获取验证码
    zlcache.set(text.lower(), text.lower())         # 将验证码作为key将验证码存储到缓存，储存成小写形式
    out = BytesIO()  # 创建字节流
    image.save(out, 'png')  # 将图片存储到字节流当中，格式为png
    out.seek(0)  # 将文件流的指针放在0的位置
    resp = make_response(out.read())  # 创建response对象
    resp.content_type = 'image/png'
    return resp


# 旧版本：使用get的方式发送短信验证码
# @bp.route('/sms_captcha/')
# def sms_captcha():
#     # ?telephone=xxx
#     # /c/sms_captcha/xxx
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.params_error(message='请传入手机号码！')
#
#     captcha = Captcha.gene_text(number=4)  # 随机生成一个4位数的验证码
#
#     if demo.alidayu(telephone, captcha):
#         return restful.success()
#     else:
#         #return restful.params_error(message='短信验证码发送失败！')
#         return restful.success()


# 使用post加盐的方式发送短信验证码
@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = Captcha.gene_text(number=4)
        print('发送的短信验证码是：', captcha)
        if demo.alidayu(telephone, captcha):
            zlcache.set(telephone, captcha)      # 将手机号作为key，将验证码保存到缓存中
            return restful.success()
        else:
            #return restful.params_error(message='短信验证码发送失败！')
            zlcache.set(telephone, captcha)      # 开发测试：即使由于限制验证码发送失败也可以保存验证码到缓存
            return restful.success()
    else:
        return restful.params_error(message='参数错误！')
