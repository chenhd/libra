import re

from flask import Blueprint
from flask import render_template
from flask import request

from flask_app.models import *


cs_type_data = Blueprint('cs_type', __name__, url_prefix='/cs_type')

@cs_type_data.route('/')
def stock_data_root():
    dict_data = {}
    print(request.args)
    cs_type_level = -1
    cs_type_name = ""

    cs_type_level = request.args.get("cs_type_level")
    cs_type_name = request.args.get("cs_type_name")
    print(cs_type_name)
    

    csindex_industry_data = get_csindex_industry_data()
    all_stock_market_capital = get_all_stock_market_capital()
    # all_stock_market_capital["symbol"] = all_stock_market_capital["symbol"].str[2:]

    df_data = pd.merge(csindex_industry_data, all_stock_market_capital, left_on="证券代码", right_on="symbol", how="outer")

    # # csindex_industry_level_1 = df_data.groupby("中证一级行业分类简称")[["market_capital"]].agg("sum").sort_values("market_capital", ascending=False)
    # csindex_industry_level_2 = df_data.groupby("中证二级行业分类简称")[["market_capital"]].agg("sum").sort_values("market_capital", ascending=False)
    # csindex_industry_level_3 = df_data.groupby("中证三级行业分类简称")[["market_capital"]].agg("sum").sort_values("market_capital", ascending=False)



    if cs_type_level == "2":
        cs_type_level_name = "中证二级行业分类简称"
    elif cs_type_level == "3":
        cs_type_level_name = "中证三级行业分类简称"
    else:
        raise Exception("todo")

    # 聚合行业分类后进行市值聚集汇总排序
    cs_type_level_data = df_data.groupby(cs_type_level_name)[["market_capital"]].agg("sum").sort_values("market_capital", ascending=False)





    dict_data["cs_type_level_name"] = cs_type_level_name
    dict_data["cs_type_level_data"] = cs_type_level_data.to_dict()["market_capital"]

    if cs_type_name == None:
        dict_data["cs_type_name"] = None
    else:
        # 如果请求带有类型名称，则返回该类型具体个股数据
        dict_data["cs_type_name"] = cs_type_name

        cs_type_level_stock = df_data[df_data[cs_type_level_name]==cs_type_name][["证券代码", "证券代码简称", cs_type_level_name, "market_capital"]].sort_values("market_capital", ascending=False)

        cs_type_level_stock["证券雪球链接"] = cs_type_level_stock["证券代码"]
        cs_type_level_stock["证券雪球链接"] = cs_type_level_stock["证券雪球链接"].where(~cs_type_level_stock["证券雪球链接"].str.startswith("00"), "SZ"+cs_type_level_stock["证券雪球链接"])
        cs_type_level_stock["证券雪球链接"] = cs_type_level_stock["证券雪球链接"].where(~cs_type_level_stock["证券雪球链接"].str.startswith("30"), "SZ"+cs_type_level_stock["证券雪球链接"])
        cs_type_level_stock["证券雪球链接"] = cs_type_level_stock["证券雪球链接"].where(~cs_type_level_stock["证券雪球链接"].str.startswith("60"), "SH"+cs_type_level_stock["证券雪球链接"])
        cs_type_level_stock["证券雪球链接"] = cs_type_level_stock["证券雪球链接"].where(~cs_type_level_stock["证券雪球链接"].str.startswith("68"), "SH"+cs_type_level_stock["证券雪球链接"])
        cs_type_level_stock["证券雪球链接"] = "https://xueqiu.com/S/" + cs_type_level_stock["证券雪球链接"]

        dict_data["cs_type_level_stock"] = cs_type_level_stock.T.to_dict()








    
    return render_template("layouts/content/cs_type.html", dict_data=dict_data)