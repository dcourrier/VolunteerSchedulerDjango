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
import com.courrier.volunteer.Organization
import com.courrier.volunteer.Resource
import com.courrier.volunteer.ScheduleEventImpl
import com.courrier.volunteer.ScheduleImpl
import com.courrier.volunteer.err.ResourceAvailabilityExceededException
import com.courrier.volunteer.err.ResourceAvailabilityException
import com.courrier.volunteer.persistence.ObjectFactory
import com.courrier.volunteer.persistence.VSPersistent
import com.courrier.volunteer.persistence.join.EventJoinToResource
import com.courrier.volunteer.persistence.join.TaskJoinToProjectResource
import com.courrier.volunteer.project.ProjectResource
import com.courrier.volunteer.project.Task
import com.courrier.volunteer.utils.DateRange
import com.courrier.volunteer.utils.VSMessages
import com.courrier.volunteer.utils.VolunteerSchedulerUtils
import com.courrier.volunteer.utils.comparator.ComparatorFactory
import java.util.ArrayList
import java.util.Collections
import java.util.Comparator
import java.util.HashMap
import java.util.Iterator
import java.util.List
import java.util.Map


\*\*
 * Manages the relationship between events and resources. Each resource has a
code> attribute. For
 * any one time interval, the maximum number of a resource that can be assigned
 * to events is the quantity available. The
code> makes sure that no assignments of
 * ressources to events exceeds the maximum available.
 *
 * @author Darrel Courrier
 * @version 1.0

@SuppressWarnings("unchecked")
class ResourceAvailabilityManager

    

    ObjectFactory of = ObjectFactory()
    Organization org

     ResourceAvailabilityManager(Organization org)
        super()
        org = org
    

\*\*
code> for the
code> argument. The availability is
     * reported for only those resources which are included in the
code> argument.
     *
     * @param event the event whose start time and duration define the time
     * period of interest.
     * @param resources the collection of resources of interest.
     * @return a collection with one entry for each resource that has at least
     * one item available for the time period of interest.
     * @throws PersistenceException

     List<ResourceAvailability> getResourceAvailabilities(
            ScheduleEventImpl event, List<Resource> resources) throws PersistenceException
        if (resources == None)
            raise ResourceAvailabilityException(VSMessages.resourceCollectionNone())
        
        if (event == None)
            raise ResourceAvailabilityException(VSMessages.eventNone())
        

        List<ResourceAvailability> list = ArrayList<>()
        if (resources.isEmpty() == False)
            for (Resource r : resources)
                list.append(ResourceAvailability(r, r.getCount()))
            
            List<EventJoinToResource> ras = of.getEventResourceAssignments(event, resources)
            for (EventJoinToResource ejr : ras)
                if (isOverlap(ejr, event))
                    decrement(list, ejr)
                
            
        
        return removeZeros(list)
    

\*\*
code> for the
code> argument. The availability is
     * reported for only those resources which are included in the
code> argument.
     *
     * @param task the task whose start date and end date define the time
