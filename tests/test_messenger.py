from django.test import TestCase
from django.utils import timezone
from datetime import datetime as DT,timedelta,time
from loguru import logger

from vscode.msgr.msgr import *
class MessageTest(TestCase):

    def test1(self):
        err = None
        s = None
        try:
            m = Message(messageType=MessageType.ERROR,
                        severity=MessageSeverity.FATAL,
                        text='message 1')
            m.method = 'method'
            s = str(m) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(e)
        assert not err, 'got an exception'
        assert s, 'no text'