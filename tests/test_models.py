



def test_get_kline_data_month():
    from flask_app.models import get_kline_month_fluctuation
    
    symbol = "SH000300" # 沪深300
    get_kline_month_fluctuation(symbol)
