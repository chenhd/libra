



def test_get_kline_data_month():
    from flask_app.models import get_kline_month_fluctuation
    
    # symbol = "SH000300" # 沪深300
    symbol = "SH600036" # 招商银行
    get_kline_month_fluctuation(symbol)
