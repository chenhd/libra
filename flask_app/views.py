import os
from . import app

from flask import render_template
from flask import send_from_directory

from .models import get_kline_month_fluctuation
from .models import get_kline_peak_and_vally

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

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
    # symbol = "SH600036" # 招商银行
    symbol = "SH000300" # 沪深300
    df_data = get_kline_month_fluctuation(symbol)

    dict_data = {}
    dict_data["xAxis_data"] = df_data["timestamp"].to_list()
    dict_data["percent_data"] = df_data["percent"].to_list()
    dict_data["percent_current_data"] = df_data["percent_current"].to_list()

    peak_and_vally_list = get_kline_peak_and_vally(df_data)
    dict_data["peak_and_vally_data"] = peak_and_vally_list

    return render_template("test.html", dict_data=dict_data)


    pass