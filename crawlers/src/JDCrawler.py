#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import time
import requests
import gevent
import gevent.monkey
import logging
import logging.config

from settings import *
from utils import sendEmail

logging.config.fileConfig(LOG_CONF_PATH, disable_existing_loggers=False, 
    defaults={'logfilename': CRAWLERS_LOG_PATH, 'name': 'crawlers'})
logger = logging.getLogger('crawlers')
gevent.monkey.patch_socket()


class JDCrawler(object):

    @staticmethod
    def run(good, threshold, result):
        """ 爬取商品价格，并判断是否达到期望阈值 """
        def _runOnce(good, threshold):
            priceUrl = JD_PRICE_URL_PATTRN % good
            goodUrl = JD_GOOD_URL_PATTERN % good
            try:
                resp = requests.get(priceUrl, timeout=3)
                if resp.status_code != 200:
                    raise Exception("Wrong response status [status=%d]" % (resp.status_code))
                price = float(json.loads(resp.text)[0]['p'])
                if price <= threshold:
                    return True, "SUCC: [%s/%s] %s" % (str(price), str(threshold), goodUrl)
                else:
                    logger.info("High price [good=%s] [price=%s] [threshold=%s]" % 
                        (goodUrl, str(price), str(threshold)))
                    return False, ''
            except Exception, e:
                logger.error("Request except [url=%s], error: %s" % (priceUrl, str(e)))
                return None, "FAIL: [%s] %s" % (str(e), goodUrl)

        for _ in xrange(MAX_REQUEST_TIMES):
            isDown, text = _runOnce(good, threshold)
            if isDown is not None:
                break

        if isDown != False:
            result.append(text)


def main():
    result = []
    gevent.joinall([gevent.spawn(JDCrawler.run, good, threshold, result) 
        for good, threshold in JD_GOODS.items()])
    logger.info("Result: %s" % str(result))
    if result:
        try:
            sendEmail(EMAIL_TO_ADDRS, u'[%s] 京东价格爬取汇总' % time.strftime('%Y-%m-%d'), '\n'.join(result))
        except Exception, e:
            logger.error("Send email failed, error: %s" % str(e))
        else:
            logger.info("Send email success")


if __name__ == '__main__':
    main()
