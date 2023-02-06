



def test_get_kline_data_month():
    from flask_app.models import get_kline_month_fluctuation
    from flask_app.models import get_kline_peak_and_vally
    # symbol = "SH000300" # 沪深300
    symbol = "SH600036" # 招商银行
    df_data = get_kline_month_fluctuation(symbol)
    get_kline_peak_and_vally(df_data)


