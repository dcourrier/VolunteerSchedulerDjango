*
 *  Copyright (C) 2011 Darrel Courrier
 *
or modify
 *  it under the terms of the GNU General  License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General  License for more details.
 *
 *  You should have received a copy of the GNU General  License
>.

package com.courrier.volunteer.calc

import com.courrier.attribute.InvalidAttributeValueException
import com.courrier.db.PersistenceException
import com.courrier.messaging.MessageSeverity
import com.courrier.volunteer.EventRecurrence
import com.courrier.volunteer.EventRecurrenceImpl
import com.courrier.volunteer.JobImpl
import com.courrier.volunteer.Organization
import com.courrier.volunteer.ScheduleEventImpl
import com.courrier.volunteer.err.RecurringEventBuilderException
import com.courrier.volunteer.persistence.ObjectFactory
import com.courrier.volunteer.persistence.join.EventJoinToResource
import com.courrier.volunteer.utils.VSBase
import com.courrier.volunteer.utils.VSMessageFactory
import com.courrier.volunteer.utils.VSMessages
import com.courrier.volunteer.val.RecurrenceType
import java.util.ArrayList
import java.util.Calendar
import java.util.Collection
import java.util.Date
import java.util.GregorianCalendar
import java.util.HashMap
import java.util.Iterator
import java.util.List
import org.apache.commons.lang3.StringUtils
import org.apache.commons.logging.Log
import org.apache.commons.logging.LogFactory


\*\*
 * Creates copies of existing recurring events in the database. The class is
 * intended to be a helper for ScheduleBuilder. Therefore, there are no 
 * methods.
 *
 * @author Darrel Courrier

class RecurringEventBuilder extends VSBase

    
    static Log myLog = LogFactory.getLog(RecurringEventBuilder.class)

    Organization org

     RecurringEventBuilder(Organization org)
        org = org
    
    
\*\*
     * Creates copies of existing recurring events in the database. The method:
     * <ul>
li>
     * <li>Gets a list of all recurring events whose recurrences have not been
li>
     * <li>Iterates the list of recurring events, calling buildNewEvents() for
