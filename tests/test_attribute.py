from vscode.att.attribute import BooleanAttribute,IntegerAttribute,StringAttribute,NumericStringAttribute,CurrencyAttribute,TimeAttribute,DateAttribute
from django.test import TestCase
from django.utils import timezone
from datetime import datetime as DT,timedelta,time
from vscode.loader.loaders import *
from vscode.base.base import *
from vscode.base.business_objects  import *
from vs.models import *
from vscode.val.vals import ValueTableManager

class VolunteerSchedulerAttributeTests(TestCase):
    
    def testBooleanAttribute(self): 
        self.boolAtt = BooleanAttribute(
            name = 'boolAtt',
            allowInvalid=False,
            value=True)
        ok = True
        try:
            self.boolAtt.validate()
        except:
            ok = False
        self.assertIs(ok, True)
        
    def testIntegerAtt(self):  
        self.intAtt = IntegerAttribute(
            name='intAtt',
            allowInvalid=False,
            nullAllowed=False,
            value=7,
            minimum=0,
            maximum=10,
            hasMinimum=True,
            hasMaximum=True)
        ok = True
        self.intAtt.validate()
        self.assertIs(ok, True)
        
    def testNumericStringAtt(self):
        nsAtt = NumericStringAttribute(
        name='nsaAtt',
        value=11,
        allowInvalid=False,
        minimumLength=1,
        mixedCaseAllowed=True, 
        maximumLength=3,
        nullStringAllowed=False,
        hasMinimumLength=True,
        hasMaximumLength=True,
        allSpacesAllowed=False,
        leadingZeroRequired=False, 
        hasMinimumValue=True, 
        hasMaximumValue=True,
        maximumValue=999,
        minimumValue=1)
        ok = True
        try:
            nsAtt.validate()
        except Exception as e:
            logger.opt(exceptiom=True).debug('numericString')
            ok = False
            print(e)
        self.assertIs(ok, True)     
        
    def testStringAtt(self):
        self.sAtt = StringAttribute(
        name= 'saAtt' ,
            value= None ,
            nullAllowed=True,
            allowInvalid=False,
            minimumLength=3,
            maximumLength=None,
            mixedCaseAllowed=True,
            nullStringAllowed=False,
            hasMinimumLength=True,
            hasMaximumLength=False,
            allSpacesAllowed=False)
        ok = True
        self.sAtt.validate()
        self.assertIs(ok, True)
        
    def testCurrencyAtt(self):
        self.cAtt = CurrencyAttribute(
            name= 'cAtt',
            value=1.00,
            allowInvalid=False,
            nullAllowed=False,
            minimum = 1.00,
            maximum = None,
            hasMinimum = True,
            hasMaximum = False)
        ok = True
        self.cAtt.validate()
        self.assertIs(ok, True)
        
    def testDateAtt(self):
        self.dAtt = DateAttribute(
        name='dAtt',
        allowInvalid=False,
        nullAllowed=False,
        value=DT.now(),
        duration = 90,
        durationRequired = True)
        ok = True
        try:
            self.dAtt.validate()
        except Exception as e:
            err = e
            ok = False
        assert ok, 'dateattribue validate' + str(err)
        
    def testTimeAtt(self):
        self.tAtt = TimeAttribute(
            name='tAtt',
            allowInvalid=False, 
            nullAllowed=False, 
            value='00:00:01')
        ok = True
        self.tAtt.validate()
        self.assertIs(ok, True)
        
        