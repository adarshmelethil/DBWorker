import os 


# class Config(object):
  # basedir = os.path.abspath(os.path.dirname(__file__))

  # SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

  # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
  #   "sqlite:///" + os.path.join(basedir, "app.db")
  # SQLALCHEMY_TRACK_MODIFICATIONS = False

  # DATABASE = os.environ.get("DATABASE_URL") \
  #   or os.path.join(basedir, "app.db")

  # # REDIS_URL = "redis://localhost"

  # 

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(16)

DATABASE = os.environ.get("DATABASE_URL") \
  or os.path.join(basedir, "app.db")
