

from flask_app.vendor.net_base import Net_Base


class XueQiu_Base(Net_Base):
    # 雪球首页
    homepage = "https://xueqiu.com/"

    # 用于模拟浏览器对雪球的请求头
    headers = {
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        "sec-ch-ua-mobile": "?0",
        'sec-ch-ua-platform': '"macOS"',
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }


    # k-线链接模版，需要补充三个参数
    #   symbol：标的编号
    #   begin：当前时间戳相关值，已设置默认参数
    #   period：k-线周期指标，用于指定年k线、月k线等，主要标的为月k线
    KLINE_URL_TEMPLATE = "https://stock.xueqiu.com/v5/stock/chart/kline.json?" \
                         "symbol=%s" \
                         "&begin=%d" \
                         "&period=%s" \
                         "&type=before" \
                         "&count=-284" \
                         "&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance"
    
    # 个股基本面数据信息链接模版，需要补充一个参数
    #   symbol：标的编号
    QUOTE_INFO_URL_TEMPLATE = "https://stock.xueqiu.com/v5/stock/quote.json?" \
                              "symbol=%s" \
                              "&extend=detail"
    

    # 页面位置：个股页面-财务数据-利润表
    # 个股利润表，需要用多个子页查看各季度收入
    # symbol：标的编号
    # type为Q4表示年报数据，Q4指代年报，除此之外还有Q1、Q2、Q3、all
    # count 指代单次页面拉取数据大小，这里用与页面数据一样的请求方式单次仅请求5次
    # 子页索引通过timestamp实现，首次数据timestamp为空值
    INCOME_URL_TEMPLATE = "https://stock.xueqiu.com/v5/stock/finance/cn/income.json?" \
                          "symbol=%s" \
                          "&type=%s" \
                          "&is_detail=true&count=%d" \
                          "&timestamp=%s"

    
    # 页面位置：个股页面-公司概括-公司高管
    # 高管持股数据
    # symbol：标的编号
    SKHOLDER_URL_TEMPLATE = "https://stock.xueqiu.com/v5/stock/f10/cn/skholder.json?" \
                            "symbol=%s"
    


    # 页面位置：个股页面-公司运作-分红送配
    # 历年分红数据
    # symbol：标的编号
    # page：分红数据的子页索引，每页10条数据，如果刚好20条则第三页数据为空
    BONUS_URL_TEMPLATE = "https://stock.xueqiu.com/v5/stock/f10/cn/bonus.json?" \
                         "symbol=%s" \
                         "&size=10&page=%d&extend=true"
    



    # 页面位置：行情 - 行情中心 - 沪深一览 - （筛选市值倒序）
    # 股票当前市值
    # page：数据的子页索引，每页90条数据，第56页数据为空
    ALL_STOCK_MARKET_CAPITAL_URL_TEMPLATE = "https://stock.xueqiu.com/v5/stock/screener/quote/list.json?" \
                                            "page=%d" \
                                            "&size=90&order=desc&orderby=market_capital&order_by=market_capital&market=CN&type=sh_sz"