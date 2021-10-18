from flask import Flask

app = Flask(__name__, template_folder=r"E:\flask_fullstack\demo04\mytemplates")


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
