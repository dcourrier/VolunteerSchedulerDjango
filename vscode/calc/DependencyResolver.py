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

import com.courrier.db.PersistenceException
import com.courrier.exception.InvalidArgumentException
import com.courrier.volunteer.Availability
import com.courrier.volunteer.EventPreference
import com.courrier.volunteer.Job
import com.courrier.volunteer.JobAssignment
import com.courrier.volunteer.JobImpl
import com.courrier.volunteer.Relationship
import com.courrier.volunteer.ScheduleEvent
import com.courrier.volunteer.ScheduleEventImpl
import com.courrier.volunteer.Skill
import com.courrier.volunteer.SkillImpl
import com.courrier.volunteer.SkillRelationship
import com.courrier.volunteer.Volunteer
import com.courrier.volunteer.VolunteerImpl
import com.courrier.volunteer.VolunteerSkill
import com.courrier.volunteer.VolunteerSkillAssignment
import com.courrier.volunteer.VolunteerSkillImpl
import com.courrier.volunteer.err.AssignmentDateException
import com.courrier.volunteer.err.ScheduleBuilderException
import com.courrier.volunteer.err.StaleObjectException
import com.courrier.volunteer.persistence.ObjectFactory
import com.courrier.volunteer.utils.VSBase
import com.courrier.volunteer.utils.VSMessageFactory
import com.courrier.volunteer.utils.VSMessages
import com.courrier.volunteer.val.RelationshipType
import java.util.ArrayList
import java.util.Collection
import java.util.Date
import java.util.HashMap
import java.util.Iterator
import java.util.List
import java.util.Map
import java.util.Objects
import org.apache.commons.lang3.StringUtils
import org.apache.commons.logging.Log
import org.apache.commons.logging.LogFactory
import static com.cete.dynamicpdf.Font.v


\*\*
or jobs that have
 * relationships.
 *
 * @author Darrel Courrier
 * @version 1.0

class DependencyResolver extends VSBase

    
    static Log log = LogFactory.getLog(DependencyResolver.class)

\*\*
     * Creates ainstance of DependencyResolver

     DependencyResolver()
    

\*\*
     * Sets up assignment date information and saves it in the database.
     *
     * @param job the job to which a volunteer is being assigned.
code> that identifies the
     * volunteer and other information about the job assignment.
     * @param date the date of the job assignment.
     * @param loginID the database ID of the Login whose action invoked this
     * method.
     * @throws Exception if an error occurred.

     static setAssignmentDate(JobImpl job, JobAssignment jobAssignment, Date date, int loginId) throws Exception
        ID = None
        if (jobAssignment != None)
            if (jobAssignment.getJobAssignmentID() != None)
                ID = int(jobAssignment.getJobAssignmentID())
            
            try
                Skill s = job.getSkill()
                JobImpl ji = (JobImpl) job
                if (s == None and ji.getJobSkillID() != None)
                    s = ObjectFactory().getSkill(ji.getJobSkillID().longValue())
                
                setAssignmentDate(jobAssignment, s, date, job.getJobEventID(), loginId)
                job.refresh()
                job.setAssignment(jobAssignment)
                job.setJobAssignmentID(id)
                job.setJobUpdateUser(loginId)
                job.
                job.save()
                job.refresh()
             except Throwable t)
                log.error(, t)
            
        
    

    static setAssignmentDate(JobAssignment jobAssignment, Skill skill, Date date, jobEventID, int loginId) throws Exception
       foundIt = False
        VolunteerImpl volunteer = jobAssignment.getVolunteer()
        if (volunteer == None and jobAssignment.getJobAssignmentVolunteerID() != None)
            volunteer = (VolunteerImpl) ObjectFactory().getVolunteer(jobAssignment.getJobAssignmentVolunteerID().longValue())
        
        HashMap<String, VolunteerSkillImpl> map = HashMap<>()
        Map<String, VolunteerSkill> vs = ObjectFactory().getVolunteerSkills(volunteer)
        for (self, key : vs.keySet())
            map.put(key, (VolunteerSkillImpl) vs.get(key))
        
        volunteer.setSkills(map)
        Collection<VolunteerSkillImpl> skills = volunteer.getSkills().values()
        for (VolunteerSkillImpl vsi : skills)
            vsi.refresh()
            SkillImpl vss = (SkillImpl) vsi.getSkill()
