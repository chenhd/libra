
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
    # print(xueqiu_client)

    df_data = xueqiu_client.get_kline_data_month(symbol)
    # print(df_data)

    df_data = _do_kline_month_fluctuation_data(df_data)

    return df_data



def _get_peak_and_vally_from_boundary(df_data, index, boundary=6):
    sum = 0  # 累加值
    target_value = [None, 0]  # 目标极值[索引, 极值]

    for index, row in df_data[["percent"]].iterrows():
        sum += df_data.loc[index].percent
        # 存在峰谷，峰即极大值，谷即极小值，此处加上相对值比较是针对极小值进行比较
        if abs(sum) > abs(target_value[1]): 
            target_value = [index, sum]
        
        # 当遍历索引超过目标边界值时，即判定为在该目标边界下，目标索引所在位置即峰谷位置
        if target_value[0] is not None and \
            index - target_value[0] > boundary:
            break

    return target_value



    pass

# 获取k线的峰谷值，用于评估在一个周期时间内的峰顶与谷底的位置
# threshold: 初始观测指标水平，用于触发观测流程
def get_kline_peak_and_vally(df_data, threshold=10):
    dict_data = {
        # 目标峰顶值索引列表
        "peak_index": [],
        # 目标谷底值索引列表
        "vally_index": []
    }


    # 上一个观测峰谷值索引，用于滤去已确认目标索引之前的值
    # 比如：从索引0开始观测得峰顶值索引为5，故1至5、2至5等计算无需再次进行，直接跳至5继续后续的观测
    last_target_index = 0

    for index, row in df_data.iterrows():
        if index <= last_target_index:
            continue # 筛掉新端点的左侧趋势数据
        if abs(row["percent"]) < threshold:
            continue # 筛除“初始”涨跌幅未达到观测指标的数据

        target_value = _get_peak_and_vally_from_boundary(df_data[df_data.index >= index], index)
        target_index, target_sum = target_value
        if target_sum > 0: # 峰顶值
            dict_data["peak_index"].append([target_value, df_data.loc[target_index].timestamp])
        else: # 谷底值
            dict_data["vally_index"].append([target_value, df_data.loc[target_index].timestamp])
        
        last_target_index = target_index
    
    # 转换数据格式为前端可直接渲染数据
    peak_and_vally_list = []
    for index in dict_data.values():
        for value in index:
            peak_and_vally_list.append([value[1], value[0][1]])

    
    return peak_and_vally_list




