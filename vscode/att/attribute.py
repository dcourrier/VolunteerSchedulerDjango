from abc import ABC, abstractmethod
import ast
from datetime import datetime as DT,timedelta,date,time
from decimal import Decimal,ROUND_HALF_UP
from vscode.utils.utils import Utils,VSMessages


class Attribute(ABC):
    
    def __init__(self, name=None, allowInvalid=True, nullAllowed=True):
        
        self.name = name
        self.allowInvalID = allowInvalid
        self._nullAllowed = nullAllowed
        
    @abstractmethod  
    def validate(self):
        pass
     
    def allowInvalid(self, allow):
        self.allowInvalID = allow

    def isAllowInvalid(self):
        return self.allowInvalid

    def isNullAllowed(self):        
        return self._nullAllowed
 
    def setNullAllowed(self, newnullAllowed):
        self._nullAllowed = newnullAllowed
        
    def getName(self):
        return self.name

    def setName(self, newName):
        self.name = newName
   
    @abstractmethod  
    def getValue(self):
        pass
    
    @abstractmethod  
    def __str__(self):
        pass
    

class BooleanAttribute(Attribute):
    
    def __init__(self,
         name,
         value=None,
         allowInvalid=False):        
        super().__init__(name = name,allowInvalid=allowInvalid)

        self.value = None

        if value != None:
            if value is True:
                self.value = value
            elif value is False:
                self.value = value
            else:
                if super().allowinvalID == False:
                    raise InvalidAttributeValueException(msg=AttributeMessageFactory.NOT_BOOLEAN_ERROR) 
               
    def validate(self):
        if self.value is None and not super().nullAllowed  and not super().allowInvalid:
            raise InvalidAttributeValueException('must not be null')
        
        if self.getValue() == None:
            if not super().isnullAllowed() and not super().isAllowInvalid():
                s = super().getName() + AttributeMessageFactory.NoneError()
                raise InvalidAttributeValueException(msg=s)

    def setValue(self, newValue):
        if newValue is True:
            self.value = True
        elif newValue is False:
            self.value = False
        else:
            v = ast.literal_eval(newValue)
            if v is True or v is False:
                self.value = v
            else:
                raise InvalidAttributeValueException(super().getName() + " requires a boolean")
 
    def getValue(self):
        return self.value

    def getValueString(self):
        result = ""
        if self.value != None:
            if self.value is True:
                result = "True"
            else:
                result ="False"
        return result

    def equals(self, obj):        
        result = True
        if isinstance(obj, BooleanAttribute):
            if obj.getName() is None and super().getName() is not None:
                result = False
            if obj.getName() != None and super().getName() == None:
                result = False
            if obj.getName() != None and super().getName() != None and obj.getName() != super().getName():
                result = False
            if obj.value == None and self.value != None:
                result = False
            if obj.value != None and self.value == None:
                result = False
            if obj.value != None and self.value != None and obj.value != self.valuee:
                result = False
            if obj.isnullAllowed() != super().isnullAllowed():
                result = False
        else:
            result = False
        return result 

    def __str__(self):
        return str(self.value)


