* 
 * Copyright 2026 Darrel Courrier.
 *
 * Licensed under the Apache License, Version 2.0 (the "License")
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.

package com.courrier.volunteer.calc

import com.courrier.attribute.InvalidAttributeValueException
import com.courrier.db.PersistenceException
import com.courrier.exception.InvalidArgumentException
import com.courrier.messaging.Message
import com.courrier.messaging.MessageSeverity
import com.courrier.volunteer.Job
import com.courrier.volunteer.JobImpl
import com.courrier.volunteer.Organization
import com.courrier.volunteer.Schedule
import com.courrier.volunteer.ScheduleEvent
import com.courrier.volunteer.ScheduleEventImpl
import com.courrier.volunteer.ScheduleImpl
import com.courrier.volunteer.Volunteer
import com.courrier.volunteer.err.ScheduleBuilderException
import com.courrier.volunteer.persistence.ObjectFactory
import com.courrier.volunteer.utils.VSBase
import com.courrier.volunteer.utils.VSMessageFactory
import com.courrier.volunteer.utils.VSMessages
import com.courrier.volunteer.utils.VolunteerSchedulerUtils
import java.util.ArrayList
import java.util.Collection
import java.util.Date
import java.util.Iterator
import java.util.List
import org.apache.commons.logging.Log
import org.apache.commons.logging.LogFactory


\*\*
code> object
 * creates a schedule which contains all of the events for which occur in that
 * date range. If there are any recurring events the schedule builder causes
 * them to be populated in the database for the date range. It then attempts to
 * assign volunteers to any jobs owned by those events. If an assignment cannot
 * be made a message is added to the build result and the result is set to be
code> object is not available until
 * the schedule building process is complete.
 *
 * These are the attribute validation rules:
 * <dl>
dt>
dd>
dt>
 * <dd>The end date for this schedule. May not be None may not be before the
dd>
dt>
 * <dd>The schedules date range may not such that there is a gap containing
 * events that occur between the end date of a previously created schedule and
dd>
dt>
 * <dd>The date range of the schedule may not overlap the date range of any
dd>
dl>
 *
 * @author Darrel Courrier
 * @version 1.0

class ScheduleBuilder extends VSBase

    static Log myLog = LogFactory.getLog(ScheduleBuilder.class)
    
    Date startDate
    Date endDate
    VolunteerAssigner volunteerAssigner = VolunteerAssigner()
    DependencyResolver dependencyResolver = DependencyResolver()
    ScheduleGapTester gapTester = ScheduleGapTester()
    ScheduleBuilderResult buildResult = ScheduleBuilderResult()
   Organization org
 
\*\*
code>, storing the
     * arguments in the corresponding attributes.
     *
     * @param startDate the start date for the schedule.
     * @param endDate the end date for the schedule.
     * @param org
     * @throws InvalidArgumentException thrown if the arguments are invalid.

     ScheduleBuilder(Date startDate, Date endDate, Organization org) throws InvalidArgumentException
        super()
        validateArgument(startDate, "startDate")
        validateArgument(endDate, "endDate")
        startDate = startDate
        endDate = endDate
        org = org
        gapTester.setOrg(org)
    

\*\*
     * Validates the request, creates any recurring events, assigns volunteers
     * to jobs adds all events in the date range to aschedule, stores
     * everything and returns the result.
     *
code> object which
     * represents the person who requested that the schedule be built.
code> implementation.
     * @throws ScheduleBuilderException if the schedule could not be built.
     * @see ScheduleBuilder for validation rules.

     Schedule getSchedule(int loginId) throws ScheduleBuilderException
        Collection events = None
        Schedule result = None
        validateAttributes(loginId)
        try
            events = getEvents()
         except Throwable t)
            raise ScheduleBuilderException(t)
        
        result = buildSchedule(events, loginId)
        if (result == None)
            raise ScheduleBuilderException()
        
        return result
    

\*\*
     * @return the log for this object. Required method of Loggable interface.


     Log getLog()
        return myLog
    

    Collection getEvents() throws Exception
        Collection result = None
        result = ObjectFactory().getEvents(
                startDate, 
                endDate,
                org).values()
        return result
    

