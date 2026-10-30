from abc import ABC,abstractmethod
from datetime import datetime as DT
from enum import Enum
from pydispatch import dispatcher
import threading

from vscode.base.base import VSBase
from vscode.base.config import ConfigurationBasedFactory
from vscode.utils.exceptions import NoSuchElementException,MessageCarryingException 
from vscode.utils.utils import Utils
from vscode.att.attribute import InvalidArgumentException

class Value(VSBase):
    
    def __init__(self, val=None):
        super.__init__()
        self.value = val
        
    def getValue(self):
        return self.value
    
    def setValue(self, val):
        self.value = val


class MessageFilter(ABC):
    @abstractmethod
    def canPass(self, message):
        pass
    
    
class DefaultFilter(MessageFilter):

    def __init__(self, rtn=True):
        super().__init__()
        self.returnCode = rtn
        
    def canPass(self, msg):
        return self.returnCode
    

class MessageSeverity(Enum):
    INFORMATION = 1
    WARNING = 2
    RECOVERABLE = 3
    FATAL = 4


class MessageType(Enum):
    ERROR = 1
    TRACE = 2


class Criteria(ABC):

    @abstractmethod
    def canPass(self, MessageType=None, MessageSeverity=None):
        pass


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


class FilterSetConstants(ABC):
    supportedOps = [
        LogicOperator.AND,
        LogicOperator.NAND,
        LogicOperator.OR,
        LogicOperator.NOR
    ]

    
class CriteriaSet(Criteria, FilterSetConstants):
    
    def __init__(self):
        super().__init__()
        self.criteria = []
        self.operation = LogicOperator.UNDEFINED

    def canPassType(self, msgtype):
        for c in self.criteria:
            passed = c.canPass(msgtype)
            match self.operation:
                case LogicOperator.AND:
                    if not passed:
                        return False
                case LogicOperator.NAND:
                    if not passed:
                        return True
                case LogicOperator.OR:
                    if passed:
                        return True
                case LogicOperator.NOR:
                    if passed:
                        return False
                case _:
                    break
        match self.operation:
            case LogicOperator.AND:
                return True
            case LogicOperator.NAND:
                return False
            case LogicOperator.OR:
                return False
            case LogicOperator.NOR:
                return True
            case _:
                return False

    def canPassSeverity(self, ms):
        for c in self.critera:
            passed = c.canPass(ms)
            match self.operation:
                case LogicOperator.AND:
                    if not passed:
                        return False
                    else:
                        break
                case LogicOperator.NAND:
                    if not passed:
                        return True
                    else:
                        break
                case LogicOperator.OR:
                    if passed:
                        return True
                    else:
                        break
                case LogicOperator.NOR:
                    if passed:
                        return False
                    else:
                        break                    
                case _:
                    break
        match self.operation:
            case LogicOperator.AND:
                return True
            case LogicOperator.NAND:
                return False
            case LogicOperator.OR:
                return False
            case LogicOperator.NOR:
                return True
            case _:
                return False
       
    def setOperator(self, op):
        lo = MessageUtils.getOperator(op)
        if MessageUtils.isSupported(lo, self.supportedOps):
            self.operation = lo
        else:
            raise NoSuchElementException("Criteron does not allow opeator \"" + op + "\"")
        
    def addCriteria(self, crit):
        self.criteria.extend(crit)
    
    def addCriterion(self, crit):
        self.criteria.append(crit)


class IntCriteriaSet(CriteriaSet):

    def __init__(self):
        super().__init__()


class MessageReceiver(ABC):
    
    @abstractmethod
    def isStopped(self):
        pass
      
    @abstractmethod
    def getName(self):
        pass
  
    @abstractmethod
    def setName(self, name):
        pass
  
    @abstractmethod
    def post(self, message):
        pass
  
    @abstractmethod
    def stop(self):
        pass
  
    @abstractmethod
    def restart(self):
        pass
 
 
