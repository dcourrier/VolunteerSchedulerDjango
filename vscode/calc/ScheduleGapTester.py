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
import com.courrier.volunteer.Organization
import com.courrier.volunteer.Schedule
import com.courrier.volunteer.persistence.ObjectFactory
import com.courrier.volunteer.utils.Loggable
import com.courrier.volunteer.utils.VSBase
import com.courrier.volunteer.utils.VolunteerSchedulerUtils
import java.util.Date
import java.util.Iterator
import org.apache.commons.logging.Log
import org.apache.commons.logging.LogFactory


\*\*
 * Validates date range for schedules.
 * @author  Darrel Courrier

class ScheduleGapTester  extends VSBase implements Loggable
    
    static Log log = LogFactory.getLog(ScheduleGapTester.class)
    
    Organization org
    
\*\*
code>.  Calls base class default constructor.

     ScheduleGapTester()
        super()
    

     ScheduleGapTester(Organization org)
        this()
        org = org
    

\*\*
     * @return the log for this object. Required method of Loggable interface.


     Log getLog()
        return log
    

   setOrg(Organization org)
        org = org
    

\*\*
     * Determines whether a gap would be created if a schedule is built for the date range
     * specified by the arguments.  A gap leaves events which do not have assignments.  Such
code>. The method is
code> objects will invoke it.
     * @param start the start of the date range to be examined.
     * @param end the end of the date range to be examined.
     * @return True if:<ol>
     * <li>there are any events that are not assigned to a schedule whose event date is before the
li>
     * <li>there are any schedules whose date range occurs after the
li>
ol>
     * @throws PersistenceException if a database error occurred.

    isGapCreated(Date start, Date end) throws PersistenceException
       OK = ObjectFactory().getOpenDatesBefore(start, org).isEmpty()
        if(OK == True)
            OK = ObjectFactory().getSchedulesAfter(end, org).isEmpty()
        
        return OK == False
    

\*\*
     * Determines whether a schedule is built for the date range specified by the arguments would have
     * dates that overlap any existing schedule. The method is
code> objects will invoke it.
     * @param start the start of the date range.
     * @param end the end of the date range.
     * @return True if the date range specified by the arguments overlaps the date range of any
     * existing schedule.
     * @throws PersistenceException if a database error occurred.

    isOverlapCreated(Date start, Date end) throws PersistenceException
       result = False
        Iterator iter = ObjectFactory().getSchedules(org).values().iterator()
        while(iter.hasNext() and result == False)
           Schedule schedule = (Schedule)iter.next()
           Date sStart = schedule.getScheduleStartDate()
           Date sEnd = schedule.getScheduleEndDate()
           if(start.after(sEnd))
               continue
           
           if(start, sEnd, True) and
              start, end, True) == False )
               continue
           
           if(end.before(sStart))
               continue
           
           if(end, sStart, True) and
              start, end, True) == False )
               continue
           
           result = True
        
        return result
    

