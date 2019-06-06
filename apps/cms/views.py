# 定义视图
import random

from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    redirect,
    url_for,
    g,
    jsonify
)

from .models import CMSUser, CMSPersmission
from ..models import BannerModel, BoardModel, PostModel, HighlightPostModel
from .forms import LoginForm, ResetpwdForm, ResetEmailForm, AddBannerForm, UpdateBannerForm, AddBoardForm, UpdateBoardForm
from .decorators import login_required, permission_required
import config
from exts import db, mail
from flask_mail import Message
from utils import restful, zlcache
import string
from tasks import send_mail

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


@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html', banners=banners)


@bp.route('/abanner/', methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/ubanner/', methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图！')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请传入轮播图id！')

    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图！')

    db.session.delete(banner)
    db.session.commit()
    return restful.success()


@bp.route('/posts/')
@login_required
@permission_required(CMSPersmission.POSTER)
def posts():
    post_list = PostModel.query.all()
    return render_template('cms/cms_posts.html', posts=post_list)


@bp.route('/hpost/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def hpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子！")

    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/uhpost/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def uhpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子！")

    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/comments/')
@login_required
@permission_required(CMSPersmission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/boards/')
@login_required
@permission_required(CMSPersmission.BOARDER)
def boards():
    board_models = BoardModel.query.all()
    context = {
        'boards': board_models
    }
    return render_template('cms/cms_boards.html', **context)


@bp.route('/aboard/', methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/uboard/', methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个板块！')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dboard/', methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def dboard():
    board_id = request.form.get("board_id")
    if not board_id:
        return restful.params_error('请传入板块id！')

    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error(message='没有这个板块！')

    db.session.delete(board)
    db.session.commit()
    return restful.success()


@bp.route('/fusers/')
@login_required
@permission_required(CMSPersmission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')


@bp.route('/cusers/')
@login_required
@permission_required(CMSPersmission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/croles/')
@login_required
@permission_required(CMSPersmission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')


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
            # message = form.errors.popitem()[1][0]  # popitem返回字典里面的任意项 ("password",["请输入正确的面"])
            message = form.get_error()
            return self.get(message=message)


# 修改密码
class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # 因为前端是使用的ajax，所以这里要返回json数据：{"code":200,message=""}
                # return jsonify({"code": 200, "message": ""})
                return restful.success()  # 使用restful风格，但是没有使用flask-restful框架，比较麻烦，app/ios都是使用json数据的，所以用restful比较方便
            else:
                # return jsonify({"code": 400, "message": "旧密码错误！"})
                return restful.params_error("旧密码错误！")

        else:
            # message = form.get_error()
            # return jsonify({"code": 400, "message": message})
            return restful.params_error(form.get_error())


# 发送邮箱验证码，没有指定methed那么默认就是get
@bp.route('/email_captcha/')
def email_captcha():
    # 通过传递字符串的方式获取URL：/email_capthca/?email=714464655@qq.com
    email = request.args.get('email')
    if not email:
        return restful.params_error('请传递邮箱参数！')  # 因为数据是通过AJXA传输的，所以要返回json格式的数据

    # 生成验证码
    source = list(string.ascii_letters)  # string.ascii_letters：返回小写大写的a-z，将字符串转换成列表就可以向列表里面添加值了
    # source.extend(["0","1","2","3","4","5","6","7","8","9"])
    source.extend(map(lambda x: str(x), range(0, 10)))  # 将数字添加进列表
    captcha = "".join(random.sample(source, 6))

    # 给这个邮箱发送邮件
    #message = Message('Python论坛邮箱验证码', recipients=[email], body='您的验证码是：%s' % captcha)
    try:
        #mail.send(message)  # 同步的方式发送：可以通过URL来测试是否可以发送邮箱，接口是否能用
        send_mail.delay(subject='Python论坛邮箱验证码', recipients=[email], body='您的验证码是：%s' % captcha)
    except:
        return restful.server_error()
    zlcache.set(email, captcha)                   # 发送完验证码，将邮箱和验证码存储到memcache当中
    return restful.success()


# 修改邮箱
class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


# 此处定义的url必须与base.js中指定的url一样，这样选中的时候才会有颜色变化；
bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