class StringAttribute(Attribute):
    
    def __init__(
            self,
            name,
            value=None,
            nullAllowed=True,
            allowInvalid=False,
            minimumLength=None,
            maximumLength=None,
            mixedCaseAllowed=True,
            nullStringAllowed=True,
            hasMinimumLength=False,
            hasMaximumLength=False,
            allSpacesAllowed=True):
        
        super().__init__(name=name,allowInvalid=allowInvalid,nullAllowed=nullAllowed)
        
        self.value = value
        self.minimumLength = minimumLength
        self.maximumLength = maximumLength
        self.mixedCaseAllowed = mixedCaseAllowed
        self.nullStringAllowed = nullStringAllowed
        self.hasMinimumLength = hasMinimumLength
        self.hasMaximumLength = hasMaximumLength
        self.allSpacesAllowed = allSpacesAllowed
        
    def getValue(self):
        return self.value
    
    def setValue(self, newValue):
        s = self.getValue()
        self.value = newValue
        if not self.allowInvalid:
            try:
                if newValue == None and not super().isNullAllowed():
                    raise InvalidAttributeValueException(VSMessages.missingArgumentError('StringAttribute', 'setValue()'))
                self.validate()
            except InvalidAttributeValueException as e:
                self.value = s
                raise e

    def validate(self):
        result = True
        message = ''
        if self.getValue() is None:
            if not super().isNullAllowed():
                message += ';\n' + AttributeMessageFactory.NoneError()
                result = False
        else:
            val = self.getValue()
            if val and isinstance(val,bytes):
                val = val.decode()
            if not isinstance(val, str):
                val = str(val)
            if val and isinstance(val, str):
                if self.hasMaximumLength and len(val) > self.getMaximumLength():
                    message += '\n' + AttributeMessageFactory.maximumLengthError(len(val), self.getMaximumLength())
                    result = False
                elif val.strip() == ''  and not self.isnullStringAllowed:
                    message += '\n' + AttributeMessageFactory.nullStringError()
                    result = False

                if self.hasMinimumLength and self.minimumLength and len(val) < self.getMinimumLength():
                    message += '\n' + AttributeMessageFactory.minimumLengthError(len(val), self.getMinimumLength())
                    result = False
                s = val
                if val == s.upper() and val != s and not self.isMixedCase():
                    message += '\n' + AttributeMessageFactory.mixedCaseError(val)
                    result = False
    
                s = val
                if len(s) > 0 and len(s.strip()) == 0 and not self.isAllSpacesAllowed() and len(s) > 0:
                    message += '\n' + AttributeMessageFactory.allSpacesError()
                    result = False
            else:
                result = False
                message += '\nargument was not a string'
        if not result:
            raise InvalidAttributeValueException(message)

    def isNumeric(self, s):
        return Utils.isNumeric(s)
    
    def setHasMinimumLength(self, hasMin):
        if hasMin is True or hasMin is False:
            self.hasMinimumLength = hasMin
        else:
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_BOOLEAN_ERROR)

    def setMinimumLength(self, s):
        if not Utils.isNumeric(s) or s < 0:
            raise InvalidAttributeValueException(AttributeMessageFactory.minimumValueError(s, 0), super().getName())
        
        self.minimumLength = s
        self.setHasMinimumLength(True)
        self.allowInvalID = False
    
    def getMinimumLength(self):
        return self.minimumLength
    
    def setHasMaximumLength(self, hasMax):
        if hasMax is True or hasMax is False:
            self.hasMaximumLength = hasMax
        else:
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_BOOLEAN_ERROR)
    
    def hasMaximumLength(self):
        return self.hasMaximumLength
    
    def setMaximumLength(self, val):
        if not Utils.isNumeric(val) or val < 0:
            raise InvalidAttributeValueException(AttributeMessageFactory.minimumValueError(val, 0), super().getName())
        
        self.maximumLength = val
        self.setHasMaximumLength(True)
        self.allowInvalID = False
    
    def getMaximumLength(self):
        return self.maximumLength

    def setMixedCase(self, val):
        if val is True or val is False:
            self.mixedCaseAllowed = val
        else:
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_BOOLEAN_ERROR)

    def isMixedCase(self):
        return self.mixedCaseAllowed
    
    def setNullStringAllowed(self, val):
        if val is True or val is False:
            self.nullStringAllowed = val
        else:
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_BOOLEAN_ERROR)

    def isnullStringAllowed(self):
        return self.nullStringAllowed

    def setAllSpacesAllowed(self, val):
        if val is True or val is False:
            self.allSpacesAllowed = val
        else:
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_BOOLEAN_ERROR)

    def isAllSpacesAllowed(self):
        return self.allSpacesAllowed
    
    def getValueString(self):
        s = ''
        if self.value != None:
            s = self.getValue()
        return s

    def equals(self, obj):
        result = True
        if isinstance(obj, StringAttribute):
            att = obj
            if (att.isAllSpacesAllowed() != self.allSpacesAllowed):
                result = False
            
            elif (att.hasMaximumLength != self.hasMaximumLength):
                result = False
            
            elif (att.hasMinimumLength != self.hasMinimumLength):
                result = False
            
            elif (att.maximumLength != self.maximumLength):
                result = False
            
            elif (att.minimumLength != self.minimumLength):
                result = False
            
            elif (att.mixedCaseAllowed != self.mixedCaseAllowed):
                result = False
            
            elif (att.getName() == None and self.getName() != None):
                result = False
            
            elif (att.getName() != None and self.getName() == None):
                result = False
            
            elif att.getName() != None and self.getName() != None and att.getName() != self.getName():
                result = False
            
            elif (att.value == None and self.value != None):
                result = False
            
            elif (att.value != None and self.value == None):
                result = False
            
            elif att.value != None and self.value != None and att.value != self.value:
                result = False
            
            elif (att.isnullAllowed() != self.isnullAllowed()):
                result = False            
            else: 
                if att.nullStringAllowed != self.nullStringAllowed:
                    result = False            
        else:
            result = False
        
        return result
    
    def __str__(self):
        return self.value
    