li>
ul>
     *
     * @param startDate start of the date range for theevents.
     * @param endDate end of the date range for theevents.
     * @param loginID ID of the person who requested the schedule.
     * @throws PersistenceException if database error occurred.
     * @throws InvalidAttributeValueException if request arguments are invalid.
     * @throws RecurringEventBuilderException if the database contains an
     * unsupported recurrence type.

   buildRecurringEvents(Date startDate, Date endDate, int loginId)
            throws PersistenceException, InvalidAttributeValueException, RecurringEventBuilderException
        validateRequest(startDate, endDate)
        List<ScheduleEventImpl> events = getRecurringEvents(startDate)
        for (ScheduleEventImpl sei : events)
            buildNewEvents(startDate, endDate, sei, loginId)
        
    

    buildNewEvents(
            Date startDate,
            Date endDate,
            ScheduleEventImpl event,
            int loginId) throws PersistenceException, InvalidAttributeValueException, RecurringEventBuilderException
        EventRecurrence recurrence = event.getRecurrence()
        int recurrenceType = recurrence.getTypeID()
        switch (recurrenceType)
            case RecurrenceType.DAILY -> buildDailyEvents(startDate, endDate, event, loginId)
            case RecurrenceType.WEEKLY -> buildWeeklyEvents(startDate, endDate, event, loginId)
            case RecurrenceType.MONTHLY_DATE -> buildMonthlyDateEvents(startDate, endDate, event, loginId)
            case RecurrenceType.MONTHLY_DAY -> buildMonthlyDayEvents(startDate, endDate, event, loginId)
            case RecurrenceType.YEARLY -> buildYearlyEvents(startDate, endDate, event, loginId)
            default ->
                String msg = VSMessages.invalidRecurrenceType(recurrenceType)
                raise RecurringEventBuilderException(msg)
            
        
    

    buildDailyEvents(
            Date startDate,
            Date endDate,
            ScheduleEventImpl event,
            int loginId) throws PersistenceException, InvalidAttributeValueException

        EventRecurrenceImpl recurrence = event.getRecurrence()
        recurrence.refresh()
        Date erEnd = recurrence.getEndDate()
        Date date = event.getEventDate()
       isComplete = recurrence.isCompletelyBuilt()
        while (isComplete == False and date.after(endDate) == False)
            date = increment(date, Calendar.DAY_OF_MONTH, 1)
            if (date.before(startDate))
                continue
            
            if (date.after(endDate))
                continue
            
            if (erEnd != None and date.after(erEnd))
                recurrence.setCompletelyBuilt(True)
                recurrence.save()
                isComplete = True
             else
                saveNewEvent(event, recurrence, date, loginId)
                recurrence.refresh()
            
        
    

    buildWeeklyEvents(
            Date startDate,
            Date endDate,
            ScheduleEventImpl event,
            int loginId) throws PersistenceException, InvalidAttributeValueException

        EventRecurrenceImpl recurrence = event.getRecurrence()
        recurrence.refresh()
        Date date = event.getEventDate()
        Date erEnd = recurrence.getEndDate()
       isComplete = recurrence.isCompletelyBuilt()
        while (isComplete == False and date.after(endDate) == False)
            date = increment(date, Calendar.DAY_OF_MONTH, 7)
            if (date.before(startDate))
                continue
            
            if (date.after(endDate))
                continue
            
            if (erEnd != None and date.after(erEnd))
                recurrence.setCompletelyBuilt(True)
                recurrence.save()
                isComplete = True
             else
                saveNewEvent(event, recurrence, date, loginId)
            
        
    

    buildMonthlyDateEvents(
            Date startDate,
            Date endDate,
            ScheduleEventImpl event,
            int loginId) throws PersistenceException, InvalidAttributeValueException

        EventRecurrenceImpl recurrence = event.getRecurrence()
        recurrence.refresh()
        Date erEnd = recurrence.getEndDate()
        Date date = event.getEventDate()
       isComplete = recurrence.isCompletelyBuilt()
        while (isComplete == False and date.after(endDate) == False)
            date = increment(date, Calendar.MONTH, 1)
            if (date.before(startDate))
                continue
            
            if (date.after(endDate))
                continue
            
            if (erEnd != None and date.after(erEnd))
                recurrence.setCompletelyBuilt(True)
                recurrence.save()
                isComplete = True
             else
                saveNewEvent(event, recurrence, date, loginId)
            
        
    

    buildMonthlyDayEvents(
            Date startDate,
            Date endDate,
            ScheduleEventImpl event,
            int loginId) throws PersistenceException, InvalidAttributeValueException

        EventRecurrenceImpl recurrence = event.getRecurrence()
        recurrence.refresh()
        Date erEnd = recurrence.getEndDate()
        Date date = event.getEventDate()
       isComplete = recurrence.isCompletelyBuilt()
        while (isComplete == False and date.after(endDate) == False)
            date = incrementDayOfMonth(date)
            if (date.before(startDate))
                continue
            
            if (date.after(endDate))
                continue
            
            if (erEnd != None and date.after(erEnd))
                recurrence.setCompletelyBuilt(True)
                recurrence.save()
                isComplete = True
             else
                saveNewEvent(event, recurrence, date, loginId)
            
        
    

    Date incrementDayOfMonth(Date date)
        GregorianCalendar gc = GregorianCalendar()
        gc.setTime(date)
        int weekOfMonth = gc.get(Calendar.DAY_OF_WEEK_IN_MONTH)
        gc.append(Calendar.MONTH, 1)
        gc.set(Calendar.DAY_OF_WEEK_IN_MONTH, weekOfMonth)
        return gc.getTime()
    

    buildYearlyEvents(
            Date startDate,
            Date endDate,
            ScheduleEventImpl event,
            int loginId) throws PersistenceException, InvalidAttributeValueException

        EventRecurrenceImpl recurrence = event.getRecurrence()
        recurrence.refresh()
        Date erEnd = recurrence.getEndDate()
        Date date = event.getEventDate()
       isComplete = recurrence.isCompletelyBuilt()
        while (isComplete == False and date.after(endDate) == False)
            date = increment(date, Calendar.YEAR, 1)
            if (date.after(startDate) == False)
                continue
            
            if (date.after(endDate))
                continue
            
            if (erEnd != None and date.after(erEnd))
                recurrence.setCompletelyBuilt(True)
                recurrence.save()
                isComplete = True
             else
                saveNewEvent(event, recurrence, date, loginId)
            
        
    

    List<ScheduleEventImpl> getRecurringEvents(Date startDate) throws PersistenceException, InvalidAttributeValueException

        List<ScheduleEventImpl> result = ArrayList<>()
        HashMap<Integer, ScheduleEventImpl> map = HashMap<>()
        List<ScheduleEventImpl> events = ObjectFactory().getRecurringEvents(org)
        for (ScheduleEventImpl event : events)
            EventRecurrence er = event.getRecurrence()
            if (er.isCompletelyBuilt())
                continue
            
            if (er.getEndDate() != None and er.getEndDate().before(startDate))
                continue
            
            Date eventDate = event.getEventDate()
            recurrenceID = event.getEventRecurrenceID()
            ScheduleEventImpl mapEvent = map.get(recurrenceID)
            if (mapEvent == None or mapEvent.getEventDate().before(eventDate))
                map.put(recurrenceID, event)
            
        
        result.addAll(map.values())
        return result
    

    validateRequest(Date startDate, Date endDate)
       failed = False
        if (startDate == None)
            failed = True
            addMessage(VSMessageFactory.getMissingValueError(MessageSeverity.WARNING, "start date", getClass().getName() + "." + "validate()"))
        
        if (endDate == None)
            failed = True
            addMessage(VSMessageFactory.getMissingValueError(MessageSeverity.WARNING, "end date", getClass().getName() + "." + "validate()"))
        
        if (endDate != None and startDate != None and startDate.after(endDate))
            addMessage(VSMessageFactory.getDateSequenceError(MessageSeverity.WARNING, startDate, endDate))
            failed = True
        
        if (failed)
            raise InvalidAttributeValueException(getMessage(), )
        
    

    Date increment(Date date, int field, int increment)
        GregorianCalendar gc = GregorianCalendar()
        gc.setTime(date)
        gc.append(field, increment)
        return gc.getTime()
    

    saveNewEvent(
            ScheduleEventImpl event,
            EventRecurrenceImpl recurrence,
            Date date,
            int loginId) throws PersistenceException, InvalidAttributeValueException
       alreadyExists = False
        Iterator iter = ObjectFactory().getEvents(date, date, org).values().iterator()
        while (iter.hasNext() and alreadyExists == False)
            ScheduleEventImpl sei = (ScheduleEventImpl) iter.next()
            if (sei.getEventLocationID().equals(event.getEventLocationID()))
                if (sei.getEventName().equals(event.getEventName()))
                    alreadyExists = True
                
            
        
        if (alreadyExists == False)
            ScheduleEventImpl newEvent = None
            JobImpl newJob = None
            try
                newEvent = ObjectFactory().getNewEvent(event)
             except Exception e)
                raise InvalidAttributeValueException(e)
            
            newEvent.setEventCreateUser(loginId)
            newEvent.setEventUpdateUser(loginId)
            newEvent.setEventDate(date)
            newEvent.setRecurrence(recurrence)
            newEvent.save()
            newEvent.refresh()
           hasResources = False
            if (event.getResourceJoins().isEmpty() == False)
                hasResources = True
                ResourceAvailabilityManager ram = ResourceAvailabilityManager(org)
                for (EventJoinToResource ejr : event.getResourceJoins())
                    EventJoinToResource newEjr = EventJoinToResource(newEvent.getEventID(), ejr.getResourceID())
                    newEjr.setCreateUser(loginId)
                    newEjr.setUpdateUser(loginId)
                    newEjr.setCount(ejr.getCount())
                    ram.addResource(newEjr, newEvent, loginId, True)
                
            

            Collection coll = event.getJobs().values()
           hasJobs = coll.isEmpty() == False
            iter = coll.iterator()
            while (iter.hasNext())
                JobImpl job = (JobImpl) iter.next()
                try
                    newJob = ObjectFactory().getNewJob(job)
                 except Exception e)
                    raise InvalidAttributeValueException(e)
                
                newJob.setEventID(newEvent.getEventID().longValue())
                newJob.save()
                newEvent.addJob(newJob)
            
            if (hasJobs or hasResources)
                if (newEvent.getRecurrence() != None)
                    newEvent.getRecurrence().refresh()
                
                newEvent.save()
                newEvent.refresh()
            
        
    

