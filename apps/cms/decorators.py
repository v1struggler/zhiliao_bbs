# encoding: utf-8
from flask import session, redirect, url_for, g
from functools import wraps
import config


# 登录限制装饰器
def login_required(func):
    @wraps(func)                             # 这个装饰器是：保留函数func的属性，防止属性丢失
    def inner(*args, **kwargs):
        if config.CMS_USER_ID in session:    # session其实就是一个字典，判断一个key是否在字典中
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))

    return inner


# 限制cms用户权限
def permission_required(permission):       # 最外面的这层函数是为了接受参数   有两层装饰器
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.index'))
        return inner
    return outter
