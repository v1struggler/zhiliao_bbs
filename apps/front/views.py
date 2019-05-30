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

from .forms import SignupForm
from .models import FrontUser
from exts import db
from utils import restful, safeutils

bp = Blueprint("front", __name__)


@bp.route('/')
def index():
    return "front index"


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


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
