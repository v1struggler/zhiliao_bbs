# 定义视图

from flask import Blueprint, views, render_template, request, session, redirect, url_for, g

from .models import CMSUser
from .forms import LoginForm
from .decorators import login_required
import config

bp = Blueprint("cms", __name__, url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


# 登录界面
class LoginView(views.MethodView):

    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id  # 由于前台也需要登录所以对"user.id"进行优化，"user.id"就是一个标识而已；
                if remember:
                    # 如果设置session.permanent = True：那么过期时间是31天
                    session.permanent = True
                return redirect(url_for('cms.index'))  # 翻转的时候一定要加蓝图的名称
            else:
                return self.get(message='邮箱或密码错误')
        else:
            message = form.errors.popitem()[1][0]  # popitem返回字典里面的任意项 ("password",["请输入正确的面"])
            return self.get(message=message)


# 修改密码
class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        pass
        # form = ResetpwdForm(request.form)
        # if form.validate():
        #     oldpwd = form.oldpwd.data
        #     newpwd = form.newpwd.data
        #     user = g.cms_user
        #     if user.check_password(oldpwd):
        #         user.password = newpwd
        #         db.session.commit()
        #         # {"code":200,message=""}
        #         # return jsonify({"code":200,"message":""})
        #         return restful.success()
        #     else:
        #         return restful.params_error("旧密码错误！")
        # else:
        #     return restful.params_error(form.get_error())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