class NumericStringAttribute(StringAttribute):

    def __init__(
        self,
        name,
        value=None,
        allowInvalid=False,
        minimumLength=None,
        mixedCaseAllowed=True, 
        maximumLength=None,
        nullStringAllowed=True,
        hasMinimumLength=False,
        hasMaximumLength=False,
        allSpacesAllowed=True,
        leadingZeroRequired=False, 
        hasMinimumValue=False, 
        hasMaximumValue=False,
        maximumValue=None,
        minimumValue=None
    ):
        super().__init__(
            name=name, 
            allowInvalid=allowInvalid, 
            minimumLength=minimumLength, 
            maximumLength=maximumLength, 
            mixedCaseAllowed=mixedCaseAllowed, 
            nullStringAllowed=nullStringAllowed, 
            hasMinimumLength=hasMinimumLength, 
            hasMaximumLength=hasMaximumLength, 
            allSpacesAllowed=allSpacesAllowed
        )
        self.nullAllowed=True,
        self.value=value
        self.leadingZeroRequired = leadingZeroRequired
        self.hasMinimumValue = hasMinimumValue
        self.hasMaximumValue = hasMaximumValue
        self.maximumValue = maximumValue
        self.minimumValue = minimumValue

    def getValue(self):
        return super().getValue()
        

    def validate(self):
        result = True
        message = ''
        try:
            super().validate()
        except InvalidAttributeValueException as e:
            message += e.getMsg()
            result = False
        
        if self.hasMaximumValue and self.hasMinimumValue:
            try:
                dMin = Decimal(self.getMinimumValue())
            except:
                message += '\n minimum value is not numeric'
                raise InvalidAttributeValueException(message)
            try:
                dMax = Decimal(self.getMaximumValue())
            except:
                message += '\n maximum value is not numeric'
                raise InvalidAttributeValueException(message)
            
            if dMin > dMax:
                result = False
                message += '\n' + AttributeMessageFactory.minMaxError(self.getMinimumValue(), self.getMaximumValue())
            
        valS = super().getValue()
        if valS != None and not Utils.isNumeric(valS):
            if valS.endswith(" "):
                message += '\n' + AttributeMessageFactory.trailingSpacesError()
                result = False
            
            s = valS.strip()
            if self.isLeadingZeroRequired():
                if s != valS:
                    message += '\n' + AttributeMessageFactory.leadTrailSpacesError()
                    result = False

            if not Utils.isNumeric(valS):
                message += '\n' + AttributeMessageFactory.notNumericError(valS)
                result = False
            else:
                intValue = int(s)
                if self.hasMaximumValue:
                    if intValue > float(self.getMaximumValue()):
                        message += '\n' + AttributeMessageFactory.maximumValueError(intValue, self.getMaximumValue())
                        result = False
                                    
                if self.hasMinimumValue:
                    if intValue < float(self.getMinimumValue()):
                        message += '\n' + AttributeMessageFactory.minimumValueError(intValue, self.getMinimumValue())
                        result = False                    
        if not result:
            raise InvalidAttributeValueException(message)

 
    def setLeadingZeroRequired(self, s):
        if s is True or s is False:
            self.leadingZeroRequired = s
        else:
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_BOOLEAN_ERROR)
   
    def isLeadingZeroRequired(self):
        return self.leadingZeroRequired
    
    def setHasMinimumValue(self, s):
        if s is True or s is False:
            self.hasMinimumValue = s
        else:
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_BOOLEAN_ERROR)
        
    def hasMinimumValue(self):
        return self.hasMinimumValue

    def setHasMaximumValue(self, s):
        if s is True or s is False:
            self.hasMaximumValue = s
        else:
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_BOOLEAN_ERROR)

    def hasMaximumValue(self):
        return self.hasMaximumValue

    def setMaximumValue(self, s):
        if Utils.isNumeric(s):
            self.maximumValue = float(s)
        else:
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_NUMERIC_ERROR)
 
    def getMaximumValue(self):
        return self.maximumValue
    
    def setMinimumValue(self, s):
        if Utils.isNumeric(s):
            self.minimumValue = float(s)
        else:
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_NUMERIC_ERROR)

    def getMinimumValue(self):
        return self.minimumValue
    
    def equals(self, att):
        result = True
        if isinstance(att, NumericStringAttribute):
            if (att.isAllSpacesAllowed() != self.isAllSpacesAllowed()):
                result = False
            
            if (att.hasMaximumLength() != self.hasMaximumLength()):
                result = False
            
            if (att.hasMinimumLength() != self.hasMinimumLength()):
                result = False
            
            if (att.getMaximumLength() != self.getMaximumLength()):
                result = False
            
            if (att.getMinimumLength() != self.getMinimumLength()):
                result = False
            
            if (att.isMixedCase() != self.isMixedCase()):
                result = False
            
            if (att.getName() == None and self.getName() != None):
                result = False
            
            if (att.getName() != None and self.getName() == None):
                result = False
            
            if (att.getName() != None and self.getName() != None and att.getName() != self.getName()):
                result = False
            
            if (att.getValue() == None and self.getValue() != None):
                result = False
            
            if (att.getValue() != None and self.getValue() == None):
                result = False
            
            if (att.getValue() != None and
                    self.getValue() != None and
                    att.getValue() != self.getValue()):
                result = False
            
            if (att.isnullAllowed() != self.isnullAllowed()):
                result = False
            
            if (att.isnullStringAllowed() != self.isnullStringAllowed()):
                result = False
            
            if (att.leadingZeroRequired != self.leadingZeroRequired):
                result = False
            
            if (att.hasMinimumValue != self.hasMinimumValue):
                result = False
            
            if (att.hasMaximumValue != self.hasMaximumValue):
                result = False
            
            if (att.minimumValue != self.minimumValue):
                result = False
            
            if (att.maximumValue != self.maximumValue):
                result = False
            
        else:
            result = False
        
        return result
    
    def __str__(self):
        return str(super().getValue())



