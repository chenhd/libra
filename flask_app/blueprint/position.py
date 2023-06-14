import re

from flask import Blueprint
from flask import render_template

from flask_app.models import *


position_data = Blueprint('position', __name__, url_prefix='/position')

@position_data.route('/')
def stock_data_root():
    # return "hello"
    # return stock_data_with_symbol("SH600900") # 长江电力
    dict_data = {}
    return render_template("layouts/content/position.html", dict_data=dict_data)