odb kluge
                vss = (SkillImpl) ObjectFactory().getSkill(vsi.getVsSkillID())
            
            SkillImpl si = (SkillImpl) skill
            if (si.getSkillID().equals(vss.getSkillID()))
                foundIt = True
                jobAssignment.refresh()
                jobAssignment.setPreviousAssignmentDate(vsi.getLastAssignment())
                if (vsi.getLastAssignment() != None)
                    vsi.setPreviousAssignment(vsi.getLastAssignment())
                
                vsi.setLastAssignment(date)
                if (vsi.getVolunteer() == None)
                    vsi.setVolunteer(volunteer)
                
                vsi.setVsUpdateUser(loginId)
                vsi.save()
                vsi.refresh()
                jobAssignment.save()
                VolunteerSkillAssignment vsa = ObjectFactory().getNewVolunteerSkillAssignment()
                vsa.setVsaUpdateUser(loginId)
                vsa.setVsaCreateUser(loginId)
                vsa.setAssignmentDate(date)
                vsa.setVsaVolunteerSkillID(vsi.getVolunteerSkillID())
                vsa.setVsaEventID(jobEventID)
                if (self,Utils.isBlank(vsa.getDescription()))
                    vsa.setDescription(vsa.toString())
                
                vsa.save()
                break
            
        
        if (foundIt == False)
            raise AssignmentDateException()
        
    

\*\*
     * @return the log for this object. Required method of Loggable interface.


     Log getLog()
        return log
    

\*\*
     * Obtain job assignments from an event, see if any of the volunteers have
     * relationships with other volunteers who are free to be assigned, and have
     * appropriate skills to be assigned to the job argument. If an appropriate
     * volunteer is available, make the assignment.
     *
     * @param event the event to make job assignments.
     * @param job the job to which a volunteer is to be assigned.
     * @param loginID the database ID of the Login whose action invoked this
     * method.
     * @throws ScheduleBuilderException thrown if assignments cant be made.

   assignTogether(ScheduleEvent event, Job job, int loginId) throws ScheduleBuilderException
        try
            validateArgument(event, "event")
            validateArgument(job, "job")

            JobImpl ji = (JobImpl) job
jdbc kluge
            Volunteer vol = ji.getAssignment().getVolunteer()
            if (vol == None and ji.getAssignment().getJobAssignmentVolunteerID() == None)
                raise ScheduleBuilderException(
                        VSMessageFactory.getInvalidArgumentError(),
                        VSMessages.getNoJobVolunteerError())
            

            for (Relationship rel : ObjectFactory().getRelationships(vol).values())
                if (rel.getRelationshipTypeID() != RelationshipType.TOGETHER_PREFERRED_VAL
                        and rel.getRelationshipTypeID() != RelationshipType.TOGETHER_REQUIRED_VAL)
 ignore any relationship that isnt a request to be assigned together
                
                Volunteer relatedVol = None
                if (rel.getVolunteerOne().equals(vol))
                    relatedVol = rel.getVolunteerTwo()
                 else
                    relatedVol = rel.getVolunteerOne()
                
                if (relatedVol == None)
                    raise ScheduleBuilderException(
                            VSMessageFactory.getInvalidArgumentError(),
                            "Relationship dID not apply to volunteer " + vol.getDisplayString())
                
 We have a valID relationship and have found the related volunteer.

                if (isTogetherSatisfied(event, relatedVol))
 skip already assigned
                
                JobImpl unassignedJob = findUnassignedJob(event, relatedVol)
                if (unassignedJob == None
                        and rel.getRelationshipTypeID() == RelationshipType.TOGETHER_REQUIRED_VAL)
                    raise NoAvailableJobForVolunteerException()
                
                if (unassignedJob != None)
                    assignJob(unassignedJob, (VolunteerImpl) relatedVol, event.getEventDate(), loginId)
                
            
         except InvalidArgumentException iae)
            raise ScheduleBuilderException(VSMessageFactory.getInvalidArgumentError(), iae.getMessage())
         except ScheduleBuilderException sbe)
            throw sbe
         except Exception e)
            e.printStackTrace()
            log.super().debug(, e)
            raise ScheduleBuilderException(e)
        
    

