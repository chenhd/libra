



from numpy import kaiser
import pandas as pd

def test_get_kline_data_month():
    from flask_app.models import get_kline_month_fluctuation
    from flask_app.models import get_kline_peak_and_vally
    # symbol = "SH000300" # 沪深300
    symbol = "SH600036" # 招商银行
    df_data = get_kline_month_fluctuation(symbol)
    get_kline_peak_and_vally(df_data)


def test_get_csindex_industry_data():

    from flask_app.vendor.csindex.csindex import csindex_client
    csindex_industry_data = csindex_client.get_csindex_industry_data()
    csindex_000300_closeweight_data = csindex_client.get_csindex_000300_closeweight_data()
    
    import pandas as pd
    df_data = pd.merge(csindex_000300_closeweight_data, csindex_industry_data, left_on="成分券代码Constituent Code", right_on="证券代码", how="left")

    df_data.groupby("中证一级行业分类代码简称")[["权重(%)weight"]].agg("sum").sort_values("权重(%)weight", ascending=False)
    df_data.groupby("中证二级行业分类代码简称")[["权重(%)weight"]].agg("sum").sort_values("权重(%)weight", ascending=False)
    df_data.groupby("中证三级行业分类简称")[["权重(%)weight"]].agg("sum").sort_values("权重(%)weight", ascending=False)

    print("hello")

# def test_get_indexes_data():
#     from flask_app.models import
def test_get_stock_data():
    from flask_app.models import get_stock_info
    # symbol = "SH600036" # 招商银行
    symbol = "SH600900" # 长江电力
    data = get_stock_info(symbol)
    # print(data)
    # todo:
        # 1. 价格
        # 2. 市盈率、市净率
        # 3. 净资产收益率
        # 4. 资产/营收、营收/利润
        # 5. 高管持股数
        # 6. 分红质量（与债券比对）、分红概率、分红稳定性
        # 7. 下跌风险评估

    # 当前股价
    current = data["current"]
    # 动态市盈率
    pe_ttm = data["pe_ttm"]
    # 市净率
    pb = data["pb"]
    # 净资产收益率
        # eps: 每股利润, Earnings Per Share
        # navps: 每股资产净值, Net Asset Value Per Share (NAVPS)
    roe = data["eps"] / data["navps"]
    # 总市值
    market_capital = data["market_capital"]
    # 总股本
    total_shares = data["total_shares"]
    # 流通市值
    float_market_capital = data["float_market_capital"]
    # 流通股
    float_shares = data["float_shares"]
    # # 资产总值
    # total_assets = market_capital / pb
    # 总股本
    total_shares = data["total_shares"]
    # 流通股
    float_shares = data["float_shares"]

    from flask_app.models import get_stock_income
    data = get_stock_income(symbol)
    # print(data)


    from flask_app.models import get_stock_skholder
    data = get_stock_skholder(symbol)
    # print(data)


    from flask_app.models import get_stock_bonus
    data = get_stock_bonus(symbol)

    # todo：融合k线面板


    # 布局：
    #     基本面、
    #     月k
    #     收入、分红k线（独立图
    #     高管持股



def test_get_all_stock_market_capital():
    from flask_app.models import get_all_stock_market_capital, get_csindex_industry_data

    csindex_industry_data = get_csindex_industry_data()
    all_stock_market_capital = get_all_stock_market_capital()
    all_stock_market_capital["symbol"] = all_stock_market_capital["symbol"].str[2:]

    print("hello")

    df_data = pd.merge(csindex_industry_data, all_stock_market_capital, left_on="证券代码", right_on="symbol", how="outer")


    csindex_industry_level_1 = df_data.groupby("中证一级行业分类简称")[["market_capital"]].agg("sum").sort_values("market_capital", ascending=False)
    csindex_industry_level_2 = df_data.groupby("中证二级行业分类简称")[["market_capital"]].agg("sum").sort_values("market_capital", ascending=False)
    csindex_industry_level_3 = df_data.groupby("中证三级行业分类简称")[["market_capital"]].agg("sum").sort_values("market_capital", ascending=False)

    df_data[df_data["中证二级行业分类简称"]=="银行"].sort_values("market_capital", ascending=False)

    print(df_data)