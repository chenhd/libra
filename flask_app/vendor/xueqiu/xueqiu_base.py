

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
    #   symbol：标的名称
    #   begin：当前时间戳相关值，已设置默认参数
    #   period：k-线周期指标，用于指定年k线、月k线等，主要标的为月k线
    KLINE_URL_TEMPLATE = "https://stock.xueqiu.com/v5/stock/chart/kline.json?" \
                         "symbol=%s" \
                         "&begin=%d" \
                         "&period=%s" \
                         "&type=before" \
                         "&count=-284" \
                         "&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance"
    
    