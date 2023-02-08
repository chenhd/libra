
import time
import requests
import datetime

import pandas as pd
import numpy as np

from .xueqiu_base import XueQiu_Base


class XueQiu(XueQiu_Base):
    def __init__(self) -> None:
        self.session = requests.session()
        
        self.begin = int((time.time() + 3600*24) * 1000)

        self.create_cookies_in_session()
    
    # def get(self, url):
    #     res = self.session.get(url, headers=self.headers)
    #     assert res.status_code == 200
    #     return res
    
    # 雪球请求涉及到cookies，需要在一开始的时候进行对首页的请求来生存所需cookies
    def create_cookies_in_session(self) -> None:
        res = self.get(self.homepage)




    def get_kline_data_month(self, symbol) -> pd.DataFrame:
        period = "month"
        return self.get_kline_data(symbol, period)

    def get_kline_data(self, symbol, period) -> pd.DataFrame:
        kline_url = self.KLINE_URL_TEMPLATE % (symbol, self.begin, period)

        res = self.get(kline_url, headers=self.headers)

        json_data = res.json()
        assert json_data["error_code"] == 0
        df_data = self.do_kline_data(json_data)

        

        return df_data

    # 列名说明：
    #     0. timestamp 指的是当月最后一天的收盘时间
    #     1. volume 指的是成交量的股数，除以100即成交的手数
    #     2. open 指的是开盘价
    #     3. high 指的是最高价
    #     4. low 指的是最低价
    #     5. close 指的是收盘价
    #     6. chg 指的是涨跌额，当前交易日最新成交价（或收盘价）与前一交易日收盘价相比较所产生的数值
    #     7. percent 指的是涨跌幅，涨跌额/前一个交易日收盘价*100%
    #     8. turnoverrate 指的是换手率
    #     9. amount 指的是成交金额
    #     10. volume_post
    #     11. amount_post
    #     12. pe 指的是市盈率，总市值/盈利（净利润），分静态市盈率（去年数据）、动态市盈率（E）（今年数据预测）、滚动市盈率（TTM）
    #     13. pb 指的是市净率，总市值/净资产
    #     14. ps 指的是市销率，总市值/主营业务收入，适合因为某些原因暂时出现亏损的企业以及周期性企业，不同行业市销率标准不同
    #     15. pcf 指的是市现率，股价/每股现金流，或是市值/经营现金流，市现率，就是分母（其他指标中的利润或者营收）变成经营现金流。相比其他指标，现金流本身就足以精确的反映企业的财务健康状况，因为它简单地说明了流进、流出企业的现金是多少
    #     16. market_capital 总市值
    #     17. balance 资产？？待明确 todo
    #     18. hold_volume_cn
    #     19. hold_ratio_cn
    #     20. net_volume_cn
    #     21. hold_volume_hk
    #     22. hold_ratio_hk
    #     23. net_volume_hk
    def do_kline_data(self, json_data) -> pd.DataFrame:
        # 1. 数据抽取
        main_data = json_data["data"]
        symbol = main_data["symbol"]
        columns_name = main_data["column"]
        item_data = main_data["item"]

        # 2. 生成df
        df_data = pd.DataFrame(np.array(item_data), columns=columns_name)

        # 3. 增加数据处理列
        # 修改时间戳列的可读性
        def timestamp_reformat(x):
            data = datetime.datetime.utcfromtimestamp(x / 1000).strftime("%Y-%m")
            return data
        df_data["timestamp"] = df_data.apply(lambda x: timestamp_reformat(x.timestamp), axis=1)
        
        return df_data

        pass






    
xueqiu_client = XueQiu()