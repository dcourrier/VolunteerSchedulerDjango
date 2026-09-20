from django.test import TestCase
from datetime import datetime as DT,timedelta,time
from vscode.loader.loaders import *
from vscode.base.base import *
from vscode.base.business_objects  import *
from vscode.comparator.comp import *
from vs.models import *

class VolunteerSchedulerComparatorTests(TestCase): 
 

    def testActivityComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Activity()
            o2 = Activity()
            lst.append(o1)
            lst.append(o2)
            o1.setDescription('o2')
            o2.setDescription('o1')
            Collections.sort(lst, comparator=ActivityComparator()) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'
        assert lst[0].getDescription() == 'o1', 'not sortrd'
'''
    def testAvailabilityComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Availability()
            o2 = Availability()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testComparatorFactory(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = ComparatorFactory()
            o2 = ComparatorFactory()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testConfigurablePropertyComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = ConfigurableProperty()
            o2 = ConfigurableProperty()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testDefaultComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Default()
            o2 = Default()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testHouseholdComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Household()
            o2 = Household()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testJobAssignmentComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = JobAssignment()
            o2 = JobAssignment()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testJobComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Job()
            o2 = Job()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testLocationComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Location()
            o2 = Location()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testLoginComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Login()
            o2 = Login()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testLoginImplComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = LoginImpl()
            o2 = LoginImpl()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testLoginStatusComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = LoginStatus()
            o2 = LoginStatus()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testOrganizationComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Organization()
            o2 = Organization()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testPrivilegeComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Privilege()
            o2 = Privilege()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testProjectComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Project()
            o2 = Project()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testRecurrenceTypeComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = RecurrenceType()
            o2 = RecurrenceType()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testRelationshipComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Relationship()
            o2 = Relationship()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testRelationshipTypeComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = RelationshipType()
            o2 = RelationshipType()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testReportComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Report()
            o2 = Report()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testResourceAvailabilityComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = ResourceAvailability()
            o2 = ResourceAvailability()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testResourceComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Resource()
            o2 = Resource()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testScheduleComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Schedule()
            o2 = Schedule()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testScheduleEventComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = ScheduleEvent()
            o2 = ScheduleEvent()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testSecurityGroupComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = SecurityGroup()
            o2 = SecurityGroup()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testSkillComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Skill()
            o2 = Skill()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testTaskComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Task()
            o2 = Task()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testTaskComparator1(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = TaskComparator1()
            o2 = TaskComparator1()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testTeamComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Team()
            o2 = Team()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testVolunteerComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = Volunteer()
            o2 = Volunteer()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

    def testVolunteerSkillComparator(self):
        lm = LoaderManager()
        lm.load()
        err = None
        lst = []
        try:
            o1 = VolunteerSkill()
            o2 = VolunteerSkill()
            lst.append(o1)
            lst.append(o2)
            Collections.sort(lst) 
        except Exception as e:
            err = e
            logger.opt(exception=True).debug(err)
        assert not err, 'Got an exception'

'''