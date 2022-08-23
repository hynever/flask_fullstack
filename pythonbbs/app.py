import click
from flask import Flask
from exts import db, mail, cache, csrf, avatars
import config
from flask_migrate import Migrate
from blueprints.cms import bp as cms_bp
from blueprints.front import bp as front_bp
from blueprints.user import bp as user_bp
from blueprints.media import bp as media_bp
import commands
from bbs_celery import make_celery
import hooks
import filters
import logging


app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
db.init_app(app)
mail.init_app(app)
cache.init_app(app)
avatars.init_app(app)


# 设置日志级别
app.logger.setLevel(logging.INFO)


# CSRF保护
csrf.init_app(app)

migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(user_bp)
app.register_blueprint(media_bp)

# 添加命令
app.cli.command("create-permission")(commands.create_permission)
app.cli.command("create-role")(commands.create_role)
app.cli.command("create-test-front")(commands.create_test_user)
app.cli.command("create-board")(commands.create_board)
app.cli.command("create-test-post")(commands.create_test_post)
app.cli.command("create-admin")(commands.create_admin)

# 构建celery
celery = make_celery(app)

# 添加钩子函数
app.before_request(hooks.bbs_before_request)
app.errorhandler(401)(hooks.bbs_401_error)
app.errorhandler(404)(hooks.bbs_404_error)
app.errorhandler(500)(hooks.bbs_500_error)

# 添加模板过滤器
app.template_filter("email_hash")(filters.email_hash)



if __name__ == '__main__':
  app.run()
