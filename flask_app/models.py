


from .vendor.xueqiu.xueqiu import xueqiu_client

# 获取月K线的数据波动情况
def get_kline_month_fluctuation(symbol):
    print(xueqiu_client)

    df_data = xueqiu_client.get_kline_data_month(symbol)

    print(df_data)


    pass