class NumericAttribute(Attribute):

    def __init__(
        self,
        name,
        value=None,
        digits=9,
        decimalDigits=0,
        allowInvalid=False,
        nullAllowed=True,
        hasMinimumValue=False, 
        hasMaximumValue=False,
        maximumValue=None,
        minimumValue=None
    ):
        super().__init__(
            name=name,
            nullAllowed=nullAllowed, 
            allowInvalid=allowInvalid
        )
        
        self.hasMinimumValue = hasMinimumValue
        self.hasMaximumValue = hasMaximumValue
        self.maximumValue = maximumValue
        self.minimumValue = minimumValue
        self.nullAllowed=True
        self.value=value
        
        self.digits = digits
        self.hasMinimumDigits = True
        self.minimumDigits = 1
        self.hasMaximumDigits = True
        self.maximumDigits = 9
        
        self.decimalDigits = decimalDigits
        self.hasMinimumDecimalDigits = True
        self.minimumDecimalDigits = 0
        self.hasMaximumDecimalDigits = True
        self.maximumDecimalDigits = 7
        
        self.value = value
        
    def setDigits(self, val):
        if val < self.digits.minimum:
            raise InvalidAttributeValueException('digits too sall' )
        elif val > self.digits.maximum: 
            raise InvalidAttributeValueException('digits too long' )
        else:
            self.digits = val
            
    def getDigits(self):
        return self.digits
        
    def setDecimalDigits(self, val):
        if val < self.decimalDigits.minimum:
            raise InvalidAttributeValueException('decimalDigits too sall' )
        elif val > self.decimalDigits.maximum: 
            raise InvalidAttributeValueException('decimalDigits too long' )
        else:
            self.digits = val
            
    def getDecimalDigits(self):
        return self.decimalDigits

    def getValue(self):
        return self.value
        
    def setValue(self, val):
        oldVal = self.value
        try:
            self.value = val
            self.validate()
        except Exception as e:
            self.value = oldVal
            raise e
        
    def validate(self):
        result = True
        message = ''
        try:
            super().validate()
        except InvalidAttributeValueException as e:
            message += e.getMsg()
            result = False             
        if not result:
            raise InvalidAttributeValueException(message)
        if self.value and not self.allowInvalid:
            parts = self.value.as_integer_ratio()
            numPt = parts[0]
            fracPt = parts[1]
            if self.hasMaximumDecimalDigits:
                if len(str(abs(fracPt))) > self.maximumDecimalDigits:
                    result = False
                    message += "too many decimal digits"
            if self.hasMinimumDecimalDigits:
                if len(str(abs(fracPt))) < self.minimumDecimalDigits:
                    result = False
                    message += "too few decimal digits"
            if self.hasMaximumDigits:
                if len(str(abs(numPt))) > self.maximumDigits:
                    result = False
                    #print(str(parts) + ' ' + str(self.maximumDigits))
                    message += "too many digits"
            if self.hasMinimumDigits:
                if len(str(abs(numPt))) < self.minimumDigits:
                    result = False
                    message += "too few digits"
        if not result:
            raise InvalidAttributeValueException(message)
            
    def setHasMinimumValue(self, s):
        if s is True or s is False:
            self.hasMinimumValue = s
        else:
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_BOOLEAN_ERROR)
        
    def hasMinimumValue(self):
        return self.hasMinimumValue

    def setHasMaximumValue(self, s):
        if s is True or s is False:
            self.hasMaximumValue = s
        else:
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_BOOLEAN_ERROR)

    def hasMaximumValue(self):
        return self.hasMaximumValue

    def setMaximumValue(self, s):
        if Utils.isNumeric(s):
            self.maximumValue = float(s)
        else:
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_NUMERIC_ERROR)
 
    def getMaximumValue(self):
        return self.maximumValue
    
    def setMinimumValue(self, s):
        if Utils.isNumeric(s):
            self.minimumValue = float(s)
        else:
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_NUMERIC_ERROR)

    def getMinimumValue(self):
        return self.minimumValue
    
    def equals(self, att):
        result = True
        if isinstance(att, NumericAttribute):
            if att.digits != self.digits:
                result = False   
            elif att.digits.minimum != self.digits.minimum:
                result = False   
            elif att.digits.hasMaximum != self.digits.hasMaximum:
                result = False   
            elif att.digits.maximum != self.digits.maximum:
                result = False   
            elif att.decimalDigits != self.decimalDigits:
                result = False   
            elif att.decimalDigits.hasMinimum != self.decimalDigits.hasMinimum:
                result = False   
            elif att.decimalDigits.minimum != self.decimalDigits.minimum:
                result = False   
            elif att.decimalDigits.hasMaximum != self.decimalDigits.hasMaximum:
                result = False   
            elif att.decimalDigits.maximum != self.decimalDigits.maximum:
                result = False
            elif att.decimalDigits != self.decimalDigits:
                result = False
            elif (att.getName() == None and self.getName() != None):
                result = False
            
            elif (att.getName() != None and self.getName() == None):
                result = False
            
            elif (att.getName() != None and self.getName() != None and att.getName() != self.getName()):
                result = False
            
            elif (att.getValue() == None and self.getValue() != None):
                result = False
            
            elif (att.getValue() != None and self.getValue() == None):
                result = False
            
            elif (att.getValue() != None and
                    self.getValue() != None and
                    att.getValue() != self.getValue()):
                result = False
            
            elif (att.isnullAllowed() != self.isnullAllowed()):
                result = False
            
            elif (att.isnullStringAllowed() != self.isnullStringAllowed()):
                result = False
            
            elif (att.hasMinimumValue != self.hasMinimumValue):
                result = False
            
            elif (att.hasMaximumValue != self.hasMaximumValue):
                result = False
            
            elif (att.minimumValue != self.minimumValue):
                result = False
            
            elif (att.maximumValue != self.maximumValue):
                result = False
            
        else:
            result = False
        
        return result
    
    def __str__(self):
        return str(getValue())

