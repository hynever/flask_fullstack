from wtforms import Form, StringField,BooleanField,SubmitField, ValidationError,PasswordField
from wtforms.validators import length, email, equal_to
from flask_wtf import FlaskForm

registed_email = ['aa@example.com', 'bb@example.com']


class RegisterForm(Form):
    username = StringField(validators=[length(min=3, max=20, message="请输入正确长度的用户名！")])
    email = StringField(validators=[email(message="请输入正确格式的邮箱！")])
    password = StringField(validators=[length(min=6, max=20, message="请输入正确长度的密码！")])
    confirm_password = StringField(validators=[equal_to("password", message="两次密码不一致！")])

    def validate_email(self, field):
        email = field.data
        if email in registed_email:
            raise ValidationError("邮箱已经被注册！")
        return True


class LoginForm(FlaskForm):
    email = StringField(label="邮箱：",validators=[email(message="请输入正确格式的邮箱！")],render_kw={"placeholder":"请输入邮箱"})
    password = PasswordField(label="密码：",validators=[length(min=6, max=20, message="请输入正确长度的密码！")],render_kw={"placeholder":"请输入密码"})
    remember = BooleanField(label="记住我：")
    submit = SubmitField(label="提交")
