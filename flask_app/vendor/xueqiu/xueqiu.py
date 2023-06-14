
import re
import time
import requests
# import datetime


import pandas as pd
import numpy as np

from .xueqiu_base import XueQiu_Base

from collections import OrderedDict
from datetime import datetime

class XueQiu(XueQiu_Base):
    def __init__(self) -> None:
        self.session = requests.session()
        
        self.begin = int((time.time() + 3600*24) * 1000)

        self.create_cookies_in_session()

        self.df_all_stock_market_capital = None
    
    # def get(self, url):
    #     res = self.session.get(url, headers=self.headers)
    #     assert res.status_code == 200
    #     return res
    
    # 雪球请求涉及到cookies，需要在一开始的时候进行对首页的请求来生存所需cookies
    def create_cookies_in_session(self) -> None:
        res = self.get(self.homepage, headers=self.headers)


    

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
            data = datetime.utcfromtimestamp(x / 1000).strftime("%Y-%m")
            return data
        df_data["timestamp"] = df_data.apply(lambda x: timestamp_reformat(x.timestamp), axis=1)
        
        return df_data

    # 获取股票基本面数据信息
    def get_stock_info(self, symbol) -> dict:
        quote_info_url = self.QUOTE_INFO_URL_TEMPLATE % (symbol)

        res = self.get(quote_info_url, headers=self.headers)

        json_data = res.json()
        assert json_data["error_code"] == 0
        dict_data = self._do_quote_data(json_data)
        
        return dict_data

    def _do_quote_data(self, json_data) -> dict:
        quote_dict_data = json_data["data"]["quote"]
        return quote_dict_data
    
    # 获取股票历年利润数据
    def get_stock_income(self, symbol) -> dict:
        _type = "Q4" # Q4指代年报，除此之外还有Q1、Q2、Q3、all
        count = 5

        od_report = OrderedDict()

        timestamp = ""

        times = 0
        while True:
            times += 1
            if times > 10:
                raise Exception("todo: protect logic.")

            income_url = self.INCOME_URL_TEMPLATE % (symbol, _type, count, timestamp)

            res = self.get(income_url, headers=self.headers)
            data = res.json()
            for report in data["data"]["list"]:
                name = report["report_name"]
                od_report[name] = report
            
            if len(data["data"]["list"]) == count:
                # 通过最后一年的年报时间戳+1进行下个子页的搜索参数
                timestamp = data["data"]["list"][-1]["report_date"] + 1
            else:
                break
            
        # print(od_report)
        od_report = self._do_stock_income(od_report)
        # print(od_report)
        return od_report

    # 处理利润表数据，保留目标数据
    def _do_stock_income(self, od_report) -> OrderedDict:
        od_report_new = OrderedDict()
        for report_name, report in od_report.items():
            report_new = {}
            # 营业总收入
            report_new["total_revenue"] = report["total_revenue"]
            # 净利润
            report_new["net_profit"] = report["net_profit"]
            # 基本每股收益
            report_new["basic_eps"] = report["basic_eps"]
            od_report_new[report_name] = report_new

            # todo: 每个数据之后带带有一个相对变化的百分比数值
        
        return od_report_new

    # 获取个股高管持股数据
    def get_stock_skholder(self, symbol) -> OrderedDict:
        skholder_url = self.SKHOLDER_URL_TEMPLATE % (symbol)

        res = self.get(skholder_url, headers=self.headers)

        json_data = res.json()
        assert json_data["error_code"] == 0
        # print(json_data)

        target_list = []
        for item in json_data["data"]["items"]:
            target_item = {}
            # 姓名
            target_item["personal_name"] = item["personal_name"]
            # 职务
            target_item["position_name"] = item["position_name"]
            # 持股数
            target_item["held_num"] = item["held_num"]
            # 年薪
            target_item["annual_salary"] = item["annual_salary"]
            target_list.append(target_item)
        
        return target_list

    # 获取个股分红数据
    def get_stock_bonus(self, symbol) -> OrderedDict:
        # https://stock.xueqiu.com/v5/stock/f10/cn/bonus.json?symbol=SH600900&size=10&page=3&extend=true
        od_bonus = OrderedDict()
        
        page = 1

        times = 0
        while True:
            times += 1
            if times > 10:
                raise Exception("todo: protect logic.")
            

            bonus_url = self.BONUS_URL_TEMPLATE % (symbol, page)
            res = self.get(bonus_url, headers=self.headers)
            json_data = res.json()
            assert json_data["error_code"] == 0
            for item in json_data["data"]["items"]:
                target_dict = {}
                # 分红相关年报
                target_dict["dividend_year"] = item["dividend_year"]
                # 分红方案
                target_dict["plan_explain"] = item["plan_explain"]
                # 派息日
                target_dict["dividend_date"] = item["dividend_date"]
                
                od_bonus[target_dict["dividend_year"]] = target_dict
            
            if len(json_data["data"]["items"]) < 10:
                break
            else:
                page += 1
        
        od_bonus = self._do_stock_bonus(od_bonus)
        return od_bonus

    def _do_stock_bonus(self, od_bonus) -> OrderedDict:
        for dividend_year, item in od_bonus.items():
            if item["dividend_date"] is None:
                # 预案，未确定分红时间
                continue
            item["dividend_date"] = datetime.fromtimestamp(item["dividend_date"]/1000).strftime("%Y-%m-%d")
            # 将多个分红方案抽取成多个元素组成的list，默认仅关注第一个元素
            filter = re.findall("10派\d+.\d*元", item["plan_explain"])
            if len(filter) > 0:
                item["plan_explain"] = filter
            else:
            # todo: 还需处理复杂过滤方案
                item["plan_explain"] = [item["plan_explain"]]
        return od_bonus
        

    def get_all_stock_market_capital(self):
        # 路径：行情 - 行情中心 - 沪深一览 - （筛选市值倒序）
        # https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page=1&size=90&order=desc&orderby=market_capital&order_by=market_capital&market=CN&type=sh_sz

        # od_all_stock_market_capital = OrderedDict()
        # list_all_stock_market_capital = []
        if self.df_all_stock_market_capital is None:
            df_all_stock_market_capital = pd.DataFrame(columns=["symbol", "market_capital"])

            page = 1

            times = 0
            while True:
                times += 1
                if times > 100:
                    raise Exception("todo: protect logic.")
                
                url = self.ALL_STOCK_MARKET_CAPITAL_URL_TEMPLATE % (page)
                res = self.get(url, headers=self.headers)
                json_data = res.json()
                assert json_data["error_code"] == 0
                if "list" in json_data["data"]:
                    for item in json_data["data"]["list"]:
                        # 股票编号、股票市值
                        df_all_stock_market_capital.loc[len(df_all_stock_market_capital.index)] = [item["symbol"], item["market_capital"]]
                    
                    page += 1
                else:
                    break
            
            df_all_stock_market_capital = self._do_all_stock_market_capital(df_all_stock_market_capital)
            self.df_all_stock_market_capital = df_all_stock_market_capital
        return self.df_all_stock_market_capital
    
    def _do_all_stock_market_capital(self, df_all_stock_market_capital):
        # 筛除B股数据
        df_all_stock_market_capital = df_all_stock_market_capital[~df_all_stock_market_capital["symbol"].str.startswith("SH900")]
        # 去除股票代码前缀
        df_all_stock_market_capital["symbol"] = df_all_stock_market_capital["symbol"].str[2:]
        return df_all_stock_market_capital
                


            



        





    
xueqiu_client = XueQiu()