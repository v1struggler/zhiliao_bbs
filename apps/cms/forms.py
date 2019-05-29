# 定义表单

from wtforms import StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo
from ..forms import BaseForm
from utils import zlcache
from wtforms import ValidationError
from flask import g

# 登录验证
class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'), InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])
    remember = IntegerField()


# 修改密码验证
class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='请输入正确格式的旧密码')])
    newpwd = StringField(validators=[Length(6, 20, message='请输入正确格式的新密码')])
    newpwd2 = StringField(validators=[EqualTo("newpwd", message='确认密码必须和新密码保持一致')])

    # def get_error(self):        # 提取到了apps\forms.py中的BaseForm
    #     message = self.errors.popitem()[1][0]
    #     return message


# 修改邮箱验证
class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱！')])
    captcha = StringField(validators=[Length(min=6, max=6, message='请输入正确长度的验证码！')])

    def validate_captcha(self, field):
        captcha = field.data                    # 首先拿到captcha,此时field就代表captcha
        email = self.email.data                 # 拿到邮箱
        captcha_cache = zlcache.get(email)      # 到缓存中拿到邮箱对应的验证码
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误！')

    def validate_email(self, field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError('不能修改为相同的邮箱！')