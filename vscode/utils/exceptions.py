class VSException(Exception):
    def __init__(self, msg=None, cause=None):
        if msg:
            super().__init__(msg)
            super().add_note(msg)
        else:
            super().__init__()
        self.cause = cause
        
    def getCause(self):
        return self.cause
 
class AccountDeletedException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class AccountExpiredException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
            
class AccountLockedException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class AssignmentDateException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class AvailabilityOverlapException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class ClassCastException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class ConfigElementNotSupportedException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class ConfigIndexOutOfBoundsException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class ConfigNodeException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class ConfigNodeNotElementException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
     
class DuplicateKeyException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class DuplicateLocationException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class DuplicateLoginException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class DuplicateOrganizationException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class EventDateScheduleDateConflictException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class EventInSameLocationException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class IllegalStateException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class InvalidArgumentException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class InvalidAttributeValueException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class InvalidDateException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class InvalidDateCombinationException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class InvalidPasswordException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class InvalidPasswordValueException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class InvalidRequestError(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)

class MessageCarryingException(VSException):
    
    def __init__(self, msg=None, text=None):
        super().__init__(text)
        self.msg = msg
    
    def getMsg(self):
        return self.msg
    
    def getAllMsgs(self):
        result = []
        m = self.getMsg()
        if m:
            result.append(m)
            result.addAll(m.getChildren(True))
        return result
    
    def __str__(self):
        sb = ''
        sb += str(self.getMessage())
        if self.msg:
            sb += "\n"
            sb += str(self.msg)
        return sb 
    
    def toHtmlString(self):
        sb = "<html>"
        sb += str(self.getMessage())
        if self.msg:
            sb += self.msg.toHtmlString()
        sb += "</html>"
        return sb
 
        
class MessageListenerInitializeException(VSException):
   
    def __init__(self, msg=None, cause=None):
        super().__init__(msg, cause)
 
class InvalidSecretException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class MissingArgumentException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class MissingParameterException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class NeedOrganizationException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class NoSuchElementException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class NoAvailableJobForVolunteerException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
             
class NotAStringException(VSException):
    def __init__(self, msg=None):
        super().__init__(msg)
    
class NoLoginFoundException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class NotFoundException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class NotUniqueException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class PasswordAlreadyUsedException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
  
class PersistenceException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
class RecurringEventBuilderException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class ReportDeleteException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class ResourceAvailabilityExceededException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class ResourceAvailabilityException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class ScheduleBuilderException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class SecurityManagerInitializeException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class StaleObjectException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class SystemOrganizationException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class ValidationException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class ValueTableKeyException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