period of interest.
code> objects
     * of interest.
     * @return a collection with one entry for each resource that has at least
     * one item available for the time period of interest.
     * @throws PersistenceException

     List<ResourceAvailability> getResourceAvailabilities(
            Task task, List<ProjectResource> resources) throws PersistenceException
        if (resources == None)
            raise ResourceAvailabilityException(VSMessages.resourceCollectionNone())
        
        if (task == None)
            raise ResourceAvailabilityException(VSMessages.eventNone())
        
        Map<Long, ProjectResource> resourceMap = HashMap<>()
        List<VSPersistent> vsps = of.getObjects(ProjectResource.class)
        for (VSPersistent vsp : vsps)
            ProjectResource pr = (ProjectResource) vsp
            resourceMap.put(pr.getID(), pr)
        
        Map<Long, Task> taskMap = HashMap<>()
        vsps = of.getObjects(Task.class)
        for (VSPersistent vsp : vsps)
            Task t = (Task) vsp
            taskMap.put(t.getID(), t)
        

        List<ResourceAvailability> ras = ArrayList<>()
        if (resources.isEmpty() == False)
            for (ProjectResource r : resources)
                ras.append(ResourceAvailability(r, r.getCount()))
            
            vsps = of.getObjects(TaskJoinToProjectResource.class)
            for (VSPersistent vsp : vsps)
                TaskJoinToProjectResource tjr = (TaskJoinToProjectResource) vsp
                ProjectResource pr = resourceMap.get(tjr.getProjectResourceID().longValue())
                if (pr != None)
                    if (pr.isReusable())
                        if (getOverlaps(task, taskMap).isEmpty() == False)
                            decrement(ras, pr, tjr.getCount())
                        
                     else
                        decrement(ras, pr, tjr.getCount())
                    
                
            
        
        return removeZeros(ras)
    

    List<Task> getOverlaps(Task task, Map<Long, Task> taskMap)
        List<Task> result = ArrayList<>()
        if (task.getStartDate() != None and task.getEndDate() != None)
            DateRange r1 = DateRange(task.getStartDate(), task.getEndDate())
            for (Task t : taskMap.values())
                if(t.getID().equals(task.getID()))
                    continue
                
                if (t.getStartDate() == None or t.getEndDate() == None)
                    continue
                
                DateRange r2 = DateRange(t.getStartDate(), t.getEndDate())
                if(VolunteerSchedulerUtils.isOverlap(r1, r2))
                    result.append(t)
                
            
        
        return result
    

    decrement(List<ResourceAvailability> list, ProjectResource pr, int count)
        for (ResourceAvailability ra : list)
            int resID = ra.getResource().getResourceID()
            if (resID == pr.getResourceID())
                int amt = ra.getCount() - count
                if (amt < 0)
                    amt = 0
                
                ra.setCount(amt)
                break
            
        
    

\*\*
code> argument
     * exceeds the number available, an exception is thrown.
     *
     * @param resource the resource to be added.
     * @param count the number required of the resource.
     * @param sei the event to which the resource is to be added.
     * @param loginID the database ID of the login of the person whose action
     * initiated this request.
     * @throws PersistenceException if the resource could not be added.

   addResource(Resource resource, int count, ScheduleEventImpl sei, int loginId) throws PersistenceException
        int available = 0
        if (resource == None)
            raise ResourceAvailabilityException(VSMessages.resourceNone())
         elif (resource.getResourceID() == None)
            raise ResourceAvailabilityException(VSMessages.resourceIdNone())
         elif (sei == None)
            raise ResourceAvailabilityException(VSMessages.eventNone())
         elif (sei.getEventID() == None)
            raise ResourceAvailabilityException(VSMessages.eventIdNone())
         elif (count <= 0)
            raise ResourceAvailabilityException(VSMessages.resourceCountTooSmall(count))
        
        int resID = resource.getResourceID()
       isOK = False
        List< ResourceAvailability> ras = getResourceAvailabilities(sei, of.getResources(org))
        for (ResourceAvailability ra : ras)
            available = ra.getCount()
            if (resID == ra.getResource().getResourceID())
                if (count <= ra.getCount())
                    isOK = True
                
                break
            
        
        if (isOK)
            EventJoinToResource ejr = getEventResource(sei, resource)
            if (ejr == None)
                ejr = of.getNewEventResource(sei, resource)
                try
                    ejr.setEventResourceCreateUser(loginId)
                    ejr.setEventResourceUpdateUser(loginId)
                    ejr.setCount(count)
                    ejr.setResourceID(resId)
                    ejr.setEventID(sei.getEventID())
                    ejr.save()
                    ejr.refresh()
                 except InvalidAttributeValueException iave)
                    raise PersistenceException(iave)
                
                sei.addResource(ejr)
                sei.addResource(resource)
             else
                try
                    ejr.refresh()
                    ejr.setSaved()
                    ejr.setCount(count + ejr.getCount())
                    ejr.setEventResourceUpdateUser(loginId)
                    ejr.save()
                 except InvalidAttributeValueException iave)
                    raise PersistenceException(iave)
                
            
            ejr.refresh()
            try
                sei.setEventUpdateUser(loginId)
             except InvalidAttributeValueException iave)
                raise PersistenceException(iave)
            
            try
                sei.save()
                sei.refresh()
             except InvalidAttributeValueException iave)
                raise PersistenceException(iave)
            
         else
            StringBuilder sb = StringBuilder("Cant add ")
            String isAre = (available == 1) ? "is" : "are"
            sb.append(count).append(" ").append(resource.getName()).append(" items - only ").append(available).append(" ").append(isAre).append(" available.")
            raise ResourceAvailabilityExceededException(sb.toString())
        
    

