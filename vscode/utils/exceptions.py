class VSException(Exception):
    def __init__(self, msg=None):
        super().__init__()
        if msg:
            super().add_note(msg)
 
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
 
class InvalidArgumentException(VSException):

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
 
class InvalidSecretException(VSException):

    def __init__(self, msg=None):
        super().__init__(msg)
 
class MissingArgumentException(VSException):

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
 
