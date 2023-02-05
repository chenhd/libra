
from . import app

from flask import render_template
from .models import get_kline_month_fluctuation

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/about/<var_name>', methods=["GET"])
def about(var_name):
    data = {
        "key": "value",
        # "type": type(app)
        "list": [1, 2, 3],
        "var_name": var_name
    }
    return render_template("about.html", dict_data=data)


# from flask import request
# @app.route('/login/<username>', methods=['GET'])
# def login(username):
#     print(username)

@app.route("/test")
def test():
    symbol = "SH600036" # 招商银行
    df_data = get_kline_month_fluctuation(symbol)

    dict_data = {}
    dict_data["xAxis_data"] = df_data["timestamp"].to_list()
    dict_data["percent_data"] = df_data["percent"].to_list()
    dict_data["percent_current_data"] = df_data["percent_current"].to_list()

    return render_template("test.html", dict_data=dict_data)


    pass