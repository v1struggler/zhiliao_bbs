# 定义视图

from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    url_for,
    abort,
    g
)

from .forms import SignupForm, SigninForm
from .models import FrontUser
from ..models import BannerModel
from exts import db
from utils import restful, safeutils
import config

bp = Blueprint("front", __name__)


@bp.route('/')
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    context = {
        'banners': banners
    }
    return render_template('front/front_index.html', **context)


class SignupView(views.MethodView):

    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signup.html', return_to=return_to)  # 将需要跳转的url传递给前端模板，这样js就可以获取到
        else:
            return render_template('front/front_signup.html')

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for("front.signup") and safeutils.is_safe_url(
                return_to):
            return render_template('front/front_signin.html', return_to=return_to)
        else:
            return render_template('front/front_signin.html')

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remeber.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id                     # 将用户id保存在session中，持久化登录
                if remember:
                    session.permanent = True            # session保存31天
                return restful.success()
            else:
                return restful.params_error(message='手机号或密码错误！')
        else:
            return restful.params_error(message=form.get_error())


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))