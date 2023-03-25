import re

from flask import Blueprint
from flask import render_template

from flask_app.models import *


bp_stock_data = Blueprint('stock_data', __name__, url_prefix='/stock_data')

@bp_stock_data.route('/')
def stock_data_root():
    # return "hello"
    return stock_data_with_symbol("SH600900") # 长江电力


# 布局：
#     基本面、
#     月k done!
#     收入、分红k线（独立图 done!
#     高管持股
@bp_stock_data.route("/<symbol>", methods=["GET"])
def stock_data_with_symbol(symbol):
    # symbol = "SH600900" # 长江电力
    # symbol = "SH603444" # 吉比特
    # symbol = "SH603444" # 吉比特


    stock_info_dict = get_stock_info(symbol)
    stock_info_data = {}

    # 名称
    stock_info_data["name"] = stock_info_dict["name"]
    # 编号
    stock_info_data["symbol"] = symbol
    # 当前股价
    stock_info_data["current"] = stock_info_dict["current"]
    # 动态市盈率
    stock_info_data["pe_ttm"] = stock_info_dict["pe_ttm"]
    # 市净率
    stock_info_data["pb"] = stock_info_dict["pb"]
    # 净资产收益率
        # eps: 每股利润, Earnings Per Share
        # navps: 每股资产净值, Net Asset Value Per Share (NAVPS)
    stock_info_data["roe"] = stock_info_dict["eps"] / stock_info_dict["navps"]
    

    # 总市值
    stock_info_data["market_capital"] = stock_info_dict["market_capital"]
    # 总股本
    stock_info_data["total_shares"] = stock_info_dict["total_shares"]
    # 流通市值
    stock_info_data["float_market_capital"] = stock_info_dict["float_market_capital"]
    # 流通股
    stock_info_data["float_shares"] = stock_info_dict["float_shares"]
    # 流通率
    stock_info_data["float_ratio"] = stock_info_data["float_shares"] / stock_info_data["total_shares"]

    # # 资产总值
    # total_assets = market_capital / pb
    # # 总股本
    # stock_info_data["total_shares"] = stock_info_dict["total_shares"]
    # # 流通股
    # stock_info_data["float_shares"] = stock_info_dict["float_shares"]




    kline_df = get_kline_data_month(symbol)

    kline_data = {}
    kline_data["timestamp"] = kline_df["timestamp"].to_list()
    kline_data["close"] = kline_df["close"].to_list()


    bonus_dict = get_stock_bonus(symbol)
    
    bonus_data = {}
    bonus_data["dividend_date"] = [ item["dividend_date"] for key, item in bonus_dict.items() if re.match("10派\d+.*\d*元", item["plan_explain"][0]) ][::-1]
    bonus_data["plan_explain"] = [ re.search("10派(\d+.*\d*)元", item["plan_explain"][0]).group(1) for key, item in bonus_dict.items() if re.match("10派\d+.*\d*元", item["plan_explain"][0]) ][::-1]
    bonus_data["bonus_ratio"] = []
    for index in range(len(bonus_data["dividend_date"])):
        date = bonus_data["dividend_date"][index][:-3] # 截断具体日期只保留年月
        close = kline_data["close"][kline_data["timestamp"].index(date)] if date in kline_data["timestamp"] else None
        if close == None:
            bonus_data["bonus_ratio"].append(None)
        else:
            # ratio = "{:.2%}".format(float(bonus_data["plan_explain"][index]) / close / 10)
            ratio = "{:.2}".format(float(bonus_data["plan_explain"][index]) / close / 10)
            bonus_data["bonus_ratio"].append(ratio)

    # todo： to show bonus_data["bonus_ratio"]


    
    skholder_list = get_stock_skholder(symbol)
    skholder_data = [person for person in skholder_list if person["held_num"] is not None]

    for person in skholder_data:
        
        person["held_num_percent"] = person["held_num"]/stock_info_data["total_shares"]

        person["held_num"] = "{:7.2f}".format(person["held_num"]/10000) + "万"
        person["held_num_percent"] = "{:.4%}".format(person["held_num_percent"])
        person["annual_salary"] = "{:7.2f}".format(person["annual_salary"]/10000) + "万" if person["annual_salary"] is not None else None



    # # todo：
    #     1. 分红是用来降低持有的风险，分红变化与影响显示
    #     2. 盈利核心：还得T，T的周期管理！


    # 转化为百分比字符串格式
    stock_info_data["roe"] = "{:.2%}".format(stock_info_data["roe"])
    # 转化数值格式
    stock_info_data["market_capital"] = str(int(stock_info_data["market_capital"]/100000000)) + "亿"
    stock_info_data["float_market_capital"] = str(int(stock_info_data["float_market_capital"]/100000000)) + "亿"
    stock_info_data["total_shares"] = "{:.4}".format(float(stock_info_data["total_shares"]/100000000)) + "亿"
    stock_info_data["float_shares"] = "{:.2}".format(float(stock_info_data["float_shares"]/100000000)) + "亿"
    stock_info_data["float_ratio"] = "{:.2%}".format(stock_info_data["float_ratio"])
    dict_data = {}
    dict_data["stock_info_data"] = stock_info_data
    dict_data["kline_data"] = kline_data
    dict_data["bonus_data"] = bonus_data
    dict_data["skholder_data"] = skholder_data

    return render_template("layouts/content/stock.html", dict_data=dict_data)