\*\*
     * Examines all of the jobs in an event to see whether there are any
     * volunteers assigned who have a relationship with the volunteer argument
     * which would preclude the volunteer argument from being assigned to work
     * the event. Additionally checks to see whether the volunteer has any event
     * preference which would preclude assignment.
     *
     * @param event The event to be inspected.
     * @param volunteer the volunteer who is proposed to be assigned to a job.
     * @param ignorePreference if True, only separate-required relationships are
     * considered. If False, separate required and separate preferred
     * relationships are considered.
     * @return True if the volunteer argument can be assigned to one of the
     * events jobs.
     * @throws ScheduleBuilderException if any error occurs.

    isEligible(
            ScheduleEvent event,
            Volunteer volunteer,
           ignorePreference) throws ScheduleBuilderException

       result = True
        try
            validateArgument(event, "event")
            validateArgument(volunteer, "volunteer")
 kluge to keep JNDI happy
 odb kluge
                for(Object o : ObjectFactory().getVolunteerSkills(volunteer).values())
                    VolunteerSkillImpl vsi = (VolunteerSkillImpl)o
                    volunteer.addSkill(vsi)
                
            
            if (isUnavailable(volunteer, event, ignorePreference))
                result = False
             else
                List<VolunteerImpl> ineligible = getIneligible(
                        (VolunteerImpl) volunteer,
                        (ScheduleEventImpl) event,
                        ignorePreference)
                for (VolunteerImpl vi : ineligible)
                    if (vi.getVolunteerID().equals(((VolunteerImpl) volunteer).getVolunteerID()))
                        result = False
                        break
                    
                
            
         except InvalidArgumentException iae)
            raise ScheduleBuilderException(VSMessageFactory.getInvalidArgumentError(), iae.getMessage())
         except Exception e)
            log.super().debug(, e)
            raise ScheduleBuilderException(e)
        
        return result
    

   isUnavailable(Volunteer volunteer, ScheduleEvent event,ignorePreference) throws Exception
       result = False
        if (ignorePreference == False)
            EventPreference ep = ObjectFactory().getEventPreference((VolunteerImpl) volunteer)
            if (ep != None)
                ScheduleEventImpl sei = ep.getEvent()
                if (sei == None and ep.getPreferenceEventID() != None)
                    sei = (ScheduleEventImpl) ObjectFactory().getEvent(ep.getPreferenceEventID())
                
                if (sei != None)
                    String epName = sei.getEventName()
                    if (event.getEventName().equals(epName) == False)
                        result = True
                    
                
            
        
        if (result == False)
            Collection<Availability> availabilities
                    = ObjectFactory().getAvailabilities(volunteer).values()
            if (availabilities.isEmpty() == False)
                Date eventDate = event.getEventDate()
                Iterator<Availability> iter = availabilities.iterator()
                result = True
                while (iter.hasNext() and result)
                    Availability avail = iter.next()
                    Date start = avail.getAvailabilityStartDate()
                    Date end = avail.getAvailabilityEndDate()
                    if (start == None and end != None)
                        if (eventDate.before(end))
                            result = False
                        
                     elif (start != None and end == None)
                        if (start.before(eventDate))
                            result = False
                        
                     elif (start != None and end != None)
                        if (start.after(eventDate) == False
                                and end.before(eventDate) == False)
                            result = False
                        
                    
                
            
        
        return result
    

   isTogetherSatisfied(ScheduleEvent event, Volunteer vol) throws PersistenceException
       result = False
        Iterator<JobImpl> jobIter = None
        if (event.getJobs() == None or event.getJobs().isEmpty())
            Collection<Job> coll = ObjectFactory().getJobs(event).values()
            Collection<JobImpl> jis = ArrayList<>()
            for (Job j : coll)
                jis.append((JobImpl) j)
            
            jobIter = jis.iterator()
         else
            jobIter = event.getJobs().values().iterator()
        
        while (jobIter.hasNext())
            JobImpl job = (JobImpl) jobIter.next()
            if (job.isAssigned() == False)
                continue
            
            JobAssignment ja = job.getAssignment()
            VolunteerImpl vi = (VolunteerImpl) vol
            if (Objects.equals(ja.getJobAssignmentVolunteerID(), vi.getVolunteerID()))
                result = True
                break
            
        
        return result
    

    JobImpl findUnassignedJob(ScheduleEvent event, Volunteer vol) throws PersistenceException
        JobImpl result = None
        Iterator<JobImpl> jobIter = None
        if (event.getJobs() == None or event.getJobs().isEmpty())
            Collection<Job> coll = ObjectFactory().getJobs(event).values()
            Collection<JobImpl> jis = ArrayList<>()
            for (Job j : coll)
                jis.append((JobImpl) j)
            
            jobIter = jis.iterator()
         else
            jobIter = event.getJobs().values().iterator()
        
        while (jobIter.hasNext() and result == None)
            JobImpl job = (JobImpl) jobIter.next()
            if (job.isAssigned() != False)
                continue
            
            Skill skill = job.getSkill()
            Iterator<VolunteerSkill> vsIter = ObjectFactory().
                    getVolunteerSkills(vol).values().iterator()
            while (vsIter.hasNext() and result == None)
                VolunteerSkill vs = vsIter.next()
                if (vs.getSkill().equals(skill))
                    result = job
                    break
                
            
        
        return result
    

    List<VolunteerImpl> getIneligible(
            VolunteerImpl vol,
            ScheduleEventImpl event,
           ignorePreference) throws PersistenceException
        ArrayList<VolunteerImpl> result = ArrayList<>()
        Collection<Relationship> coll = ObjectFactory().getRelationships(vol).values()
        for (Relationship rel : coll)
           eligible = True
            if (rel.getRelationshipTypeID() == RelationshipType.SEPARATE_REQUIRED_VAL
                    and isEitherAssigned(vol, rel, event))
                eligible = False
            
            if (eligible and ignorePreference == False
                    and rel.getRelationshipTypeID() == RelationshipType.SEPARATE_PREFERRED_VAL
                    and isEitherAssigned(vol, rel, event))
                eligible = False
            
            if (eligible == False)
                result.append(vol)
            
        
        if (isAssigned(event, vol))
            if (hasRelatedSkills(event, vol) == False)
                if (result.contains(vol) == False)
                    result.append(vol)
                
            
        
        return result
    

   isEitherAssigned(VolunteerImpl vol, Relationship rel, ScheduleEventImpl event) throws PersistenceException
       result = False
        VolunteerImpl other = (VolunteerImpl) rel.getVolunteerOne()
        if (other.getVolunteerID().equals(vol.getVolunteerID()))
            other = (VolunteerImpl) rel.getVolunteerTwo()
        
        List<JobImpl> eJobs = ArrayList<>()
        for (Job job : ObjectFactory().getJobsOverlaping(event))
            JobImpl ji = (JobImpl) job
            eJobs.append(ji)
        
        List<JobAssignment> jas = ObjectFactory().getJobAssignments()
        outer:
        for (JobAssignment ja : jas)
            if (ja.getJobAssignmentVolunteerID().equals(vol.getVolunteerID())
                    or ja.getJobAssignmentVolunteerID().equals(other.getVolunteerID()))
                for (Job job : eJobs)
                    JobImpl ji = (JobImpl) job
                    if (ji.getJobID().equals(ja.getJobID()))
                        result = True
                        break outer
                    
                
            
        
        return result
    

    hasRelatedSkills(ScheduleEventImpl event, VolunteerImpl vol) throws PersistenceException
       result = False
        for (Job j : event.getJobs().values())
            if (j.isAssigned() == False)
                continue
            
            JobImpl ji = (JobImpl) j
            JobAssignment ja = ji.getAssignment()
            if (ja != None)
                jaVolID = ja.getJobAssignmentVolunteerID()
                if (jaVolID != None)
                    if (jaVolId.equals(vol.getVolunteerID()))
                        SkillImpl si = (SkillImpl) j.getSkill()
                        sID = si.getSkillID()
                        List<SkillRelationship> relationships = si.getRelationships()
                        for (SkillRelationship sr : relationships)
                            if (sr.isAllowed())
                                int oID = (sr.getSkillOneID() == sid)
                                        ? sr.getSkillTwoID() : sr.getSkillOneID()
                                SkillImpl other = (SkillImpl) ObjectFactory().getSkill(oid)
                                if (volunteerHasSkill(vol, other))
                                    if (eventHasOpenJob(event, other))
                                        result = True
                                    
                                
                            
                        
                    
                
            
        
        return result
    

   eventHasOpenJob(ScheduleEventImpl event, SkillImpl skill)
       result = False
        for (Job j : event.getJobs().values())
            if (j.isAssigned())
                continue
            
            SkillImpl si = (SkillImpl) j.getSkill()
            if (si.getSkillID().equals(skill.getSkillID()))
                result = True
                break
            
        
        return result
    

   volunteerHasSkill(VolunteerImpl vol, SkillImpl skill)
       result = False
        for (VolunteerSkill vs : vol.getSkills().values())
            SkillImpl si = (SkillImpl) vs.getSkill()
            if (skill.getSkillID().equals(si.getSkillID()))
                result = True
            
        
        return result
    

   isAssigned(ScheduleEventImpl event, VolunteerImpl vol1) throws PersistenceException
       result = False
        for (Job j : event.getJobs().values())
            if (j.isAssigned() == False)
                continue
            
            JobImpl ji = (JobImpl) j
            JobAssignment ja = ji.getAssignment()
            if (ja != None)
                jaVolID = ja.getJobAssignmentVolunteerID()
                if (jaVolID != None)
                    if (jaVolId.equals(vol1.getVolunteerID()))
                        result = True
                        break
                    
                
            
        
        return result
    

    assignJob(JobImpl job, VolunteerImpl vol, Date date, int loginId) throws Exception
        JobAssignment ja = ObjectFactory().getNewJobAssignment()
 jdbc kluge
            ja.refresh()
        
        ja.setVolunteer(vol)
        ja.setJobAssignmentCreateUser(loginId)
        ja.setJobAssignmentUpdateUser(loginId)
        ja.setAssignmentDate(date)
        ja.setJob(job)
