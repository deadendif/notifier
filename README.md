# notifier
基于Thrift框架实现的邮件通知服务及简单的爬虫程序。

### 说明
#### emailServer
基于Thrift框架实现的邮件通知服务。

##### 启动服务

```bash
cd notifier/emailService/src && nohup python SendEmailServer.py &
```

#### crawlers
极简爬虫，基于协程实现了在单个线程内多个爬虫的并发爬取。

动机：京东上商品价格经常波动，有时候对于想买但不急买的商品，不希望高价买入又不想天天关注商品价格，所以就写个简单的爬虫，根据商品历史价格配置期望价格，每天爬取对应商品价格。当商品价格不高于期望值时通过PRC发送邮件通知。

##### 启动程序
```bash
cd notifier/crawlers/src && python JDCrawler.py
```
