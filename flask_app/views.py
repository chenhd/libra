import os
import collections
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


# @app.route('/test_sidebars')
# def test_sidebars():

#     # todo： https://stackoverflow.com/questions/15501518/dynamic-navigation-in-flask

#     dict_data = collections.OrderedDict()
#     dict_data["home"] = [
#         {
#             "name": "name",
#             "url": "url"
#         },
#         {
#             "name": "name2",
#             "url": "url2"
#         },
#     ]
#     dict_data["dashboard"] = [
#         {
#             "name": "name3",
#             "url": "url3"
#         },
#         {
#             "name": "name4",
#             "url": "url4"
#         },
#     ]

#     return render_template("base.html", dict_data=dict_data)

@app.route('/test_home')
def test_home():
    return render_template("layouts/_default/test_base.html")


@app.route('/test_hello')
def test_hello():
    return render_template("layouts/content/hello.html")

@app.route('/test_zxc')
def test_zxc():
    return render_template("layouts/content/zxc.html")


@app.route("/get_indexes_data/<index>", methods=["GET"])
def get_indexes_data(index):
    # todo: 
    #   1. 行业占比 饼图
    #   2. 趋势
    #   3. 历史位置
    symbol = "SH000300" # 沪深300



    from flask_app.vendor.csindex.csindex import csindex_client
    csindex_industry_data = csindex_client.get_csindex_industry_data()
    csindex_000300_closeweight_data = csindex_client.get_csindex_000300_closeweight_data()
    
    import pandas as pd
    df_data = pd.merge(csindex_000300_closeweight_data, csindex_industry_data, left_on="成分券代码Constituent Code", right_on="证券代码", how="left")

    df_data.groupby("中证一级行业分类代码简称")[["权重(%)weight"]].agg("sum").sort_values("权重(%)weight", ascending=False)
    df_data.groupby("中证二级行业分类代码简称")[["权重(%)weight"]].agg("sum").sort_values("权重(%)weight", ascending=False)
    df_data.groupby("中证三级行业分类简称")[["权重(%)weight"]].agg("sum").sort_values("权重(%)weight", ascending=False)


    csindex_industry_level_1 = df_data.groupby("中证一级行业分类代码简称")[["权重(%)weight"]].agg("sum").sort_values("权重(%)weight", ascending=False)
    csindex_industry_level_2 = df_data.groupby("中证二级行业分类代码简称")[["权重(%)weight"]].agg("sum").sort_values("权重(%)weight", ascending=False)
    csindex_industry_level_3 = df_data.groupby("中证三级行业分类简称")[["权重(%)weight"]].agg("sum").sort_values("权重(%)weight", ascending=False)

    csindex_industry_level_1_data_list = []
    for index, row in csindex_industry_level_1.iterrows():
        # print(index)
        # print(row.name, row.values[0])
        csindex_industry_level_1_data_list.append(
                {
                    "name": row.name,
                    "value": row.values[0]
                }
            )


    dict_data = {
        "csindex_industry_level_1": csindex_industry_level_1_data_list,
        "csindex_industry_level_2": csindex_industry_level_2,
        "csindex_industry_level_3": csindex_industry_level_3
    }

    return render_template("layouts/content/indexes_data.html", dict_data=dict_data)
