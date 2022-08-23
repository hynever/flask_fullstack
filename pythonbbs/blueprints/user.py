from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash, session, g, send_from_directory
from exts import cache,db
import random
from utils import restful
from forms.user import RegisterForm, LoginForm, EditProfileForm
from models.user import UserModel
from decorators import login_required
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
import os

bp = Blueprint("user",__name__,url_prefix="/user")

@bp.route("/register",methods=['GET','POST'])
def register():
  if request.method == 'GET':
    return render_template("front/register.html")
  else:
    form = RegisterForm(request.form)
    if form.validate():
      email = form.email.data
      username = form.username.data
      password = form.password.data
      user = UserModel(email=email,username=username,password=password)
      db.session.add(user)
      db.session.commit()
      return redirect(url_for("user.login"))
    else:
      for message in form.messages:
        flash(message)
      return redirect(url_for("user.register"))


@bp.route("/mail/captcha")
def mail_captcha():
  try:
    email = request.args.get("mail")
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    captcha = "".join(random.sample(digits, 4))
    subject="【知了Python论坛】注册验证码"
    body = f"【知了Python论坛】您的注册验证码是：{captcha}，请勿告诉别人！"
    current_app.celery.send_task("send_mail",(email,subject,body))
    cache.set(email, captcha, timeout=100)
    return restful.ok()
  except Exception as e:
    print(e)
    return restful.server_error()


@bp.route('/login',methods=['GET','POST'])
def login():
  if request.method == 'GET':
    return render_template("front/login.html")
  else:
    form = LoginForm(request.form)
    if form.validate():
      email = form.email.data
      password = form.password.data
      remember = form.remember.data
      user = UserModel.query.filter_by(email=email).first()
      if user and user.check_password(password):
        if not user.is_active:
          flash("该用户已被禁用！")
          return redirect(url_for("user.login"))
        session['user_id'] = user.id
        if remember:
          session.permanent = True
        return redirect("/")
      else:
        flash("邮箱或者密码错误！")
        return redirect(url_for("login"))
    else:
      for message in form.messages:
        flash(message)
      return render_template("front/login.html")


@bp.get('/logout')
def logout():
  session.clear()
  return redirect("/")


@bp.get("/profile/<string:user_id>")
def profile(user_id):
  user = UserModel.query.get(user_id)
  is_mine = False
  if hasattr(g,"user") and g.user.id == user_id:
    is_mine = True
  context = {
    "user": user,
    "is_mine": is_mine
  }
  print(user)
  return render_template("front/profile.html",**context)


@bp.post("/profile/edit")
@login_required
def edit_profile():
  form = EditProfileForm(CombinedMultiDict([request.form,request.files]))
  if form.validate():
    username = form.username.data
    avatar = form.avatar.data
    signature = form.signature.data

    # 如果上传了头像
    if avatar:
      # 生成安全的文件名
      filename = secure_filename(avatar.filename)
      # 拼接头像存储路径
      avatar_path = os.path.join(current_app.config.get("AVATARS_SAVE_PATH"), filename)
      # 保存文件
      avatar.save(avatar_path)
      # 设置头像的url
      g.user.avatar = url_for("media.media_file",filename=os.path.join("avatars",filename))

    g.user.username = username
    g.user.signature = signature
    db.session.commit()
    return redirect(url_for("user.profile",user_id=g.user.id))
  else:
    for message in form.messages:
      flash(message)
    return redirect(url_for("user.profile",user_id=g.user.id))