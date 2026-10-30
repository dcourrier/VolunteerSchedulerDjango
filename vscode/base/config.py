from abc import ABC,abstractmethod
from xml.dom.minidom import *
from xml.dom import Node

from vscode.base.base import VSBase
from vscode.utils.exceptions import *

class ConfigNode(ABC):

    @abstractmethod
    def getAttributeIterator(self):
        pass

    @abstractmethod
    def getElementIterator(self):
        pass

    @abstractmethod
    def getElementType(self):
        pass

        pass

    @abstractmethod
    def getValue(self):
        pass

    @abstractmethod
    def init(self):
        pass
  
    @abstractmethod  
    def size(self):
        pass

    @abstractmethod
    def getChildElement(self, index):
        pass


class ConfigNodeElementIterator(VSBase):

    def __init__(self, node):
        super().__init__()
        self.current = -1
        self.parent = node
        self.elements = node.childNodes

    def hasNext(self):
        result = True
        if self.current >= len(self.elements):
            result = False
        else:
            nt = self.elements.item(self.current).nodeType
            match nt:
                case Node.NOTATION_NODE:
                    self.parent.removeChild(self.lements.item(self.current))
                    result = self.hasNext()
                case Node.COMMENT_NODE:
                    self.parent.removeChild(self.lements.item(self.current))
                    result = self.hasNext()
                case Node.TEXT_NODE:
                    self.parent.removeChild(self.lements.item(self.current))
                    result = self.hasNext()
                case _:
                    pass
        return result

    def next(self):
        result = None
        if self.hasNext():
            result = ConfigNodeImpl(self.elements.item(self.current))
            self.current += 1
        return result 

    def remove(self):
        if self.current < 0:
            raise IllegalStateException("remove was called before next()")
        self.parent.removeChild(self.elements.item(self.current - 1))


class ConfigNodeImpl(ConfigNode):

    def __init__(self, node=None):
        super().__init__()
        self.idElements = {}
        self.impl = None
        self.nodeID = None
    
    def getImpl(self):
        result = None
        if self.nodeID:
            result = self.idElements.get(self.nodeID) 
        else: 
            result = self.impl
        return result
    
    def setImpl(self, node):
        match node.getNodeType():
            case xml.dom.Node.ELEMENT_NODE:
                self._processNode(node)
            case xml.dom.Node.DOCUMENT_NODE:
                self._processNode(node)
            case xml.dom.Node.DOCUMENT_TYPE_NODE: 
                self._processNode(node)
            case xml.dom.Node.ATTRIBUTE_NODE:
                self.impl = node
            case _:
                raise NoSuchElementException(node.getNodeName() + " " + node.getNodeType())
    
    def _processNode(self, node):
        if node.getNodeName().lower() == "use":
            nodeID = node.attributes.getNamedItem("objectID").nodeValue
        else:
            nid = None
            if node.getAttributes() and node.getAttributes().getNamedItem("id"):
                nid = node.getAttributes().getNamedItem("id")
                self.nodeID = nid.nodeValue
                self.idElements[nodeID] = node
            else:
                self.impl = node

    def getAttributeIterator(self):
        return ConfigNodeAttributeIterator(self.getImpl())

    def getElementIterator(self):
        return ConfigNodeElementIterator(self.getImpl())

    def getElementType(self):
        return self.getImpl().nodeType

    def getValue(self):
        result = ''
        if self.getImpl().getNodeType() == xml.dom.Node.ATTRIBUTE_NODE:
            result = self.getImpl().getValue()
        return result
            
    def getChildElement(self, index):
        result = None
        if not self.isElementContainer(self.impl):
            raise ConfigNodeNotElementException(str(self.impl) + ' is not an element container')
        
        nl = self.impl.childNodes
        if index > (len(nl) - 1):
            raise ConfigIndexOutOfBoundsException()
        count = 0
        for node in nl:
            if self.isElement(node):
                count += 1
            if count == (index + 1):
                result = ConfigNodeImpl(node)
                break
        return result

    def size(self):
        result = 0
        if not self.isElementContainer(self.impl):
            raise ConfigNodeNotElementException(str(self.impl) + ' is not an element container')
        nl = self.impl.getChildNodes()
        for node in nl:
            if self.isElement(node):
                result += 1
        return result
    
    def isElement(self, node):
        result = False
        if node:            
            if xml.dom.Node.ELEMENT_NODE == node.nodeType:
                result = True
        return result

    def isElementContainer(self, node):
        result = False
        if node:
            if self.isElement(node):
                result = True
            elif xml.dom.Node.DOCUMENT_NODE == node.nodeType:
                result = True
            elif xml.dom.Node.DOCUMENT_FRAGMENT_NODE == node.nodeType:                
                result = True
        return result


