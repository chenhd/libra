

from flask_app.vendor.net_base import Net_Base


class CSIndex_Base(Net_Base):
    # 中证数据首页
    homepage = "https://www.csindex.com.cn/"

    def __init__(self) -> None:
        super().__init__()