class IntegerAttribute(Attribute):
    def __init__(
            self,
            name,
            allowInvalid=True,
            nullAllowed=True,
            value=None,
            minimum=None,
            maximum=None,
            hasMinimum=False,
            hasMaximum=False
    ):
        super().__init__(
            name=name,
            allowInvalid=allowInvalid,
            nullAllowed=nullAllowed)
        
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        self.hasMinimum = hasMinimum
        self.hasMaximum = hasMaximum

    def validate(self):
        result = True
        message = ''
        if self.getValue() == None:
            if not self.isNullAllowed():
                message += ('\n' + AttributeMessageFactory.NoneError())
                result = False
            
        else:
            if self.maximum and self.minimum:
                if self.minimum > self.maximum:
                    message += ('\n' + AttributeMessageFactory.minMaxError(self.getMinimum(), self.getMaximum()))
                    result = False
            if self.getValue():
                if self.maximum and self.getValue() > self.getMaximum():
                    message += ('\n' + AttributeMessageFactory.maximumValueError(self.getValue(), self.getMaximum()))
                    result = False
                
                if self.minimum and self.getValue() < self.getMinimum():
                    message += ('\n' + 
                            AttributeMessageFactory.minimumValueError(self.getValue(), self.getMinimum()))
                    result = False
        if not result:
            raise InvalidAttributeValueException(message)   
        
    
    def setValue(self, newV):
        if not Utils.isNumeric(newV):
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_NUMERIC_ERROR)
        val = self.getValue()
        self.value = newV

        if not self.allowInvalid:
            try:
                self.validate()
            except InvalidAttributeValueException as e:
                self.value = val
                raise e
            
    def getValue(self):
        return self.value
    
    def setHasMinimum(self, newV):
        if not Utils.isBoolean(newV):
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_BOOLEAN_ERROR)
        self.hasMinimum = newV
    
    def hasMinimum(self):
        return self.hasMinimum
    
    def setMinimum(self, newV):
        if not Utils.isNumeric(newV):
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_NUMERIC_ERROR)
        self.allowInvalID = False
        self.setHasMinimum(True)
        self.minimum = newV    

    def getMinimum(self):
        return self.minimum
    
    def hasMaximum(self):
        return self.hasMaximum
    
    def setMaximum(self, newV):
        if not Utils.isNumeric(newV):
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_NUMERIC_ERROR)
        self.allowInvalID = False
        self.setHasMaximum(True)
        self.maximum = newV
        
    def getMaximum(self):
        return self.maximum
    
    def setHasMaximum(self, newV):
        if not Utils.isBoolean(newV):
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_BOOLEAN_ERROR)
        self.hasMaximum = newV

    def getValueString(self):
        if self.value is None: 
            return 
        else: 
            return  self.getValue()

    def equals(self, att):
        result = True
        if isinstance(att, IntegerAttribute):
            if (att.hasMaximum != self.hasMaximum):
                result = False
            
            if (att.hasMinimum != self.hasMinimum):
                result = False
            
            if (att.maximum != self.maximum):
                result = False
            
            if (att.minimum != self.minimum):
                result = False
            
            if (att.getName() == None and self.getName() != None):
                result = False
            
            if (att.getName() != None and self.getName() == None):
                result = False
            
            if (att.getName() != None and self.getName() != None and att.getName() != self.getName()):
                result = False
            
            if (att.value == None and self.value != None):
                result = False
            
            if (att.value != None and self.value == None):
                result = False
            
            if (att.value != None and self.value != None and att.value != self.value):
                result = False
            
            if (att.isNullAllowed() != self.isNullAllowed()):
                result = False
            
        else:
            result = False
        
        return result
    
    def __str__(self):
        return "" + str(self.value)


