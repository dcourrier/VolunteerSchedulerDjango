from django.test import TestCase
from django.utils import timezone
from django.db import transaction
from datetime import datetime as DT
from vscode.base.base import *
from vscode.base.business_objects  import *
import vscode
from vscode.loader.loaders import LoaderManager
from vs.models import *
from loguru import logger

class VolunteerSchedulerTestDataLoaderTests(TestCase):
    databases = '__all__'
    
    def test_1(self):
        err = None
        try:
            DataLoader().load()
        except Exception as e:
            logger.opt(exception=True).debug(e)
            err = e
        assert not err, 'got an exception'
        


class DataLoader(VSBase):
    def __init__(self):
        pass
    
    def load(self):
        from vscode.base.business_objects import ObjectFactory,Password,Address,\
        Household,Volunteer,Relationship,Location,WorkAddress,Resource,Skill,\
        Location,EventRecurrence,ScheduleEvent,Job,EventJoinToResource,\
        VolunteerSkill,EventPreference,Availability,EventRecurrence
        from vs.models import DbAddress,DbHousehold,DbVolunteer,DbRelationship,\
        DbLocation,DbWorkAddress,DbResource,DbSkill,DbLocation,DbEventRecurrence,\
        DbScheduleEvent,DbJob,DbEventJoinToResource,DbVolunteerSkill,DbEventPreference,\
        DbAvailability,DbEventRecurrence
        LoaderManager().load()
        of = ObjectFactory()
        name = 'TestDataLoader'
        org = of.getOrganization(name='Volunteer Scheduler')
        if not org:
            org = of.createOrganization(name,1)
        org_id = org.getOrganizationID()
        #org.printDict() 
        li = of.createLogin(name,name+' ' + name,org,1)
        #org.printDict() 
        lid = li.getLoginID()
        assert lid,"didn't get login id"
        #print('org: ' + str(org) + ' ' +str(org.getOrganizationID()))
        #org.printDict() 
        #li.printDict()
        pwd = Password(myDb=DbPassword())
        pwd.setPassword("gronk")
        pwd.setPasswordCreateUser(lid)
        pwd.setPasswordUpdateUser(lid)
        pwd.setPasswordCreateDate(DT.now())
        pwd.setPasswordUpdateDate(DT.now())
        pwd.setLogin(li)
        pwd.save()
        pwd1 = of.getPassword(pwd.getPasswordID())
        assert pwd1, 'Failed to get any passwords'
        assert pwd1.getPasswordLoginID(), 'password missing login id'
        add = Address(DbAddress())
        add.setAddressCreateUser(lid)
        add.setAddressUpdateUser(lid)
        add.save()
        if not org.getOrganizationID() or not org.myDb or not org.myDb.organizationID:
            org = of.getOrganization(oid=org_id)
        hi1 = Household(myDb=DbHousehold())
        hi1.setAddress(add)
        hi1.setOrganization(org)
        hi1.setAddressLineTwo("Address Line Two")
        hi1.setCity("Any Town")
        hi1.setEmail("hitech@wonder.net")
        hi1.setFax("## fax ##")
        hi1.setMobilePhone("Cell #")
        hi1.setPager("Pager #")
        hi1.setPhone("phone #")
        hi1.setPostalCode("zip + 4")
        hi1.setState("MN")
        hi1.setStreet("123 Elm")
        hi1.setHouseholdFirstName("Tom")
        hi1.setHouseholdLastName("Jones")
        hi1.setHouseholdCreateUser(lid)
        hi1.setHouseholdUpdateUser(lid)
        hi1.toDb()
        if not org.getOrganizationID() or not org.myDb or not org.myDb.organizationID:
            org = of.getOrganization(oid=org_id)
        if not hi1.myDb.organization_id:
            hi1.myDb.organization_id = org_id
        hi1.save()
        assert hi1.getHouseholdID(), 'No householdID'
        assert hi1.getOrganization(), 'No household organization'
        #print('\nAfter\n')
        #hi1.printDict()
        assert hi1.getHouseholdOrganizationID(), 'No household oranization Id'
        assert hi1.myDb.address, 'No household myDb addresses'
        assert hi1.address, 'no household address'
        if not org.getOrganizationID():
            org = of.getOrganization(org_id)
        v = Volunteer(myDb=DbVolunteer())
        v.household = hi1
        v.setOrganization(org)
        v.setVolunteerFirstName("Tom")
        v.setVolunteerLastName("Jones")
        v.setVolunteerCreateUser(lid)
        v.setVolunteerUpdateUser(lid)
        v.save()
        add = Address(myDb=DbAddress())
        add.setAddressCreateUser(lid)
        add.setAddressUpdateUser(lid)
        add.setStreet("Will Smith")
        add.save()
        assert v.myDb.organization, 'No mv.myDb.orgaanization_id'
        hi2 = Household(myDb=DbHousehold())
        hi2.address= add
        hi2.setOrganization(org)
        hi2.setHouseholdFirstName("Will")
        hi2.setHouseholdLastName("Smith")
        hi2.setHouseholdCreateUser(lid)
        hi2.setHouseholdUpdateUser(lid)
        if not hi2.myDb.organization_id:
            hi2.setHouseholdOrganizationID(org_id)
            hi2.myDb.organization_id = org_id
            hi2.organization_id = org_id
        #hi2.printDict()
        hi2.save()
        #print('******   hi2.getHouseholdOrganizationID(): ' + str( hi2.getHouseholdOrganizationID()))
        #hi2.printDict()
        assert hi2.getHouseholdOrganizationID() == org_id, 'no hi2 organization id'
        v = Volunteer(myDb=DbVolunteer())
        v.household = hi2
        v.setOrganization(org)
        v.setVolunteerFirstName("Will")
        v.setVolunteerLastName("Smith")
        v.setVolunteerCreateUser(lid)
        v.setVolunteerUpdateUser(lid)
        v.save()
        assert v.organization, 'No volunteer organization'
        add = Address(myDb=DbAddress())
        add.setStreet("Booker T. Washington")
        add.setAddressCreateUser(lid)
        add.setAddressUpdateUser(lid)
        add.save()
        hi3 = Household(myDb=DbHousehold())
        hi3.address = add
        hi3.setOrganization(org)
        hi3.setHouseholdFirstName("Booker T.")
        hi3.setHouseholdLastName("Washington")
        hi3.setHouseholdCreateUser(lid)
        hi3.setHouseholdUpdateUser(lid)
        hi3.save()
        assert hi3.getHouseholdOrganizationID(), 'no hi3 organization id'
        v = Volunteer(myDb=DbVolunteer())
        v.household = hi3
        v.setOrganization(org)
        v.setVolunteerFirstName("Booker T.")
        v.setVolunteerLastName("Washington")
        v.setVolunteerCreateUser(lid)
        v.setVolunteerUpdateUser(lid)
        v.save()
        v = Volunteer(myDb=DbVolunteer())
        v.setHousehold(hi3)
        add = Address(myDb=DbAddress())
        add.setAddressCreateUser(lid)
        add.setAddressUpdateUser(lid)
        add.setAddressLineTwo("George Washington")
        add.save()
        v.setAddress(add)
        v.setVolunteerFirstName("George")
        v.setVolunteerLastName("Washington")
        v.setVolunteerCreateUser(lid)
        v.setVolunteerUpdateUser(lid)
        v.setOrganization(org)
        v.save()
        assert v.address, 'No volunteer address'
        assert v.myDb.address_id, 'missing address id'
        wa = WorkAddress(myDb=DbWorkAddress())
        add = Address(myDb=DbAddress())
        add.setAddressCreateUser(lid)
        add.setAddressUpdateUser(lid)
        with transaction.atomic():
            add.save()
            wa.setAddress(add)
            wa.setEmployer("Megabucks, Inc.")
            wa.setJobTitle("Lackey")
            wa.setWaCreateUser(lid)
            wa.setWaUpdateUser(lid)
            wa.setStreet("Megabucks Drive")
            wa.save()
            v.setWorkAddress(wa)
            #v.printDict()
            v.save()
        #print('********* before get ' + str(v.getVolunteerID()))
        #v.printDict() 
        v1 = of.getVolunteer(oid=v.getVolunteerID(),dbo=True)
        #print(v1)
        #print('********* ' + str(v.getVolunteerID()))
        #v1.printDict() 
        #print('********* ' + str(v1)) 
        assert v1,'no volunteer'
        assert v.getWorkAddress(), 'missing work address'
        #print('\n v1 ' + str(v.getVolunteerID()))
        r = Relationship(myDb=DbRelationship())
        r.setOrganization(org)
        typ = of.getRelationshipType(oid=3)
        #print(typ)
        r.setRelationshipType(typ)
        r.setVolunteerOne(v)
        #print('r v1 ' + str(r.myDb.volunteerOne_id))
        v2 = of.getNewVolunteer(hi3,1,org,'Mrs Velda','Jones')
        r.setVolunteerTwo(v2)
        r.setRelationshipCreateUser(lid)
        r.setRelationshipUpdateUser(lid)
        #print('r v2 ' + str(r.myDb.volunteerTwo_id))
        #r.printDict()
        r.save()
        rid = r.getRelationshipID()
        r2 = of.getRelationship(rid)
        #print('r2 type: ' + str(r2.relationshipType))
        #r2.printDict()
        assert r2, 'got no relationship'
        assert r2.getOrganization(), 'no org'
        assert r2.areTogether(), 'wrong relationship type'
        v = None
        for i in range(5):
            v = Volunteer(myDb=DbVolunteer())
            v.setHousehold(hi2)
            v.setOrganization(org)
            v.setVolunteerFirstName("Will #" + str(i))
            v.setVolunteerLastName("Smith")
            v.setVolunteerCreateUser(lid)
            v.setVolunteerUpdateUser(lid)
            v.setOrganization(org)
            v.save()
        resourceNames = [
            "Lectionary",
            "Candle",
            "Lighter",
            "Crucifix",
            "Organ",
            "Anvil",
            "Hammer",
            "Saw",
            "Piano",
            "Fire Extinguisher"
        ]
        res = None
        for name in resourceNames:
            res = Resource(myDb=DbResource())
            res.setOrganization(org)
            res.setCount(1)
            res.setName(name)
            res.setResourceCreateUser(lid)
            res.setResourceUpdateUser(lid)
            res.save()
        res = of.getResource(oid=res.getResourceOrganizationID())
        #res.printDict()
        assert res.getResourceOrganizationID(), 'no resource org id'
        skillNames = [
            "Teacher",
            "Principal",
            "Cook",
            "School Administrative Assistant",
            "Master of Ceremonies",
            "Motivational Speaker",
            "Education Committee Chair",
            "Building Committee Chair",
            "Finance Council Chair",
            "Fundraising Committee Chair",
            "Social Civic Committee Chair",
            "Social Justice Committee Chair",
            "Liturgy Committee Chair",
            "Music Minister",
            "Decorator",
            "Pastor",
            "Priest",
            "Parish Administrative Assistant",
            "Parish Administrator",
            "Youth Minister",
            "Religious Education Director",
            "Deacon",
            "Cantor",
            "Server",
            "Usher",
            "Organist",
            "Plumber",
            "Attorney",
            "CPA",
            "Carpenter",
            "Electrician",
            "Roofer",
            "Painter",
            "Lector",
            "Fireman"]
        s = DbSkill.objects.filter(skillName="Pastor").first()
        if not s:
            for skillName in skillNames:
                s = Skill(myDb=DbSkill())
                s.setOrganization(org)
                s.setSkillName(skillName)
                s.setSkillCreateUser(lid)
                s.setSkillUpdateUser(lid)
                s.save()
        s = of.getSkill(oid=s.getSkillID())
        assert s.getSkillOrganizationID(), 'no skill org id' 
        locationNames = [
            "Church",
            "Church Hall",
            "Park",
            "Joe's Bar and Grill",
            "Piggy's Pen"
        ]
        #if not org or not org.getOrganizationID(): #kluge
        #    org = of.getOrganizations()[-1]
        loc = None
        for locName in locationNames:
            loc = of.getNewLocation(locName,1,org)
        loc = of.getLocation(oid=loc.getLocationID())
        assert loc.getOrganizationID(), ' no loc org id'
        assert loc.myDb.organization_id, ' no loc myDb org id'
        eri = EventRecurrence(myDb=DbEventRecurrence())
        eri.setCreateUser(lid)
        eri.setUpdateUser(lid)
        eri.setIntervalAmount(1)
        dt = DT.strptime('2026-06-01', "%Y-%m-%d")
        eri.setEndDate(dt)
        dt = DT.strptime('2026-05-01', "%Y-%m-%d")
        eri.setStartDate(dt)
        eri.setRecurrenceType(of.getRecurrenceType(5))
        eri.save()
        ev = ScheduleEvent(myDb=DbScheduleEvent())
        ev.setOrganization(org)
        ev.setEventName("July 4 Fireworks")
        ev.setEventDuration(90)
        dt = DT.strptime('2026-07-04', "%Y-%m-%d")
        ev.setEventDate(dt)
        ev.setEventStartTime("21:00:00")
        ev.setEventCreateUser(lid)
        ev.setEventUpdateUser(lid)
        ev.setLocation(loc)
        ev.setRecurrence(eri)
        #ev.printDict()
        ev.save()
        ev1 = of.getEvent(oid=ev.getEventID())
        assert ev1.getOrganization, ' no event org'
        assert ev1.myDb.organization_id, ' no event myDb org id'
        j = Job(myDb=DbJob())
        j.setJobCreateUser(lid)
        j.setJobUpdateUser(lid)
        j.setSkill(s)
        j.setEventID(ev.getID())
        j.save()
        assert j.skill, 'no job skill after save'
        j1 = of.getJob(oid=j.getJobID(), dbo=True)
        assert j1, 'no job'
        assert j1.skill, 'no job skill'
        ev.addJob(j)
        ev.save()
        j2 = of.getJob(oid=j.getJobID())
        assert j2.skill, 'no skill w/ job'
        ejr = EventJoinToResource(myDb=DbEventJoinToResource())
        ejr.setResourceID(res.getResourceID())
        ejr.setEventID(ev.getEventID())
        ejr.setUsed(10)
        ejr.setCreateUser(lid)
        ejr.setUpdateUser(lid)
        ejr.save()
        ev.addResourceJoin(ejr)
        ev.addResource(res)
        ev.save()
        dbh = DbHousehold()
        hi4 = Household(myDb=dbh,org=org,uid=1)
        hi4.setHouseholdFirstName('Murville')
        hi4.setHouseholdLastName('Hurd')
        hi4.setHouseholdCreateUser(lid)
        hi4.setHouseholdUpdateUser(lid)
        hi4.save()
        v = of.getNewVolunteer(hi4, 1, org, 'Murville', 'Hurd')
        vsi = VolunteerSkill(DbVolunteerSkill())
        vsi.setVsCreateUser(lid)
        vsi.setVsUpdateUser(lid)
        vsi.setSkill(s)
        vsi.setExpert(True)
        vsi.save()
        #print('\nloader v1 ' + str(v.myDb.volunteerCreateUser))
        v.save()
        #print('\nloader v2 ' + str(v.myDb.volunteerCreateUser))
        v.addSkill(vsi)
        #print('\nloader v3 ' + str(v.myDb.volunteerCreateUser))
        v.save()
        #print('\nloader v4 ' + str(v.myDb.volunteerCreateUser))
        ep = EventPreference(myDb=DbEventPreference())
        ep.setEvent(ev)
        ep.setVolunteer(v)
        ep.setPreferenceCreateUser(lid)
        ep.setPreferenceUpdateUser(lid)
        #print('\nloader v5 ' + str(v.myDb.volunteerCreateUser))
        ep.save()
        assert ep.event, 'no preference event'
        assert ep.volunteer, 'no preference volunteer'
        #print('\nloader v6 ' + str(v.myDb.volunteerCreateUser))
        av = Availability(myDb=DbAvailability())
        av.setVolunteer(v)
        av.setAvailabilityCreateUser(lid)
        av.setAvailabilityUpdateUser(lid)
        av.setAvailabilityStartDate(DT.now())
        #v.printDict()
        av.save()
        assert av.volunteer, 'no availability volunteer'
        #v.printDict()
        #print('\nloader v7 ' + str(v.myDb.volunteerCreateUser))
        v.save()
        #v.printDict()
        #print('\nloader v8 ' + str(v.myDb.volunteerCreateUser))
        l = DbLocation.objects.filter(locationName="Church Hall").first()
        if l: 
            loc = Location(l)
        eri = EventRecurrence(myDb=DbEventRecurrence())
        eri.setCreateUser(lid)
        eri.setUpdateUser(lid)
        eri.setIntervalAmount(1)
        dt = DT.strptime('2028-07-04', "%Y-%m-%d")
        eri.setEndDate(dt)
        dt = DT.strptime('2022-07-04', "%Y-%m-%d")
        eri.setStartDate(dt)
        ert = of.getRecurrenceType(4)
        eri.setRecurrenceType(ert)
        eri.save()
        ev.setOrganization(org)
        ev.setEventName("KofC Meeting")
        ev.setEventDuration(1500)
        dt = DT.strptime('2026-07-04', "%Y-%m-%d")
        ev.setEventDate(dt)
        ev.setEventStartTime("17:30:00")
        ev.setEventCreateUser(lid)
        ev.setEventUpdateUser(lid)
        ev.setLocation(loc)
        ev.setRecurrence(eri)
        ev.addJob(j)
        ev.addResource(res)
        ev.addResourceJoin(ejr)
        #ev.printDict()
        ev.save()
        #ev.printDict()
        sched = of.getNewSchedule(dt,dt,1,org)
        sched.addEvent(ev)
        sched.setOrganization(org)
        sched.setScheduleStartDate(dt)
        sched.setScheduleEndDate(dt)
        sched.setScheduleCreateUser(1)
        sched.setScheduleUpdateUser(1)
        schedStat = of.getScheduleStatus(1)
        sched.setScheduleStatus(schedStat)
        #sched.printDict()
        sched.save()
        ev.setSchedule(sched)
        ev.save()
        assert sched.scheduleStatus, ' no schedule status'
        assert sched.organization, 'no schedule organization'
        ev2 = of.getEvent(oid=ev.getEventID())
        #ev2.printDict()
        assert ev2,'no event for id ' + str(ev.getEventID())
        assert ev2.organization, 'no event organization'
        assert ev2.location, 'no event location'
        assert ev2.recurrence, ' no event recurrence'
        assert ev2.resources, 'no event resources'
        assert ev2.resourceJoins, 'no event resources'
        assert ev2.getJobs(), ' no event jobs'
               