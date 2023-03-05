



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