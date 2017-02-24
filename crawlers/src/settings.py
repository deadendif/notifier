#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 日志配置文件
LOG_CONF_PATH = "../etc/logger.conf"
# 日志文件路径
CRAWLERS_LOG_PATH = "../logs/crawlers.log"
# 收件人地址，多个收件人逗号分割
EMAIL_TO_ADDRS = 'xxxxx@qq.com'
# 失败情况下最大请求次数
MAX_REQUEST_TIMES = 3
# RPC调用地址
HOST = 'localhost'
# RPC调用端口
PORT = 9090

# 京东商品地址模式
JD_GOOD_URL_PATTERN = 'https://item.jd.com/%s.html'
# 京东商品价格地址模式
JD_PRICE_URL_PATTRN = 'http://p.3.cn/prices/get?skuid=J_%s'
# 京东商品及期望价格阈值
JD_GOODS = {
    '4281194': 300,
    '3792237': 310,
    '4281214': 320
}