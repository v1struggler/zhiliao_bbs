# encoding: utf-8

from wtforms import Form


# 定义一个父类来定义一些公有的方法
class BaseForm(Form):

    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message

    def validate(self):     # 重写父类的验证器，调用父类的验证器
        return super(BaseForm, self).validate()