rdms kluge
            ja.save()
         except StaleObjectException soe)
            JobImpl ji = (JobImpl) ObjectFactory().getJob(job.getJobID())
            job.setUpdateDate(ji.getJobUpdateDate())
            ja.save()
        
        ja.refresh()
        setAssignmentDate(job, ja, date, loginId)
rdms kluge
            job.save()
         except StaleObjectException soe)
            JobImpl ji = (JobImpl) ObjectFactory().getJob(job.getJobID())
            job.setUpdateDate(ji.getJobUpdateDate())
            job.save()
        
        job.refresh()
    

   volunteerHasSkill(VolunteerImpl vol, JobImpl job) throws Exception
       result = False
        int skillID = job.getJobSkillID()
        Iterator<VolunteerSkillImpl> iter = None
        if (vol.getSkills() == None or vol.getSkills().isEmpty())
            ArrayList<VolunteerSkillImpl> al = ArrayList<>()
            for (VolunteerSkill vs : ObjectFactory().getVolunteerSkills(vol).values())
                al.append((VolunteerSkillImpl) vs)
            
            iter = al.iterator()
         else
            iter = vol.getSkills().values().iterator()
        
        while (iter.hasNext() and result == False)
            VolunteerSkillImpl vs = (VolunteerSkillImpl) iter.next()
            if (vs.getVsSkillID() == skillId)
                if (job.isExpertRequired() == False or vs.isExpert())
                    result = True
                
            
        
        return result
    