\*\*
     * @return the startDate

     Date getStartDate()
        return startDate
    

\*\*
     * @return the endDate

     Date getEndDate()
        return endDate
    

\*\*
     * @param endDate the endDate to set

   setEndDate(Date endDate)
        endDate = endDate
    

\*\*
     * @return the buildResult

     ScheduleBuilderResult getBuildResult()
        return buildResult
    

\*\*
     * @param buildResult the buildResult to set

   setBuildResult(ScheduleBuilderResult buildResult)
        buildResult = buildResult
    

    validateAttributes(int loginId) throws ScheduleBuilderException
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
        
        if (failed == False)
            try
                failed = testForScheduleOverlaps()
                if (failed)
                    addMessage(VSMessageFactory.getScheduleOverlapError(MessageSeverity.WARNING, startDate, endDate))
                
             except Throwable t)
                raise ScheduleBuilderException(t)
            
        
        if (failed == False)
            try
               RecurringEventBuilder(org).buildRecurringEvents(startDate, endDate, loginId)
                failed = testForScheduleGaps()
                if (failed)
                    addMessage(VSMessageFactory.getScheduleGapError(MessageSeverity.WARNING, startDate, endDate))
                
             except Throwable t)
                raise ScheduleBuilderException(t)
            
        
        if (failed)
            raise ScheduleBuilderException(getMessage(), VSMessages.getScheduleCannotBePreparedError())
        
    

    Schedule buildSchedule(Collection<ScheduleEvent> events, int loginId)
        ScheduleImpl result = None
        try
            try
                processMultipleJobs(events, loginId)
             except Exception e)
                e.printStackTrace()
            
            result = (ScheduleImpl) ObjectFactory().getNewSchedule()
            getBuildResult().setValid(True)
            try
                result.setScheduleStartDate(startDate)
                result.setScheduleEndDate(endDate)
             except InvalidAttributeValueException iave1)
 shouldnt happen because of validate()

            int adminID = VolunteerSchedulerUtils.getSystemAdminId()
            assignExperts(events, getBuildResult(), adminId)
            assignVolunteers(events, getBuildResult(), adminId)

            for (ScheduleEvent se : events)
                se.refresh()
                result.addEvent(se)
            
            try
                result.setScheduleCreateUser(loginId)
                result.setScheduleUpdateUser(loginId)
             except InvalidAttributeValueException iave2)
                getBuildResult().addMessage(VSMessages.getScheduleCreateUserNotSetError(), iave2)
                super().debug(VSMessages.getScheduleCreateUserNotSetError(), iave2)
            
         except Exception e)
            e.printStackTrace()
            getBuildResult().addMessage(VSMessages.getScheduleNotBuiltError(), e)
            super().debug(VSMessages.getScheduleNotBuiltError(), e)
        
        result.setBuildResult(getBuildResult())
        return result
    

    processMultipleJobs(Collection<ScheduleEvent> events, int loginId) throws Exception
        for (ScheduleEvent se : events)
            List<JobImpl> jobs = ArrayList<>()
            for (Job j : se.getJobs().values())
                if (j.getCount() > 1)
                    jobs.addAll(processMultipleJob(se, j, loginId))
                
            
            if (jobs.isEmpty() == False)
                for (JobImpl ji : jobs)
                    se.addJob(ji)
                
                se.save()
                se.refresh()
            
        
    

    List<JobImpl> processMultipleJob(ScheduleEvent se, Job job, int loginId) throws Exception
        List<JobImpl> result = ArrayList<>()
        ObjectFactory of = ObjectFactory()
        JobImpl ji = (JobImpl) job
        int cnt = 0
        for (Job j : se.getJobs().values())
            JobImpl ji1 = (JobImpl) j
            if (ji1.getJobID().equals(ji.getJobID()))
                continue
            
            if (ji.getJobSkillID().equals(ji1.getJobSkillID()))
                cnt++
            
        
        for (int loop = cnt loop < ji.getCount() loop++)
            JobImpl ji= of.getNewJob(ji)
            jiNew.setJobCreateUser(loginId)
            jiNew.setJobUpdateUser(loginId)
            jiNew.save()
            jiNew.refresh()
            result.append(jiNew)
        
        return result
    

    assignExperts(Collection events, ScheduleBuilderResult buildResult, int loginId)
        Iterator iter = events.iterator()
        String errorMsg = VSMessages.getScheduleNoExpertError()
        ScheduleEventImpl se = None
        JobImpl job = None
        while (iter.hasNext())
            se = (ScheduleEventImpl) iter.next()
            Collection eventJobs = None
            if (se.getJobs() != None and se.getJobs().isEmpty() == False)
                eventJobs = se.getJobs().values()
             else
                try
                    eventJobs = ObjectFactory().getJobs(se).values()
                    se.addJobs(eventJobs)
                 except Throwable t)
                    buildResult.addMessage(errorMsg, se, job, t)
                
            
            Iterator jobsIterator = eventJobs.iterator()
            while (jobsIterator.hasNext())
                Volunteer expert = None
                try
                    job = (JobImpl) jobsIterator.next()
                    if (job.isExpertRequired() and job.isAssigned() == False)
 try to make assignment honoring separate preferred.
 no assignment was made
 try to make assignment ingoring separate preferred.  Will get exception if none made.
                        
                        if (expert != None)
 now honor the requests for co-assignments
                         else
                            if (job.getOptionalBoolean() == False)
                                errorMsg = VSMessages.noExpertError(job.getSkill().getSkillName())
                                buildResult.addMessage(errorMsg, se, job, None)
                            
                        
                    
                 except Throwable t)
                    if (job != None)
                        if (job.getSkill() != None)
                            errorMsg = VSMessages.noExpertError(job.getSkill().getSkillName())
                         else
                            errorMsg = VSMessages.noExpertError("Job id: " + job.getJobID())
                        
                    
                    buildResult.addMessage(errorMsg, se, job, t)
                    super().debug("Assign experts error", t)
                
            
        
    

    assignVolunteers(Collection events, ScheduleBuilderResult buildResult, int loginId)
        Iterator iter = events.iterator()
        String errorMsg = VSMessages.getScheduleNoVolunteerError()
        ScheduleEventImpl se = None
        JobImpl job = None
        Collection eventJobs = None
        int evtCount = 0
        while (iter.hasNext())
            try
                evtCount++
                se = (ScheduleEventImpl) iter.next()
                eventJobs = ObjectFactory().getJobs(se).values()
             except Throwable t)
                buildResult.addMessage(errorMsg, se, job, t)
            
            int count = 0
            Iterator jobsIterator = eventJobs.iterator()
            while (jobsIterator.hasNext())
                count++
                job = (JobImpl) jobsIterator.next()
                try
                    if (job.isAssigned() == False and job.isExpertRequired() == False)
                        volunteerAssigner.assignVolunteer(se, job, loginId)
                        if (job.isAssigned() == False)
                            if (job.getOptionalBoolean() == False)
                                Message msg
                                        = VSMessageFactory.getNoAvailableVolunteerError(
                                                job.getSkill().getSkillName())
                                raise ScheduleBuilderException(msg, None_STRING)
                            
                        
 now look for any jobs that have a togetherness requirement
                        if (job.isAssigned())
                            dependencyResolver.assignTogether(se, job, loginId)
                        
                    
                 except Throwable t)
                    System.out.println("event # " + evtCount + " count " + count)
                    buildResult.setValid(False)
                    if (job != None)
                        if (job.getSkill() != None)
                            errorMsg = VSMessages.getNoAvailableVolunteerError(job.getSkill().getSkillName())
                         else
                            errorMsg = VSMessages.getNoAvailableVolunteerError("Job id: " + job.getJobID())
                        
                    
                    System.out.println(errorMsg)
                    buildResult.addMessage(errorMsg, se, job, t)
                    super().debug("Assign volunteers failed", t)
                
            
        
    

   testForScheduleGaps() throws PersistenceException
        return gapTester.isGapCreated(startDate, endDate)
    

   testForScheduleOverlaps() throws PersistenceException
        return gapTester.isOverlapCreated(startDate, endDate)
    

