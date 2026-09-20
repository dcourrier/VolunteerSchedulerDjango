from abc import ABC
from datetime import datetime as DT
from vscode.utils.exceptions import InvalidArgumentException
from loguru import logger
from dateutil.relativedelta import relativedelta

logger.add("D:/tmp/PythonVolsched.log", backtrace=True, diagnose=True)

class VSBase(ABC):
    SPACE = '                                                                                                                        '
    DATE_FMT = '%b %d, %Y'
    DATE_FMT_SLASH = '%m/%d/%Y'
    TIME_FMT = '%H:%M'
    def __init__(self):
        pass

    def stringToBool(self,val):
        truthMapping = {
            "true": True, "yes": True, "t": True, "1": True, "on": True,
            "false": False, "no": False, "f": False, "0": False, "off": False
        }
        # Normalize the string to lowercase and strip whitespace
        cleanedVal = str(val).strip().lower()
        
        if cleanedVal in truthMapping:
            return truthMapping[cleanedVal]
        raise ValueError(f"Cannot convert '{val}' to a boolean.")
         
    def handleException(self, err):
        logger.opt(exception=True).debug(err)  
        
    def trace(self, msg, exception=None):
        if msg and isinstance(msg, str):
            logger.trace(msg)
            if exception:
                logger.opt(exception=True).trace(exception)
            
    def debug(self, msg, exception=None):
        if msg and isinstance(msg, str):
            logger.debug(msg)
            if exception:
                logger.opt(exception=True).debug(exception)
            
    def info(self, msg, exception=None):
        if msg and isinstance(msg, str):
            logger.info(msg)
            if exception:
                logger.opt(exception=True).info(exception)
            
    def warning(self, msg, exception=None):
        if msg and isinstance(msg, str):
            logger.warning(msg)
            if exception:
                logger.opt(exception=True).warning(exception)
            
    def error(self, msg, exception=None):
        if msg and isinstance(msg, str):
            logger.error(msg)
            if exception:
                logger.opt(exception=True).error(exception)
            
    def complain(self,msg):
        raise InvalidArgumentException(msg);
    
    def isBlank(self, txt):
        result = True 
        if txt and isinstance(txt, str) and len(txt.strip()) > 1:
            result = False
        return result
    
    def notBlank(self, txt):
        return not self.isBlank(txt)

    def now(self):
        return DT.now()
    
class BusinessObjectBase(VSBase):
    
    @staticmethod
    def validateAttributes(attList):
        from vscode.att.attribute import InvalidAttributeValueException
        result = True
        message = None
        for att in attList:
            try:
                att.validate()
            except InvalidAttributeValueException as e:
                message = ('\n' + att.getName() + ' : ' + e.getMsg())
                result = False
        if not result:
            raise InvalidAttributeValueException(msg=message, attr=att.name)
    
    def __init__(self):
        pass
    
    def setIdProperties(self, att):
        att.allowInvalID = False
        att.nullAllowed = True  # needed because database generates an ID when the object is inserted.
        att.hasMinimum = True
        att.minimum = 0
        
    def setTrackingAttributes(self,
        createUser,
        updateUser,
        createDate,
        updateDate):

        createUser.allowInvalID = False
        createUser.nullAllowed = False
        createUser.hasMinimum = True
        createUser.setMinimum = 0

        updateUser.allowInvalID = False
        updateUser.nullAllowed = False
        updateUser.hasMinimum = True
        updateUser.setMinimum = 0

        createDate.allowInvalID = False
        createDate.nullAllowed = False
        
        updateDate.allowInvalID = False
        updateDate.nullAllowed = False

    def now(self): 
        return DT.now()
    
class ObjectFactoryBase(ABC):
    
    def __init__(self):
        pass