class Messenger(MessageReceiver):
    
    @abstractmethod
    def post(self, mtype=None, severity=None, text=None, exc=None):
        pass

    @abstractmethod
    def getMessage(self, mtype, severity, text):
        pass


class MessageListener(ABC):# extends PropertyChangeListener
    
    @abstractmethod
    def initialize(self,node=None):
        pass
    
    @abstractmethod
    def stop(self):
        pass
     
    @abstractmethod
    def restart(self):
        pass

    
class MessageSource(ABC):

    @abstractmethod
    def addPropertyChangeListener(self, listener):
        pass
 
    @abstractmethod
    def hasMoreMessages(self):
        pass
    
    @abstractmethod
    def getNextMessage(self):
        pass

   
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
    
    
class Criterion(Criteria):
    supportedOps = [
        LogicOperator.IN,
        LogicOperator.NOTIN,
        LogicOperator.LT,
        LogicOperator.LE,
        LogicOperator.EQ,
        LogicOperator.NE,
        LogicOperator.GE,
        LogicOperator.GT
    ]
    
    def __init__(self):
        super().__init__()
        self.operation = LogicOperator.UNDEFINED
        self.value = None
        self.values = []
    
    def canPass(self, msgtype=None, msgSeverity=None):
        result = True
        if msgtype:
            result = self.canPassInt(msgtype.value)
        elif msgSeverity:
            result = self.canPassInt(msgSeverity.value)
        return result
        
    def canPassInt(self, i):
        result = False
        if i:
            match self.operation:
                case LogicOperator.IN:
                    result = i in self.values
                case LogicOperator.NOTIN:
                    result = not i in self.values
                case LogicOperator.LT:
                    if self.value:
                        result = (i < self.value)
                case LogicOperator.LE:
                    if self.value:
                        result = (i <= self.value)
                case LogicOperator.GT:
                    if self.value:
                        result = (i > self.value)
                case LogicOperator.GE:
                    if self.value:
                        result = (i >= self.value)
                case LogicOperator.EQ:
                    if self.value:
                        result = (i == self.value)
                case LogicOperator.NE:
                    if self.value:
                        result = (i != self.value)
                case _:
                    result = False
        return result
    
    def setOperator(self, op):
        lo = MessageUtils.getOperator(op)
        if MessageUtils.isSupported(lo, Criterion.supportedOps):
            self.operation = lo
        else:
            raise NoSuchElementException("Criteron does not allow opeator \"" + op + "\"")
          
    def setValue(self, val):
        if self.operation in [LogicOperator.IN,LogicOperator.NOTIN]:
            done = False
            delimiter = ' '
            index = 0
            v = val
            while not done:
                v = v.strip()
                index = v.find(delimiter)
                if index == -1:
                    self.values.append(int(v))
                    done = True
                else:
                    self.values.append(int(v[0:index]))
                    v = v[index:]
        else:
            self.value = int(v)

    def addValue(self, intval=None, value=None):
        val = None
        if value and isinstance(value, Value):
            val = value.getValue()
        elif intval and isinstance(intval,int):
            val = intval
        try:
            mt = MessageType[val]
            i = int(mt.value)
            self.values.append(i)
            self.value = i
        except:
            try:
                ms = MessageSeverity.valueOf(val)
                i = int(ms.ordinal())
                self.values.append(i)
                self.value = i
            except Exception as e:
                super().handleException(e)


class IntCriterion(Criterion):

    def __init__(self):
        super().__init()

    
class Message(VSBase):
    
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
   
    
class StopMessage(Message):
    
    def __init__(self):
        super().__init__()
  
  
