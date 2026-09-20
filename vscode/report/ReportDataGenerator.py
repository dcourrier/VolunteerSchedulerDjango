*
 *  Copyright 2011 Darrel Courrier.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License")
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *  under the License.

package com.courrier.volunteer.report

import com.courrier.volunteer.Constants
import com.courrier.volunteer.JobAssignment
import com.courrier.volunteer.JobImpl
import com.courrier.volunteer.ScheduleEvent
import com.courrier.volunteer.ScheduleEventImpl
import com.courrier.volunteer.ScheduleImpl
import com.courrier.volunteer.Volunteer
import com.courrier.volunteer.persistence.ObjectFactory
import java.sql.Time
import java.util.ArrayList
import java.util.Collection
import java.util.Date
import java.util.List


\*\*
 *
 * @author Darrel Courrier

@SuppressWarnings({"unchecked", "CallToThreadDumpStack", "rawtypes")
class ReportDataGenerator implements Constants

    private ObjectFactory of = ObjectFactory()

\*\*
     * Obtain all the data required to generate a report about the argument.
     *
     * @param schedule
     * @return a list containing all information about a schedule.
     * @throws Exception

    List<ReportData> getData(ScheduleImpl schedule) throws Exception
        List<ReportData> result =ArrayList<>()
        List<ScheduleEvent> events = of.getEvents(schedule)
        for (int loop = 0 loop < events.size() loop++)
            ScheduleEventImpl sei = (ScheduleEventImpl) events.get(loop)
            getData(sei, result)
        
        return result
    

    private voID getData(ScheduleEventImpl event, List<ReportData> data) throws Exception
        Date date = event.getEventDate()
        String name = event.getEventName()
        Collection jobs = of.getJobs(event).values()
        if (jobs.isEmpty())
            ReportData rd =ReportData(
                    date,
                    Time.valueOf(event.getEventStartTime()),
                    name,
                    null,
                    null)
            data.append(rd)
         else
            for (Object job : jobs)
                String volName = "unassigned"
                JobImpl ji = (JobImpl) job
                JobAssignment ja = ji.getAssignment()
                if (ja is not None)
                    Volunteer vol = ja.getVolunteer()
                    if (vol is not None)
                        volName = vol.getDisplayString()
                    
                
                ReportData rd =ReportData(
                        date,
                        Time.valueOf(event.getEventStartTime()),
                        name,
                        ji.getSkill().getSkillName(),
                        volName)
                data.append(rd)
            
        
    

