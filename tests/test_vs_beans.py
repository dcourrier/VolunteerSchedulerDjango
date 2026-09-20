from django.test import TestCase
from loguru import logger
'''
from vs.bean.beans import *  
 
class BeanTests(TestCase):
    
    def testBase(self):
        try:
            sdb = SessionDataBean()
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'
'''        