class MessageRouter(MessageListener):
    
    def __init__(self, name):
        super().__init__()
        self.receivers = []
        self.name = None
        self.stopped = False
        self.name = name + ".Router"

    @abstractmethod
    def initialize(self, node):
        pass

    def propertyChange(self, evt):
        if evt:
            s = evt.getNewValue()
            if s:
                while s.hasMoreMessages():
                    m = s.getNextMessage()
                    if isinstance(m, StopMessage):
                        self.stop()
                    elif isinstance(m,RestartMessage):
                        self.restart()
                    else:
                        if not self.isStopped():
                            for r in self.getReceivers():
                                r.post(m)
        
    def stop(self):
        for mr in self.getReceivers():
            mr.stop()
        self.setStopped(True)
   
    def restart(self):
        if self.isStopped():
            for mr in self.getReceivers():
                mr.restart()
        self.setStopped(False)
        
    def  getName(self):
        return self.name

    def addReceiver(self, r):
        self.getReceivers().append(r) 
        
    def getReceivers(self):
        return self.receivers
    
    def setStopped(self, newStopped):
        self.stopped = newStopped
    
    def isStopped(self):
        return self.stopped
    
    
class StandardMessageRouter(MessageRouter):
    
    def __init__(self, name):
        super().__init__(name)
    
    def initialize(self, node=None):
        pass
 
   
class RestartMessage(Message):
    
    def __init__(self):
        super().__init__()
     
  
class PostOffice(MessageReceiver):

    def __init__(self, name,  queue, router):
        super().__init__()
        self.inputQueue = queue
        self.name = name
        self.router = router
        self.stopped = False
        self.inputQueue.addPropertyChangeListener(router)   

    def addListenerQueue(self, q):
        self.getRouter().addReceiver(q)
        
    def setName(self, newName):
        self.name = newName
    
    def getName(self):
        return self.name
    
    def stop(self):
        self.getInputQueue().stop()
        self.stopped = True

    def restart(self):
        if self.stopped:
            self.stopped = False
            self.getInputQueue().restart()
        
    
    def getRouter(self):
        return self.router
    
    def post(self, msg):
        if not self.isStopped():
            self.getInputQueue().post(msg)
        
    def getInputQueue(self):
        return self.inputQueue
    
    def isStopped(self):
        return self.stopped
    
    
class DummyPostOffice(PostOffice):

    def __init__(self):
        super().__init__()
        
    def post(self, msg):
        pass

class MessageFieldFilter(MessageFilter):
    
    VALID_FIELD_NAMES ="category", "severity"

    def __init__(self):
        super().__init()
        self.criteria = None
        self.messageAttrGetter = None
    
    def canPass(self, message):
        result = False
        if message != None and self.messageAttrGetter:
            methodResult = None
            try:
                methodResult = self.messageAttrGetter(message)
                if isinstance(methodResult, MessageSeverity):
                    if not self.criteria:
                        result = True
                    else:
                        result = self.criteria.canPass(methodResult)
                elif isinstance(methodResult, MessageType):
                    if not self.criteria:
                        result = True
                    else:
                        result = self.criteria.canPass(methodResult)
            except AttributeError:
                messClass = message.__class__.__name__
                print(str(self.messageAttrGetter.__name__) + " is not in " + messClass + ".")
            except:
                print("Could not access Target object of type Message.")
        return result
   
    def setFieldName(self, fieldName):
        try:            
            cls = None
            self.messageAttrGetter = Message.getattr(
                    "get" +fieldName[0:1].upper() + fieldName[1:])
        except AttributeError:
            raise Exception("could not find method Message.get" + fieldName[0:1].upper() + fieldName[1:]+ "()")
        
    def addCriteria(self, crit):
        self.criteria = crit
    
    def addCriterion(self, crit):
        self.criteria = crit
        
    def addCriteriaSet(self, critset):
        self.addCriteria(critset)


