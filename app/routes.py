from flask import Blueprint, request, render_template
import datetime
from .logger import log_request

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    log_request(request)
    return render_template("index.html")
