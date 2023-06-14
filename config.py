# Place config variables here. One per line.

# Enable Flask's debugging features. Should be False in production
DEBUG = True



TEST_DICT = {
    "hello": {
        # "world": "/test_hello",
        # "t": "url2",
        "stock_data": "/stock_data",
        "position": "/position",
        # "indexes": "/get_indexes_data/SH000300", # todo /get_indexes_data/<index>
        "index new": "/index/?index_id=000300&csindex_industry_level=1",
        "cs_type": "/cs_type/?cs_type_level=2",
    },
    "2": {
        "zxc": "/test_zxc",
        "aqsed": "url4"
    },

    }



DOCS_SIDEBAR_DICT = {
    "指数分析": {
        "沪深300": "//SH000300",

    },
    "个股": {
        # "招商银行": "/todo/SH600036",
        "SH603444": {
            "name": "吉比特",
        }
    },
    "关注列表？": {

    }

}

GET_STOCK_DATA_DICT = {
    "SH603444": {
        "name": "吉比特",
    },
    "SH600036": {
        "name": "招商银行",
    },
    "SH600900": {
        "name": "长江电力",
    },
    "SH601318": {
        "name": "中国平安",
    },
    "SH600519": {
        "name": "贵州茅台",
    },
    "SH601857": {
        "name": "中国石油",
    },
    "SZ003816": {
        "name": "中国广核",
    },
    "SZ000651": {
        "name": "格力电器",
    },
    "SZ002352": {
        "name": "顺丰控股",
    },
    "SH603259": {
        "name": "药明康德",
    }   

}


INDEX_DATA_DICT = {
    "000300": {
        "name": "沪深300",
    },
}


# csindex_industry_level_1
CSINDEX_INDUSTRY_LEVEL = {
    "1": {
        "name": "中证一级行业分类简称",
    },
    "2": {
        "name": "中证二级行业分类简称",
    },
    "3": {
        "name": "中证三级行业分类简称",
    },
}


# cs_type_level_dict
CS_TYPE_LEVEL_DICT = {
    "2": "中证二级行业分类简称", 
    "3": "中证三级行业分类简称"
}


TRADING_POSITION_TARGET_COLOR = {
    "GROWTH": "pink",
    "STABLE": "green",
    "T": "red",
    # "Hedging": "yellow",
}

# 管理粒度：资产值 1%
TRADING_POSITION = {
    "TARGET": {
        # 成长型仓位: 不包含基金？
        "GROWTH": {
            
            "中概互联": 6.2,
            
            
        },
        # 稳定型仓位: 不包含基金？
        "STABLE": {
            "招商银行": 5.8,
            "中国平安": 2.7,

            "京东方A": 1.9,
            "格力电器": 1,
            "长江电力": 1.6,
            "中国广核": 1,
            # "中国石油": 0.7,
        },
        # 做T仓位
        "T基": {
            "中证银行": 4.3,
            "沪深300": 3,
            "上证50": 2,

            "恒生中国": 2.6,
            "中证证券保险": 1.8,
            "海外互联": 1.8,
            "中证保险": 1.1,
            "家用电器": 0.8,
            "港股红利": 0.7,
            "医疗": 0.5,
            "金融地产": 0.5,
            "中证5G": 0.45,

            
        },
        # 对冲避险仓位：货币、短债
        "Hedging": {
            "货币": 28, # 招商
            "短债": 4, # 招商
            "短债2": 2, # 蚂蚁券商
            "国开债": 4, # 蚂蚁债券
            "黄金": 0.5,
        }

    },
    "OLD": {
        # 做T仓位
        "T": {

        },
    }

}


rule = {
    "单个标的上限10%"
}
target = {
    "制造业",
    "游戏",
    "高ROE",
    "高T波动",
    "周期长的波动",
    "十年后的干股",
    "后除权",
    "各概念的榜首与发展趋势", # 证券、快递、医药等
    "势的预判：大、中、小",
    "选股器", # https://data.eastmoney.com/xuangu/


}
# 持有记录与操作记录
RECORD = [
    {
        "operate": "buy",
        "type": "T",
        "date": "asd",
        
    },

]