class MessageFilterSet(MessageFilter, FilterSetConstants):

    def __init__(self):
        super().__init__()
        self.operation = LogicOperator.UNDEFINED
        self.filters = []
        self.ID = None
    
    def canPass(self, message):
        result = True
        if len(self.filters) > 0 and message:
            for f in self.filters:
                passed = f.canPass(message)
                match self.operation:
                    case LogicOperator.AND:
                        if not passed:
                            return False
                        else:
                            break
                    case LogicOperator.NAND:
                        if not passed:
                            return True
                        else:
                            break
                    case LogicOperator.OR:
                        if passed:
                            return True
                        else:
                            break
                    case LogicOperator.NOR:
                        if passed:
                            return False
                        else:
                            break
                    case _:
                         break
            match self.operation:
                case LogicOperator.AND:
                    result = True
                case LogicOperator.NAND:
                    result = False
                case LogicOperator.OR:
                    result = False
                case LogicOperator.NOR:
                    result = True
                case _:
                    result = False
        return result
    
    def setId(self, newID):
        self.ID = newID
    
    def getId(self):
        return self.ID
    
    def setOperator(self, op):
        lo = MessageUtils.getOperator(op)
        if MessageUtils.isSupported(lo, self.supportedOps):
            self.operation = lo
        else:
            raise NoSuchElementException("Criteron does not allow opeator \"" + op + "\"")
        
    def addMessageFilter(self, filt):
        if filt:
            self.filters.append(filt)
        
    def addMessageFilterSet(self, filt):
        if filt:
            self.addMessageFilter(filt)
        
    def addMessageFieldFilter(self, filt):
        self.addMessageFilter(filt)
    
    def getChildSets(self):
        result = []
        for obj in self.filters:
            if isinstance(obj,MessageFilterSet, obj):
                result.append(obj)
        return result
    

    def addChildSets(self, setlist):
        for obj in self.filters:
            if isinstance(obj,MessageFilterSet, obj):
                setlist.append(obj)
                obj.addChildSets(list)

    
class MessengerImpl(Messenger):

    def __init__(self, recvr=None, name=None):
        super().__init__()
        self.receiver = recvr
        self.name = name
        self.stopped = False
   
    def getMessage(self, mtype, severity, text):
        return Message(mtype, severity, text)
    
    def post(self, mtype=None, severity=None, text=None, msg=None, err=None):
        if err:
            if isinstance(err,MessageCarryingException) and err.getMsg():
                self.getReceiver().post(err.getMsg())
        elif not msg and mtype and severity and text:
            self.getReceiver().post(Message(mtype, severity, text))
        elif msg:
            if not self.isStopped():
                if isinstance(msg,StopMessage):
                    self.stop()                
                self.getReceiver().post(msg)
            else:
                if isinstance(msg, RestartMessage):
                    self.restart()
                    self.getReceiver().post(msg)
   
    def restart(self):
        self.setStopped(False)
    
    def setName(self, newName):
        self.name = newName

    def getName(self):
        return self.name    

    def stop(self):
        self.setStopped(True)
    
    def isStopped(self):
        return self.stopped

    def setStopped(self, stopped):
        self.stopped = stopped

    def getReceiver(self):
        return self.receiver
 
 
class MessageFilterFactory(ConfigurationBasedFactory):
    
    def __init__(self):
        super().__init__()
        super().argumentTypes = {}
        super().argumentTypes['MessageFilter']=MessageFilter.__class__
        super().argumentTypes['Criteria']=Criteria.__class__
        super().argumentTypes['MessageFilterSet']=MessageFilterSet.__class__
        super().argumentTypes['MessageFieldFilter']=MessageFieldFilter.__class__
        super().argumentTypes['CriteriaSet']=CriteriaSet.__class__
        super().argumentTypes['Criterion']=Criterion.__class__
        super().argumentTypes['Value']=Value.__class__

    def createMessageFilter(self, node):
        return super().createObject(node)
    
    def createFilterSet(self, node):
        mfs = super().createObject(node)
        setlist = fs.getChildSets()
        setlist.append(fs)
        return setlist
    
       