from flask import Flask,request,render_template,redirect,url_for,flash
from forms import RegisterForm,LoginForm
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.secret_key = "sfajksd"
CSRFProtect(app)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # request.form是html模板提交上来的表单数据
        form = RegisterForm(request.form)
        # 如果表单验证通过
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data

            # 以下可以把数据保存到数据库的操作
            print("email:",email)
            print("username:",username)
            print("password:",password)
            return "注册成功！"
        else:
            print(form.errors)
            for errors in form.errors.values():
                for error in errors:
                    flash(error)
            return redirect(url_for("register"))


@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm(meta={"csrf":False})
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print("email:",email)
        print("password:",password)
        return redirect("/")
    print(form.errors)
    return render_template("login.html",form=form)



if __name__ == '__main__':
    app.run()