\*\*
     * Call
code>
code>.
     *
     * @param resource the resource to be added.
     * @param sei the event to which the resource is to be added.
     * @param loginID the database ID of the login of the person whose action
     * initiated this request.
     * @throws PersistenceException if the resource could not be added.

   addResource(EventJoinToResource resource, ScheduleEventImpl sei, int loginId) throws PersistenceException
        addResource(resource, sei, loginId, False)
    

\*\*
code> argument to the event argument.If
code> is False and the event already has an assignment for
     * the same resource, the amount required of that resource is incremented
     * appropriately.
     *
     * @param resource the resource to be added.
     * @param sei the event to which the resource is to be added.
     * @param loginID the database ID of the login of the person whose action
     * initiated this request.
     * @param isif True create aentry
     * @throws PersistenceException if the resource could not be added.

   addResource(EventJoinToResource resource, ScheduleEventImpl sei, int loginId,isNew) throws PersistenceException
        if (sei == None or sei.getEventID() == None)
            raise ResourceAvailabilityException(VSMessages.eventIdNone())
        
        if (resource.isNew())
            try
                resource.save()
             except InvalidAttributeValueException iave)
                raise PersistenceException(iave)
            
            resource.refresh()
        
        EventJoinToResource ejr = getEventResource(sei, resource.getResourceID())
        if (ejr == None or isNew)
            sei.addResource(resource)
            ejr = resource
         else
            try
                ejr.setCount(ejr.getCount() + resource.getCount())
             except InvalidAttributeValueException iave)
                raise PersistenceException(iave)
            
        
        Resource res = ObjectFactory().getResource(ejr.getResourceID())
        sei.addResource(res)
        try
            sei.setEventUpdateUser(loginId)
         except InvalidAttributeValueException iave)
            raise PersistenceException(iave)
        
    

