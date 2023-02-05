
import pandas as pd

from .vendor.xueqiu.xueqiu import xueqiu_client

def _do_kline_month_fluctuation_data(df_data) -> pd.DataFrame:
    # 新增属性列
    # 当月波动额：当月最高值-当月最低值
    df_data["chg_current"] = df_data["high"] - df_data["low"]
    # 当月波动幅：当月波动额/当月最低值*100%
    df_data["percent_current"] = df_data["chg_current"] / df_data["low"] * 100


    # 数据处理：滤去不重要的数据，仅保留关注的有效数据
    df_data = df_data[[
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "chg",
            "percent",
            "chg_current",
            "percent_current",
            "pe",
            "pb",
            "ps",
            "pcf",
            "market_capital"
        ]]
    
    return df_data


# 获取月K线的数据波动情况
def get_kline_month_fluctuation(symbol) -> pd.DataFrame:
    print(xueqiu_client)

    df_data = xueqiu_client.get_kline_data_month(symbol)
    print(df_data)

    df_data = _do_kline_month_fluctuation_data(df_data)

    return df_data




    pass