class ConfigNodeAttributeIterator(VSBase):

    def __init__(self, node=None):
        self.current = -1
        self.attributes = None
        self.node = node
        if node:
            self.attributes = node.getAttributes()

    def hasNext(self):
        if not self.attributes:
            return False
        else:
            return self.current < (self.attributes.length - 1)

    def next(self):
        result = None
        if self.hasNext():
            self.current += 1 
            result = ConfigNodeImpl(self.attributes.item(self.current))
        return result

    def remove(self):
        if self.current < 0:
            raise IllegalStateException("remove was called before next()")
        self.attributes.removeNamedItem(self.attributes.item(self.current - 1).getNodeName())


class ConfigurationBasedFactory(VSBase):

    def __init__(self):
        super().__init__()
        self.argumentTypes = {'ConfigNode': ConfigNode.__class__,
                     'IntCriterion': IntCriterion.__class__,
                     'IntCriteriaSet' : IntCriteriaSet.__class__}
        
    def createObject(self, node):
        meth = self.findConfigMethod(self, "create", node.getElementType(),\
                self.argumentTypes.get("ConfigNode"))
        obj = self.invokeConfigMethod(self, meth, node)
        return obj
'''
    def createChildElements(self, node, obj):
        for (Iterator it = node.getElementIterator() it.hasNext()) {
            boolean found = false
            Object arg = createObject((ConfigNode) (it.next()))
            Class argType = arg.getClass()
            String argTypeName = argType.getName()
            for (Iterator<String> iter = argumentTypes.keySet().iterator() iter.hasNext()) {
                String myKey = iter.next()
                Class<?> cur = argumentTypes.get(myKey)
                if (cur.isAssignableFrom(Class.forName(argTypeName))) {
                    callConfigMethod(obj, "add", myKey, cur, arg)
                    found = true
                    break
                }
            }
            if (!found) {
                String property = argTypeName
                while (true) {
                    int i = property.indexOf(".")
                    if (i == -1) {
                        break
                    } else if (i == property.length()) {
                        property = property.substring(0, property.length() - 1)
                        break
                    } else {
                        property = property.substring(i + 1)
                    }
                }
                raise Exception(
                        "Need to add Base Class in Factory for property "
                        + obj.getClass().getName() + ".add" + property
                        + "(" + property + ")")
            }
        }
    }

    private void setAttributes(ConfigNode node, Object obj) throws Exception {
        for (Iterator it = node.getAttributeIterator() it.hasNext()) {
            ConfigNode n = (ConfigNode) (it.next())
            callConfigMethod(obj, "set", n.getElementType(),
                    argumentTypes.get("String"), n.getValue())
        }
    }

    private Object callConfigMethod(Object methodOwner, String methodType,
            String property, Class argType, Object arg) throws Exception {
        try {
            Method m = findConfigMethod(methodOwner, methodType, property,
                    argType)
            return invokeConfigMethod(methodOwner, m, arg)
        } catch (NoSuchMethodException e) {
            String methodName = methodType
                    + property.substring(0, 1).toUpperCase()
                    + property.substring(1)
            raise Exception("could not find method "
                    + methodOwner.getClass().getName() + "." + methodName
                    + "()")
        }
    }

    private Method findConfigMethod(Object methodOwner, String methodType,
            String property, Class argType) throws NoSuchMethodException {
        Class[] argTypes = new Class[1]
        argTypes[0] = argType
        String methodName = methodType
                + property.substring(0, 1).toUpperCase()
                + property.substring(1)
        return methodOwner.getClass().getMethod(methodName, argTypes)
    }

    def invokeConfigMethod(self, obj, meth, arg):
        try:
            if hasattr(obj, meth):
            

    def setFileName(self, newFileName):
        self.fileName = newFileName
        
    def getFileName(self):
        return self.fileName

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name
    '''    

class XMLConfiguration(ConfigNodeImpl):
    
    def __init__(self, fileName=None, string=None,document=None):
        super().__init__()
        if fileName:
            document = parse(fileName)
            super().setImpl(document)
            super().init()
        elif string:
            document = parseString(string)
            super().setImpl(document)
            super().init()
        elif document:
            super().setImpl(document)
            super().init()