class CurrencyAttribute(Attribute):
    def __init__(
            self,
            name,
            allowInvalid=True,
            nullAllowed=True,
            value=None,
            minimum = None,
            maximum = None,
            hasMinimum = False,
            hasMaximum = False
        ):
        super().__init__(
            name=name,
            allowInvalid=allowInvalid,
            nullAllowed=nullAllowed)
        self.value = None
        self.minimum = minimum
        self.maximum = maximum
        self.hasMinimum = hasMinimum
        self.hasMaximum = hasMaximum
        self.setValue(value)

    def validate(self):
        result = True
        message = ''
        if (self.getValue() == None):
            if not self.isnullAllowed():
                result = False
                message = ('\n' + AttributeMessageFactory.NoneError())            
        else:
            if not isinstance(self.value, Decimal):
                result = False
                message = ('\n' + AttributeMessageFactory.invalidCurrencyError(self.getValue()))
            elif self.hasMaximum and self.getValue() > self.getMaximum():
                result = False
                message = ('\n' + AttributeMessageFactory.maximumValueError(self.getValue(), self.getMaximum()))
            elif (self.hasMinimum and self.getValue() < self.getMinimum()):
                result = False
                message = ('\n' + AttributeMessageFactory.minimumValueError(self.getValue(), self.getMinimum()))
            elif (self.hasMaximum and self.hasMinimum and self.getMinimum() > self.getMaximum()):
                result = False
                message = ('\n' + AttributeMessageFactory.minMaxError(self.getMinimum(), self.getMaximum()))
        if not result:
            raise InvalidAttributeValueException(message)  

    def setValue(self, newV):
        oVal = self.value
        if newV is None:
            self.value = None
        else:
            if isinstance(newV, str):
                newV = Decimal(newV).quantize(Decimal(0.01), rounding=ROUND_HALF_UP)
            elif isinstance(newV, float):
                newV = Decimal(str(newV)) 
            elif isinstance(newV, int):
                newV = Decimal(newV)  
                
            if not isinstance(newV, Decimal):
                #print(CurrencyAttribute.setValue  + type(newV))
                raise InvalidAttributeValueException(AttributeMessageFactory.NOT_VALID_CURRENCY_ERROR)
            else:
                self.value = newV
                try:
                    self.validate()
                except InvalidAttributeValueException as e:
                    self.value = oVal
                    raise e
        
    def getValue(self):
        return self.value

    def setMinimum(self, newV):
        if isinstance(newV, int):
            newV = Decimal(newV)
        elif isinstance(newV, float):
                newV = Decimal(str(newV))   
        if not isinstance(newV, Decimal) and not newV is None:
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_VALID_CURRENCY_ERROR)
        if not newV is None:
            self.setHasMinimum(True)
            self.allowInvalID = False
        self.minimum = newV

    def getMinimum(self):
        return self.minimum

    def setMaximum(self, newV):
        if not isinstance(newV, Decimal) and not newV is None:
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_VALID_CURRENCY_ERROR)
        if not newV is None:
            self.setHasMaximum(True)
            self.allowInvalID = False
        self.maximum = newV

    def getMaximum(self):
        return self.maximum

    def setHasMinimum(self, val):
        if not Utils.isBoolean(val):
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_BOOLEAN_ERROR)
        self.hasMinimum = val

    def hasMinimum(self):
        return self.hasMinimum
    
    def setHasMaximum(self, newHasMaximum):
        self.hasMaximum = newHasMaximum

    def hasMaximum(self):
        return self.hasMaximum
    
    def getValueString(self):
        result = ""
        if not self.value is None:
            result = str(self.value)
        return result

    def equals(self, att):
        result = True
        if isinstance(att, CurrencyAttribute):
            if (att.hasMaximum != self.hasMaximum):
                result = False
            
            elif (att.hasMinimum != self.hasMinimum):
                result = False
            
            elif (att.maximum != self.maximum):
                result = False
            
            elif (att.minimum != self.minimum):
                result = False
            
            elif (att.getName() == None and self.getName() != None):
                result = False
            
            elif (att.getName() != None and self.getName() == None):
                result = False
            
            elif (att.getName() != None and self.getName() != None and att.getName() != self.getName()):
                result = False
            
            elif (att.value == None and self.value != None):
                result = False
            
            elif (att.value != None and self.value == None):
                result = False
            
            elif (att.value != None and self.value != None and att.value != self.value):
                result = False
            
            elif (att.isNullAllowed() != super().isNullAllowed()):
                result = False
            
        else:
            result = False
        
        return result


    def __str__(self):
        return "" + str(self.value)
    

