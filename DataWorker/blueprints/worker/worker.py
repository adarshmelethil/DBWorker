
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from DataWorker.blueprints.auth import login_required
from DataWorker.db import get_db

bp = Blueprint('worker', __name__, template_folder='templates')

@bp.route('/')
def index():
  return render_template("index.html")
