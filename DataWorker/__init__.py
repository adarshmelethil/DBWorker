from flask import Flask
from . import db


def create_app():
  app = Flask(__name__)

  # Configuration
  app.config.from_envvar('DW_SETTINGS')

  # Setup db
  db.init_app(app)

  # Blueprints
  from DataWorker.blueprints import auth, worker
  app.register_blueprint(auth.bp)
  app.register_blueprint(worker.bp)
  app.add_url_rule('/', endpoint='index')

  return app