class DateAttribute(Attribute):
    
    @staticmethod
    def stripTime(aDate):
        result = None
        if aDate:
            if isinstance(aDate, date):
                result = aDate
            elif isinstance(aDate, DT):
                result = aDate.date()
            elif isinstance(aDate, DateAttribute):
                result = aDate.gwtValue()
                if not result is None:
                    result = result.date()

    def __init__(
        self,
        name,
        allowInvalid=True,
        nullAllowed=True,
        value=None,
        duration = None,
        durationRequired = False):
        
        super().__init__(
            name=name,
            allowInvalid=allowInvalid,
            nullAllowed=nullAllowed)
        self.value = value
        self.duration = duration
        self.durationRequired = durationRequired
        
    def getValue(self):
        return self.value
    

    def setValue(self, newV):
        fmts = [
            '%Y-%m-%d %H:%M:%S',
            "%m %d %Y",  
            "%Y-%m-%d", 
            "%m-%d-%Y", 
            "%m.%d.%Y",  
            "%m\\%d\\%Y"
        ]
        oVal = self.value
        if newV is None or (isinstance(newV, str) and newV.strip() == ''):
            self.value = None
        elif isinstance(newV, DT):
            self.value = newV.date()
        elif isinstance(newV, date):
            self.value = newV
        else:
            ok = False
            for fmt in fmts:
                try :
                    self.value = DT.strptime(newV, fmt)
                    ok = True
                    super().allowInvalID = False
                    break
                except:
                    continue
            if not ok:
                raise InvalidAttributeValueException(AttributeMessageFactory.INVALID_TIME_ERROR)
            else:
                try:
                    self.validate()
                except InvalidAttributeValueException as e:
                    self.value = oVal
                    raise e   
    
    def getStartTime(self):
        return self.value
    
    def setStartTime(self, hour, mins, second):
        oVal = self.getValue()
        if oVal is None:
                self.setValue(DT.today())
        try:    
            self.value.val.replace(hour, mins, second, 0)
            self.validate()
        except InvalidAttributeValueException as e:
            self.value = oVal
            raise e   

    def validate(self):        
        result = True
        message = ''
        if self.getValue() is None and not super().isNullAllowed():
            message += ('\n' + AttributeMessageFactory.NoneError())
            result = False
        if self.duration is None:
            if self.isDurationRequired():            
                message += ('\n' + AttributeMessageFactory.NoneError())
                result = False
        elif self.duration < 0 and self.isDurationRequired():
            message += ('\n' + AttributeMessageFactory.negativeDurationError())
            result = False
        elif (self.duration == 0 and self.isDurationRequired()):
            message += ('\n' + AttributeMessageFactory.minimumValueError(0, 1))
            result = False
        if not result:
            raise InvalidAttributeValueException(message)

    def startsAfter(self, aDate):
        result = True
        end = self.self.getValue()
        if end is None:
            result = False
        else:
            end + timedelta(munutes=self.duration) # this objects end time
            if aDate is None:
                result = True
            elif isinstance(aDate, DT):
                result = end.after(aDate)
            elif isinstance(aDate, DateAttribute):
                d = aDate.getValue()
                if d is None:
                    result = True
                else:
                    result = end.after(d)
        return result 

  
    def endsBefore(self, aDate): 
        result = False
        if self.getValue() is None:
            if aDate != None:
                result = True            
        else: 
            if aDate != None and aDate.getValue() != None:
                end = self.self.getValue()
                end + timedelta(munutes=self.duration)
                if isinstance(aDate, DateAttribute):
                    result = end.before(aDate.getValue())
                elif isinstance(aDate, DT):
                    result = end.before(aDate)
        return result

    def spans(self, aDate):
        result = True
        if aDate is None or aDate.getValue() is None:
            result = False
        elif aDate.endsBefore(self) or aDate.startsAfter(self):
            result = False
        return result  
    
    def setDuration(self, newV):
        oldDur = newV
        oldVal = self.getValue()
        try:
            self.duration = newV
            if not newV is None and self.value is None:
                self.setValue(DT())
            self.validate()
        except InvalidAttributeValueException as e:
            self.duration = oldDur
            self.setValue(oldVal)
            if not super().allowInvalid():
                raise e
    
    def getDuration(self):
        return self.duration
    
    def isDurationRequired(self):
        return self.durationRequired
    
    def setDurationRequired(self, durationRequired):
        self.durationRequired = durationRequired

    def equals(self, att):
        result = True
        if isinstance(att, DateAttribute):
            if (att.getName() == None and self.getName() != None):
                result = False
            
            if (att.getName() != None and self.getName() == None):
                result = False
            
            if (att.getName() != None and self.getName() != None and att.getName() !=self.getName()):
                result = False
            
            if (att.value == None and self.value != None):
                result = False
            
            if (att.value != None and self.value == None):
                result = False
            
            if (att.value != None and self.value != None and att.value != self.value):
                result = False
            
            if (att.isNullAllowed() != super().isNAllowed()):
                result = False
            
            if (att.durationRequired != self.durationRequired):
                result = False
            
            if (att.duration != self.duration):
                result = False
        else:
            result = False
        return result

    def __str__(self):
        return "" + str(self.value)
    

class TimeAttribute(Attribute):
    VALUE_STRING_FORMAT = "%H:%M:%S"
    def __init__(
            self, 
            name, 
            allowInvalid=True, 
            nullAllowed=True, 
            value=None):
        super().__init__(
            name=name, 
            allowInvalid=allowInvalid, 
            nullAllowed=nullAllowed)
        self.value = None # need create instance attribute before accessing it
        self.setValue(value)

    def getValue(self):
        return self.value
    

     
    def setValue(self, txtV):
        try:
            oldV = self.value
        except:
            oldV = None
        if txtV is None:
            self.value = None
        elif not isinstance(txtV, str):
            raise InvalidAttributeValueException(AttributeMessageFactory.NOT_A_STRING_ERROR)
        else:
            self.value = time.strptime(txtV, TimeAttribute.VALUE_STRING_FORMAT)
        if not super().isAllowInvalid():
            try:
                self.validate()
            except InvalidAttributeValueException as e:
                self.value = oldV
                raise e
            
    def validate(self):
        if self.getValue() is None and not super().isnullAllowed():
            raise InvalidAttributeValueException(AttributeMessageFactory.NoneError())
        elif self.value is not None and not isinstance(self.value, time):
            raise InvalidAttributeValueException(AttributeMessageFactory.INVALID_TIME_ERROR)
                
    def getValueString(self):
        if self.value != None and not isinstance(self.value, time):
            raise InvalidAttributeValueException(AttributeMessageFactory.INVALID_TIME_ERROR)
        return DT.strftime(self.value, TimeAttribute.VALUE_STRING_FORMAT)
    
    def equals(self, att):
        result = True
        if isinstance(att, TimeAttribute):
            if (att.getName() == None and super().getName() != None):
                result = False
            
            elif (att.getName() != None and super().getName() == None):
                result = False
            
            elif (att.getName() != None and super().getName() != None and att.getName() != super().getName()):
                result = False
            
            elif (att.value == None and self.value != None):
                result = False
            
            elif (att.value != None and self.value == None):
                result = False
            
            elif (att.value != None and self.value != None and att.value != self.value):
                result = False
            
            elif (att.isnullAllowed() != super().isnullAllowed()):
                result = False            
        else:
            result = False
        if not result:
            raise InvalidAttributeValueException()
    
    def __str__(self):
        return self.getValueString()
    
     
