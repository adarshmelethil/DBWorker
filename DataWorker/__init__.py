from flask import Flask 
from . import db


def create_app():
  app = Flask(__name__)

  # Configuration
  app.config.from_envvar('DW_SETTINGS')

  # Setup db
  db.init_app(app)

  # Blueprints
  from DataWorker.blueprints import auth 
  app.register_blueprint(auth.bp)

  return app
