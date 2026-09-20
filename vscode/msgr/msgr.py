from abc import ABC
from datetime import datetime as DT
from enum import Enum

from vscode.utils.exceptions import NoSuchElementException 
from vscode.utils.utils import Utils
from vscode.att.attribute import InvalidArgumentException

class MessageSeverity(Enum):
    INFORMATION = 1
    WARNING = 2
    RECOVERABLE = 3
    FATAL = 4

class MessageType(Enum):
    ERROR = 1
    TRACE = 2

class LogicOperator(Enum):
    UNDEFINED =1
    IN = 2
    NOTIN = 3
    LT = 4 
    LE = 5
    EQ = 6
    NE = 7
    GE = 8
    GT = 9
    AND = 10
    NAND = 11
    OR = 12
    NOR = 13

class MessageUtils(ABC):
    @staticmethod
    def getOperator(op):
        try:
            return LogicOperator.valueOf(op)
        except Exception:
            raise NoSuchElementException("No such operator \"" + op +"\"")

    @staticmethod
    def isSupported(op, supportedOps):
        result = False
        for lo in supportedOps:
            if lo.equals(op):
                result = True
                break
        return result
    
class Message(ABC):
    
    def __init__(self, 
                 messageType=MessageType.ERROR,
                 severity=MessageSeverity.WARNING,
                 text='',
                 method=None,
                 className=None):
        self.children = []
        self.severity = severity 
        self.text = text
        self.messageType = messageType 
        self.method = method
        self.className = className 
        self.timeStamp = DT.now()

    def areEqual(self, m1, m2):
        result = False
        if not m1 and not m2:
            result = True
        elif m1 and m2:
            result = self.areChildrenEqual(m1, m2)
            if result == True:
                result = self.compareFields(m1, m2)
        return result
    
    def compareFields(self, m1, m2):
        result = True
        if not m1.getDate() != m2.getDate():
            result = False
        elif m1.getClassName() != m2.getClassName():
            result = False
        elif m1.getMethod() != m2.getMethod():
            result = False
        elif m1.getSeverity() != m2.getSeverity():
            result = False
        elif m1.getMessageType() != m2.getMessageType():
            result = False
        elif not Utils.equals(m1.getText(), m2.getText()):
            result = False
        return result
    
    def areChildrenEqual(self, m1, m2):
        result = True
        if Utils.isNull(m1, m2):
            result = Utils.compareNull(m1, m2)
        else:
            v1 = m1.getChildren()
            v2 = m2.getChildren()
            if Utils.isNull(v1,v2):
                result = Utils.compareNull(v1, v2)
            else:
                if len(v1) != len(v2):
                    result = False
                else:
                    for loop, msg1 in enumerate(v1):
                        msg2 = v2.get(loop)
                        result = self.areEqual(msg1,msg2)
                        if not result:
                            break
            return result
  
    def addMessage(self, msg):
        if msg:
            self.getChildren().append(msg)

    def getChildren(self, includeDescendents=False):
        result = []
        if not includeDescendents:
            result = self.children
        else:
            if self.hasChildren():
                for child in self.getChildren():
                    result.append(child)
                    for c in child.getChildren(True):
                        result.append(c)
        return result
    
    def hasChildren(self):
        return len(self.children) > 0
    
    def __str__(self):
        return self.toString()
    
    def toString(self):
        s = self.__class__.__name__
        s += "::"
        s += str(self.getMethod())
        s += ":"
        s += self.getText()
        s += " Type:"
        s += str(self.getMessageType())
        s += " severity:"
        s += str(self.getSeverity())
        s += "\n"
        for o in self.getChildren(True):
            s += o.toString()
            s += "\n"       
        return s
  
    def getSeverity(self):
        return self.severity
    
    def setSeverity(self, newSeverity):
        if not newSeverity or isinstance(newSeverity, MessageSeverity):
            self.severity = newSeverity
        else:
            raise InvalidArgumentException('severity not a MessageSeverity obbject or null')
    
    def setText(self, newText):
        self.text = newText
    
    def getText(self):
        return self.text
    
    def equalTo(self, m):
        return self.areEqual(self, m)
    
    def setClassName(self, newFileName):
        self.className = newFileName
        
    def getClassName(self):
        return self.className
    
    def getDate(self):
        return self.getTimeStamp().strftime('%m/%d/%Y')
    
    def getTime(self):
        return self.getTimeStamp().strftime('%H:%M:%S')
    
    def setTimeStamp(self, newTimeStamp):
        self.timeStamp = newTimeStamp
    
    def getTimeStamp(self):
        return self.timeStamp
    
    def setMessageType(self, newType):
        self.messageType = newType
        
    def getMessageType(self):
        return self.messageType
    
    def setMethod(self, newMethod):
        self.method = newMethod
    
    def getMethod(self):
        return self.method
    