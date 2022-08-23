from datetime import timedelta
import os

class BaseConfig:
  SECRET_KEY = "your secret key"
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  PERMANENT_SESSION_LIFETIME = timedelta(days=7)

  UPLOAD_IMAGE_PATH = os.path.join(os.path.dirname(__file__),"media")

  PER_PAGE_COUNT = 10


class DevelopmentConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/pythonbbs?charset=utf8mb4"

  # 邮箱配置
  MAIL_SERVER = "smtp.163.com"
  MAIL_USE_SSL = True
  MAIL_PORT = 465
  MAIL_USERNAME = "hynever@163.com"
  MAIL_PASSWORD = "1111111111111"
  MAIL_DEFAULT_SENDER = "hynever@163.com"

  # 缓存配置
  CACHE_TYPE = "RedisCache"
  CACHE_REDIS_HOST = "127.0.0.1"
  CACHE_REDIS_PORT = 6379

  # Celery配置
  # 格式：redis://:password@hostname:port/db_number
  CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
  CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"

  AVATARS_SAVE_PATH = os.path.join(BaseConfig.UPLOAD_IMAGE_PATH,"avatars")



class TestingConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI = "mysql+pymysql://[测试服务器MySQL用户名]:[测试服务器MySQL密码]@[测试服务器MySQL域名]:[测试服务器MySQL端口号]/pythonbbs?charset=utf8mb4"


class ProductionConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI = "mysql+pymysql://[生产环境服务器MySQL用户名]:[生产环境服务器MySQL密码]@[生产环境服务器MySQL域名]:[生产环境服务器MySQL端口号]/pythonbbs?charset=utf8mb4"
