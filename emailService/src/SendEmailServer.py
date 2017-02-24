#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import smtplib
import logging
import logging.config

sys.path.append('../lib/')
from sendEmail import SendEmail

from settings import *
from email.header import Header
from email.mime.text import MIMEText

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


logging.config.fileConfig(LOG_CONF_PATH, disable_existing_loggers=False, 
    defaults={'logfilename': SEND_EMAIL_LOG_PATH, 'name': 'sendEmail'})
logger = logging.getLogger('sendEmail')


class SendEmailExecutor(object):

    def validate(self, toAddrs, subject, body):
        if not toAddrs or not subject or not body:
            return False
        return True

    def send(self, toAddrs, subject, body):
        logger.info("Sending email ...")
        logger.info("Email details: [toAddrs=%s] [subject=%s] [body=%s]" % (toAddrs, subject, body))

        if not self.validate(toAddrs, subject, body):
            logger.error("Invalid email params")
            return False

        fromAddr = EMAIL_USER
        email = MIMEText(body, 'plain', 'utf-8')
        email['Subject'] = Header(subject, 'utf-8').encode()
        email['From'] = fromAddr
        email['To'] = toAddrs

        try:
            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            # server.set_debuglevel(1)
            server.login(fromAddr, EMAIL_PASSWORD)
            server.sendmail(fromAddr, [toAddrs], email.as_string())
            server.quit()
        except Exception, e:
            logger.error("Sending email failure, error: %s" % (str(e)))
            return False
        else:
            logger.info("Sending email success")
            return True


if __name__ == '__main__':
    executor = SendEmailExecutor()
    processor = SendEmail.Processor(executor)
    transport = TSocket.TServerSocket(port=PORT)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    logger.info('Starting the server...')
    server.serve()