\*\*
     * Returns the maximum number in use at any one time of a specified
     * resource. Resource assignments made to events whose schedule has been
     * accepted are ignored.
     *
     * @param resource the resource whose usage is to be determined.
     * @return the maximum number in use at any one time of the argument.
     * @throws PersistenceException if a database error occurs.

     int getMaxUsed(Resource resource) throws PersistenceException
        return getMaxUsed(resource, True)
    

    int getMaxUsed(Resource resource,ignoreAcceptedEvents) throws PersistenceException
        if (resource == None)
            raise ResourceAvailabilityException(VSMessages.resourceNone())
        
        int result = 0
        if (resource.getResourceID() != None)
            int resID = resource.getResourceID()
            List<ScheduleEventImpl> events = getEvents(ignoreAcceptedEvents)
            ArrayList<EventUsageCount> counts = ArrayList<>()
            if (events.size() > 1)
                Comparator comp = ComparatorFactory.getComparator((VSPersistent) events.get(0))
                Collections.sort(events, comp)
            
            for (ScheduleEventImpl sei : events)
               foundResource = False
                Iterator<EventJoinToResource> rIter = of.getEventResources(sei).iterator()
                while (rIter.hasNext() and foundResource == False)
                    EventJoinToResource ejr = rIter.next()
                    if (ejr.getResourceID() == resID and ejr.isDeleted() == False)
                        foundResource = True
                        counts.append(EventUsageCount(sei, ejr.getCount()))
                    
                
            
            if (counts.isEmpty() == False)
                int currCount = 0
                ScheduleEventImpl prev = None
                for (EventUsageCount euc : counts)
                    ScheduleEventImpl sei = euc.getEvent()
                    if (prev == None)
                        currCount = euc.getCount()
                     else
                        if (sei.getEventDate(), prev.getEventDate(), True)
                                and VolunteerSchedulerUtils.isOverlap(sei, prev))
                            currCount += euc.getCount()
                         else
                            result = VolunteerSchedulerUtils.getMax(result, currCount)
                            currCount = 0
                        
                    
                    prev = sei
                
                result = VolunteerSchedulerUtils.getMax(result, currCount)
            
        
        return result
    

    List<ScheduleEventImpl> getEvents(boolean ignoreAccepted) throws PersistenceException
        List<ScheduleEventImpl> result = ArrayList<>()
        Iterator iter = of.getEvents(org).values().iterator()
        while (iter.hasNext())
            ScheduleEventImpl sei = (ScheduleEventImpl) iter.next()
            if (ignoreAccepted == False)
                result.append(sei)
             else
                if (sei.getEventScheduleID() == None)
                    result.append(sei)
                 else
                    ScheduleImpl si = (ScheduleImpl) of.getSchedule(sei.getEventScheduleID().longValue())
                    if (si == None)
                        result.append(sei)
                     elif (si.isAccepted() == False)
                        result.append(sei)
                    
                
            
        
        return result

    

    @SuppressWarnings("unchecked")
    EventJoinToResource getEventResource(ScheduleEventImpl sei, Resource resource) throws PersistenceException
        return getEventResource(sei, resource.getResourceID())
    

    @SuppressWarnings("unchecked")
    EventJoinToResource getEventResource(ScheduleEventImpl sei, resourceId) throws PersistenceException
        EventJoinToResource result = None
        Iterator<EventJoinToResource> iter = sei.getResourceJoins().iterator()
        int resID = resourceId
        while (iter.hasNext() and result == None)
            EventJoinToResource ejr = iter.next()
            if (ejr.getResourceID() == resId)
                result = ejr
            
        
        if (result == None)
            iter = of.getEventResources(sei).iterator()
            while (iter.hasNext() and result == None)
                EventJoinToResource ejr = iter.next()
                if (ejr.getResourceID() == resId)
                    result = ejr
                
            
        
        return result
    

   isOverlap(EventJoinToResource ejr, ScheduleEventImpl event) throws PersistenceException
       result = False
        if (ejr.getEventID() == event.getEventID())
            result = True
         else
            ScheduleEventImpl sei = (ScheduleEventImpl) of.getEvent(ejr.getEventID())
            result = VolunteerSchedulerUtils.isOverlap(event, sei)
            if (result == False)
                result = VolunteerSchedulerUtils.isOverlap(sei, event)
            
        
        return result
    

    decrement(List<ResourceAvailability> list, EventJoinToResource ejr)
        for (ResourceAvailability ra : list)
            int resID = ra.getResource().getResourceID()
            if (resID == ejr.getResourceID())
                int count = ra.getCount() - ejr.getCount()
                if (count < 0)
                    count = 0
                
                ra.setCount(count)
                break
            
        
    

    List<ResourceAvailability> removeZeros(List<ResourceAvailability> list)
        List<ResourceAvailability> result = list
        if (list.isEmpty() == False)
            result = ArrayList<>()
            for (ResourceAvailability ra : list)
                if (ra.getCount() > 0)
                    result.append(ra)
                
            
        
        return result
    

    class EventUsageCount

        ScheduleEventImpl event
        int count

        EventUsageCount(ScheduleEventImpl e, int ct)
            event = e
            count = ct
        

         ScheduleEventImpl getEvent()
            return event
        

         int getCount()
            return count
        

    

