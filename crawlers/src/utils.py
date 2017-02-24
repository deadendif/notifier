#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../lib/')

from sendEmail import SendEmail
from settings import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


def sendEmail(toAddrs, subject, body):
    """ 发送邮件 """
    transport = TSocket.TSocket(HOST, PORT)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = SendEmail.Client(protocol)
    transport.open()
    b = client.send(toAddrs, subject, body)
    transport.close()