class AttributeMessageFactory:
     
    None_ERROR = "None value not allowed."
    NEGATIVE_DURATION_ERROR = "Negative value not allowed for duration."
    NULL_STRING_ERROR = "Null string value not allowed."
    ALL_SPACES_ERROR = "Value must not be all spaces."
    NOT_NUMERIC_ERROR = "Value must be numeric."
    LEAD_TRAIL_SPACES_ERROR = "Value may not begin or end with a blank."
    TRAILING_SPACES_ERROR = "Value may not end with a blank."
    PRM_SEC_SELECTED_ERROR = "Primary and Secondary indicators have been selected."
    NO_IND_SEL_ERROR = "No option was selected."
    MUST_ENTER_DATE_ERROR = "Must enter "
    NO_FINAL_ACTION_ERROR = "Must have a final action assigned."
    NO_INVESTIGATOR_ASSIGNED_ERROR = "Must have an investigator assigned."
    NOT_ATTRIBUTE_ERROR = "Expected an Attribute - got :"
    NOT_BUSINESS_OBJECT_ERROR = "Expected a BusinessObject - got :"
    ATTRIBUTE_VALUE_ERROR = "InvalID Attribute Value"
    NOT_BOOLEAN_ERROR = 'value must be True or False'
    NOT_VALID_CURRENCY_ERROR = 'Not a valID Currency'
    INVALID_TIME_ERROR = 'Not a properly formatted time'
    NOT_A_STRING_ERROR = 'Not a string'
    
    @classmethod
    def NoneError(cls):
        return cls.None_ERROR
    
    @classmethod
    def negativeDurationError(cls):
        return cls.NEGATIVE_DURATION_ERROR

    @classmethod
    def firstLastNameError(cls, f, l):
        if f == None: 
            f = ""
        if l == None:
            l = ""
        msg =  'You must supply both last and first names.  You supplied ' + f + " " + l
        return msg
    
    @classmethod
    def nullStringError(cls):
        return cls.None_STRING_ERROR
    
    @classmethod
    def notAttributeError(cls, o):
        return cls.NOT_ATTRIBUTE_ERROR + " " + str(o) + "."
    
    @classmethod
    def notBusinessObjectError(cls, o):
        return cls.NOT_BUSINESS_OBJECT_ERROR + " " + str(o) + "."
    

    @classmethod
    def noFinalActionError(cls):
        return cls.NO_FINAL_ACTION_ERROR
    
    @classmethod
    def noInvestigatorAssignedError(cls):
        return cls.NO_INVESTIGATOR_ASSIGNED_ERROR
    

    @classmethod
    def mustEnterDateError(cls, text):
        return cls.MUST_ENTER_DATE_ERROR + " " + text + "."

    @classmethod
    def noIndicatorSelectedError(cls):
        return cls.NO_IND_SEL_ERROR
    
    @classmethod
    def primarySecondarySelectedError(cls):
        return cls.PRM_SEC_SELECTED_ERROR

    @classmethod
    def allSpacesError(cls):
        return cls.ALL_SPACES_ERROR
    
    
    @classmethod 
    def attributeError(cls):
        return cls.ATTRIBUTE_VALUE_ERROR
        
    @classmethod 
    def notNumericError(cls, s):
        return cls.NOT_NUMERIC_ERROR + ' You specified "' + s +'"'
    

    @classmethod
    def leadTrailSpacesError(cls):
        return cls.LEAD_TRAIL_SPACES_ERROR

    @classmethod
    def trailingSpacesError(cls):
        return cls.TRAILING_SPACES_ERROR
    
    @staticmethod
    def dateFormatError(text):
        return "The string, \"" + str(text) + "\" cannot be converted to a date"
    

    @staticmethod
    def timeFormatError(text):
        return "The string, \"" + str(text) + "\" cannot be converted to a time"
        
    

    @staticmethod
    def maximumLengthError(length, maxVal):
        s = "Length " + str(length) + " is larger than maximum allowable length " + str(maxVal) + "."
        return s
    
    @staticmethod
    def minimumLengthError(length, minVal):
        s = "Length " + str(length) +  " is less than minimum allowable length " + str(minVal) + "."
        return s
    
    @staticmethod
    def mixedCaseError(txt):
        s = str(txt) + " is mixed case."
        return s
    

    @staticmethod
    def notAllUpperCaseError(s):
        s2 = "String \"" + s + "\" contains lower case characters. Upper case is required."
        return s2
    

    @staticmethod
    def maximumValueError(val, maxVal):
        s2 = "Value " + str(val)+ " is larger than maximum allowable value " + str(maxVal) + "."
        return s2

    @staticmethod
    def minimumValueError(val, minVal):
        s2 = "Value " + str(val) + " is less than minimum allowable value " + str(minVal) + "."
        return s2
    
    @staticmethod
    def invalidCurrencyError(val):
        s = "Value " + str(val) + " is invalID for currency."
        return s

    @staticmethod
    def minMaxError(minval, maxval):
        return "Minimum value " + str(minval) + " is greater than maxumum value " + str(maxval) + "."


class InvalidAttributeValueException(Exception):
    def __init__(self, msg="", attr=None, exc=None):
        super().__init__(msg, exc)
        self.attribute = attr
        self.cause = exc
        self.msg = msg
    
    def getMsg(self):
        return self.msg
  

    def setAttribute(self, newAttribute):
        self.attribute = newAttribute
  

    def getAttribute(self):
        return self.attribute


class InvalidArgumentException(Exception):
    def __init__(self,msg=None, exc=None):
        
        super().__init__(msg, exc)