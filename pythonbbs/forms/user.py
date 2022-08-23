from wtforms import Form,StringField,ValidationError,BooleanField,FileField
from wtforms.validators import Email,EqualTo,Length
from flask_wtf.file import FileAllowed
from exts import cache
from models.user import UserModel
from .baseform import BaseForm

class RegisterForm(BaseForm):
  email = StringField(validators=[Email(message="请输入正确格式的邮箱！")])
  captcha = StringField(validators=[Length(min=4,max=4,message="请输入正确格式的验证码！")])
  username = StringField(validators=[Length(min=2,max=20,message="请输入正确长度的用户名！")])
  password = StringField(validators=[Length(min=6,max=20,message="请输入正确长度的密码！")])
  confirm_password = StringField(validators=[EqualTo("password",message="两次密码不一致！")])

  def validate_email(self,field):
    email = field.data
    user = UserModel.query.filter_by(email=email).first()
    if user:
      raise ValidationError(message="邮箱已经存在")


  def validate_captcha(self,field):
    captcha = field.data
    email = self.email.data
    cache_captcha = cache.get(email)
    if not cache_captcha or captcha != cache_captcha:
      raise ValidationError(message="验证码错误！")


class LoginForm(BaseForm):
  email = StringField(validators=[Email(message="请输入正确格式的邮箱！")])
  password = StringField(validators=[Length(min=6, max=20, message="请输入正确长度的密码！")])
  remember = BooleanField()


class EditProfileForm(BaseForm):
  username = StringField(validators=[Length(min=2,max=20,message="请输入正确格式的用户名！")])
  avatar = FileField(validators=[FileAllowed(['jpg','jpeg','png'],message="文件类型错误！")])
  signature = StringField()

  def validate_signature(self,field):
    signature = field.data
    if signature and len(signature) > 100:
      raise ValidationError(message="签名不能超过100个字符")