'''
Created on Sep 27, 2026

@author: Darrel Courrier
'''
from datetime import date,datetime as DT
from vs.models import *
from vscode.base.base import VSBase
from vscode.loader.loaders import LoaderManager
from vscode.val.vals import *
from pickle import FALSE
from vscode.utils.utils import Encrypter

class DatabaseSetup(VSBase):

    def __init__(self):
        if len(DbStateCode.objects.all()) == 0:
            LoaderManager().load()
        if not DbVolunteer.objects.all().first():
            v = None
            rel = None
            org = None
            try:
                for o in DbOrganization.objects.all():
                    if o.organizationName == 'System':
                        continue
                    org = o
                    break  
                li = DbLogin.objects.filter(pk=1).first()
                pwd = DbPassword()
                pwd.password ="gronk"
                pwd.passwordCreateUser = 1
                pwd.passwordUpdateUser = 1
                pwd.login_id = 1
                pwd.save()
                add = DbAddress()
                add.addressCreateUser = 1
                add.addressUpdateUser = 1
                add.save()
                hi1 = DbHousehold()
                hi1.address_id = add.addressID
                hi1.organization_id = org.organizationID
                add.addressLineTwo = "Address Line Two"
                add.city = "Any Town"
                add.email = "hitech@wonder.net"
                add.fax = "## fax ##"
                add.mobilePhone = "Cell #"
                add.pager = "Pager #"
                add.phone = "phone #"
                add.postalCode = "zip + 4"
                add.state = "MN"
                add.street = "123 Elm"
                hi1.householdFirstName = "Tom"
                hi1.householdLastName = "Jones"
                hi1.householdCreateUser = 1
                hi1.householdUpdateUser = 1
                hi1.save()
                v = DbVolunteer()
                v.household_id = hi1.householdID
                v.organization_id = org.organizationID
                v.volunteerFirstName = "Tom"
                v.volunteerLastName = "Jones"
                v.volunteerCreateUser = 1
                v.volunteerUpdateUser = 1
                v.save()
                add2 = DbAddress()
                add2.addressCreateUser = 1
                add2.addressUpdateUser = 1
                add2.street = "Will Smith"
                add2.save()
                hi2 = DbHousehold()
                hi2.organization_id = org.organizationID
                hi2.address_id = add2.addressID
                hi2.householdFirstName = "Will"
                hi2.householdLastName = "Smith"
                hi2.householdCreateUser = 1 
                hi2.householdUpdateUser = 1 
                hi2.save()
                v2 = DbVolunteer()
                v2.household_is = hi2.householdID
                v2.organization_id = org.organizationID
                v2.volunteerFirstName = "Will"
                v2.volunteerLastName = "Smith"
                v2.volunteerCreateUser = 1
                v2.volunteerUpdateUser = 1
                v2.save()
                add3 = DbAddress()
                add3.street = "Booker T. Washington Dr"
                add3.addressCreateUser = 1
                add3.addressUpdateUser = 1
                add3.save()
                hi3 = DbHousehold()
                hi3.organization_id = org.organizationID
                hi3.address_id = add3.addressID
                hi3.householdFirstName = "Booker T."
                hi3.householdLastName = "Washington"
                hi3.householdCreateUser = 1
                hi3.householdUpdateUser = 1
                hi3.save()
                v3 = DbVolunteer()
                v3.household_is = hi3.householdID
                v3.organization_id = org.organizationID
                v3.volunteerFirstName = "Booker T."
                v3.volunteerLastName = "Washington"
                v3.volunteerCreateUser = 1
                v3.volunteerUpdateUser = 1
                v3.save()
                r = DbRelationship()
                r.organization_id = org.organizationID
                r.relationshipType_id = RelationshipType.TOGETHER_PREFERRED_VAL
                r.relationshipCreateUser = 1
                r.relationshipUpdateUser = 1
                r.volunteerOne_id = v3.volunteerID
                add4 = DbAddress()
                add4.addressCreateUser = 1
                add4.addressUpdateUser = 1
                add4.addressLineTwo = "George Washington Ave"
                add4.save()
                v4 = DbVolunteer()
                v4.volunteerFirstName = "George"
                v4.volunteerLastName ="Washington"
                v4.volunteerCreateUser = 1
                v4.volunteerUpdateUser = 1
                v4.organization_id = org.organizationID
                v4.save()
                add4.volunteer_id = v4.volunteerID
                wa = DbWorkAddress()
                waAdd = DbAddress()
                waAdd.addressLineTwo = "George Washington Work"
                waAdd.street = "Megabucks Drive"
                waAdd.addressCreateUser = 1
                waAdd.addressUpdateUser = 1
                waAdd.save()
                wa.address_id  = waAdd.addressID
                wa.volunteer_id = v4.volunteerID
                wa.employer = "Megabucks, Inc."
                wa.jobTitle = "Lackey"
                wa.waCreateUser = 1
                wa.waUpdateUser = 1
                v4.save()
                wa.volunteer_id = v4.volunteerID
                wa.save()
                r.volunteerTwo_id = v4.volunteerID
                r.save()
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
                for name in resourceNames:
                    res = DbResource()
                    res.organization_id = org.organizationID
                    res.count = 1
                    res.name = name
                    res.resourceCreateUser = 1
                    res.resourceUpdateUser = 1
                    res.save()
                
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
                for skillName in skillNames:
                    s = DbSkill()
                    s.organization_id = org.organizationID
                    s.skillName = skillName
                    s.skillCreateUser = 1
                    s.skillUpdateUser = 1
                    s.save()
    
                locationNames = [
                    "Church",
                    "Church Hall",
                    "Park"
                ]
                for locName in locationNames:
                    loc = DbLocation()
                    loc.organization_id = org.organizationID
                    loc.locationName = locName
                    loc.locationCreateUser = 1
                    loc.locationUpdateUser = 1
                    loc.save()
                dts = date(2022,7,4)
                dte = date(2027, 7, 4)
                er = DbEventRecurrence()
                er.recurrenceCreateUser = 1
                er.recurrenceUpdateUser = 1
                er.intervalAmount = 1
                er.startDate = dte
                er.type_id = 5
                er.save()
                ev = DbScheduleEvent()
                ev.organization_id = org.organizationID
                ev.eventName = "July 4 Fireworks"
                ev.eventDuration = 90
                ev.eventDate = DT.now().date()
                ev.eventStartTime = "21:00:00"
                ev.eventCreateUser = 1
                ev.eventUpdateUser = 1
                ev.location_id = loc.locationID
                ev.recurrence_id = er.recurrenceID
                ev.save()
                job = DbJob()
                job.jobCreateUser = 1
                job.jobUpdateUser = 1
                job.skill_id = 1
                job.event_id = ev.eventID
                job.save()
                ejr = DbEventJoinToResource()
                ejr.event_id = ev.eventID
                ejr.resource_id = 1
                ejr.createUser = 1
                ejr.updateUser = 1
                ejr.save()
                vsi = DbVolunteerSkill()
                vsi.vsCreateUser = 1
                vsi.vsUpdateUser = 1
                vsi.skill_id = 1
                vsi.volunteer_id = v4.volunteerID
                vsi.Expert=True
                vsi.save()
                ep = DbEventPreference()
                ep.event_id = ev.eventID
                ep.volunteer_id = v4.volunteerID
                ep.preferenceCreateUser = 1
                ep.preferenceUpdateUser = 1
                ep.save()
                av = DbAvailability()
                av.volunteer_id = v4.volunteerID
                av.availabilityCreateUser = 1
                av.availabilityUpdateUser = 1
                av.availabilityStartDate = DT.now().date()
                av.save()
            except Exception as e:
                super().handleException(e)
        needpwdfix = False
        enc = Encrypter()
        try:
            for pwd in DbPassword.objects.all():
                val = enc.decrypt(pwd.password)
                if val != 'Password1':
                    needpwdfix = True
                    break
        except:
            needpwdfix = True
        if needpwdfix:
            newPwd = enc.encrypt('Password1')
            for pw in DbPassword.objects.all():
                pw.password = newPwd
                pw.save() 