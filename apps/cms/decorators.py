# encoding: utf-8
from flask import session, redirect, url_for
from functools import wraps
import config

# 登录限制装饰器
def login_required(func):
    @wraps(func)  # 这个装饰器是：保留函数func的属性
    def inner(*args, **kwargs):
        if config.CMS_USER_ID in session:    # session其实就是一个字典，判断一个key是否在字典中
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))

    return inner

