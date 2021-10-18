from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = "fasdfsdfasdkj"
socketio = SocketIO(app)


class UserManager:
    # 单例实例对象
    __instance = None
    # 所有用户，里面存储的是字典类型，字典中分别为sid和username
    # 比如{"sid": "assdfsgsd", "username":"张三"}
    _users = []

    # 设置单例设计模式
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(UserManager, cls).__new__(cls)
        return cls.__instance

    # 添加用户
    @classmethod
    def add_user(cls, username, sid):
        for user in cls._users:
            if user['sid'] == sid or user['username'] == username:
                return False
        cls._users.append({"sid": sid, "username": username})

    # 移除用户
    @classmethod
    def remove_user(cls, username):
        for user in cls._users:
            if user['username'] == username:
                cls._users.remove(user)
                return True
        return False

    # 根据key获取用户，key可以为sid或username
    @classmethod
    def get_user(cls, key):
        for user in cls._users:
            if user['sid'] ==  key or user['username'] == key:
                return user
        return None

    # 根据key判断是否有某个用户，key可以为sid或username
    @classmethod
    def has_user(cls, key):
        if cls.get_user(key):
            return True
        else:
            return False

    # 获取当前用户
    @classmethod
    def get_current_user(cls):
        username = session.get("username")
        for user in cls._users:
            if user['username'] == username:
                return user
        return None

    # 获取所有用户的用户名
    @classmethod
    def all_username(cls):
        return [user['username'] for user in cls._users]


rooms = ["Flask交流群"]


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("username"):
            return redirect("/login")
        else:
            return func(*args, **kwargs)
    return wrapper


class ResultCode:
    OK = 200
    ERROR_PARAMS = 400
    ERROR_SERVER = 500


def result(code=ResultCode.OK, data=None, message=""):
    return {"code": code, "data": data or {}, "message": message}


def send_personal(uid, message):
    data = {
        "message": message,
        "from_user": session.get("username")
    }
    return data


@app.route('/')
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form.get('username')
        if not username:
            return result(ResultCode.ERROR_PARAMS, message="请输入用户名")
        elif UserManager.has_user(username):
            return result(ResultCode.ERROR_PARAMS, message="此用户名已存在")
        session['username'] = username
        return result()


@socketio.on('connect')
@login_required
def connect():
    print("连接成功")
    UserManager.add_user(session.get("username"), request.sid)
    emit("users", {"users": UserManager.all_username()}, broadcast=True)
    return result(message="连接成功！")


@socketio.on("disconnect")
@login_required
def disconnect():
    UserManager.remove_user(session.get('username'))
    emit("users", {"users": UserManager.all_username()}, broadcast=True)


@socketio.on("personal")
def send_personal(data):
    to_username = data.get('to_user')
    message = data.get('message')
    if not to_username or not UserManager.has_user(to_username):
        return result(ResultCode.ERROR_PARAMS, message="请输入正确的目标用户")
    to_user = UserManager.get_user(to_username)
    emit("personal" ,{"message": message, "from_user": session.get("username")}, room=[to_user.get("sid")])


@socketio.on("join")
@login_required
def join(data):
    room = data.get("room")
    join_room(room)
    username = session.get("username")
    print(username+"加入群聊")
    send(username+"加入群聊", to=room)
    # 如果房间是新建的，则发布广播
    if not room in rooms:
        emit("rooms", {"rooms": rooms}, broadcast=True)


@socketio.on("leave")
@login_required
def leave(data):
    room = data.get("room")
    leave_room(room)
    username = session.get("username")
    send(username+"离开群聊", to=room)


@socketio.on("room_chat")
@login_required
def room_chat(data):
    room = data.get("room")
    message = data.get("message")
    from_user = UserManager.get_current_user().get("username")
    send({"message": message, "from_user": from_user}, to=room)


if __name__ == '__main__':
    socketio.run()
