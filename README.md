# libra

install: 
    cd .\flask_app\static\npm
    npm install

todo
    - move data in
        * kline-month
        * cs indices
    * create strategy
    - flask work with bootstrap
    - vendor cache
    * manage data
    * index analyse

level:
    * sources(vendor)
    * target data
    * front chart
    * table

target
    * 离散度
    * 仓位管理
    * 趋势概率

depend lib:
    * requests
    * requests_cache
    * pandas
    * flask
    * pytest
    * openpyxl
    * xlrd

    web:
    * echarts
    * bootstrap
