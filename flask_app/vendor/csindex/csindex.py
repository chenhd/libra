
import requests
import urllib
import os

import pandas as pd

from .csindex_base import CSIndex_Base

class CSIndex(CSIndex_Base):
    def __init__(self) -> None:
        super().__init__()

        self.csindex_industry_data = None
    


    ################################################################################################################################################
    csindex_industry_url = CSIndex_Base.homepage + "csindex-home/exportExcel/security-industry-search-excel/CH"
    def _download_csindex_industry_data_file(self) -> pd.DataFrame:
        payload = {
            "searchInput": "",
            "pageNum": 1, 
            "pageSize": 10, 
            "sortField": None,
            "sortOrder": None
        }
        res = self.post(self.csindex_industry_url, json=payload)

        filename = res.headers["Content-disposition"].split("=")[1]
        filename = urllib.parse.unquote(filename)
        # filepath = self.base_store_data_path + filename

        filepath = self.save_download_file(filename, res.content)

        # todo: too slow to be speed up.
        df_data = pd.read_excel(filepath, engine="calamine")

        return df_data

    def _do_csindex_industry_data(self, df_data) -> pd.DataFrame:
        # # 筛除港股
        # df_data = df_data[~df_data["证券代码"].str.contains("HK")]

        # 筛除港股等非正常A股
        df_data = df_data[df_data["证监会行业大类代码"].notnull()]
        # 筛除B股
        df_data = df_data[~df_data["证券代码"].str.startswith("900")]
        
        return df_data

    # 获取中证行业分类数据
    # 位置：中证官网 中证行业分类（首页-产品与服务-中证数据服务-行业分类数据-中证行业分类|证监会行业分类
    # url: https://www.csindex.com.cn/#/dataService/industryClassification
    def get_csindex_industry_data(self) -> pd.DataFrame:
        if self.csindex_industry_data is None:
            df_data = self._download_csindex_industry_data_file()
            df_data = self._do_csindex_industry_data(df_data)

            self.csindex_industry_data = df_data

        return self.csindex_industry_data

    ################################################################################################################################################
    # 以指数id动态获取目标指数个股权重数据
    def get_csindex_target_closeweight_data(self, index_id) -> pd.DataFrame:
        target_handle_name = "get_csindex_" + index_id + "_closeweight_data"
        target_handle = getattr(self, target_handle_name)
        
        df_data = target_handle()
        return df_data
    ################################################################################################################################################
    csindex_000300_closeweight_url = "https://csi-web-dev.oss-cn-shanghai-finance-1-pub.aliyuncs.com/static/html/csindex/public/uploads/file/autofile/closeweight/000300closeweight.xls"
    def _download_csindex_000300_closeweight_data_file(self) -> pd.DataFrame:
        res = self.get(self.csindex_000300_closeweight_url)
        filename = self.csindex_000300_closeweight_url.split("/")[-1]

        filepath = self.save_download_file(filename, res.content)

        df_data = pd.read_excel(filepath, converters={"成分券代码Constituent Code":str})

        return df_data

    def _do_csindex_000300_closeweight_data(self, df_data) -> pd.DataFrame:
        df_data = df_data[[
            "日期Date",
            "指数名称 Index Name",
            "成分券代码Constituent Code",
            "成分券名称Constituent Name",
            "权重(%)weight"
            ]]
        # print(df_data)
        return df_data
        
    # 获取沪深300个股权重
    # 位置：中证官网 沪深300指数-样本权重数据（首页-产品与服务-指数体系与服务-指数浏览器
    # url: https://www.csindex.com.cn/#/indices/family/detail?indexCode=000300
    def get_csindex_000300_closeweight_data(self) -> pd.DataFrame:
        df_data = self._download_csindex_000300_closeweight_data_file()
        df_data = self._do_csindex_000300_closeweight_data(df_data)

        return df_data
        




csindex_client = CSIndex()