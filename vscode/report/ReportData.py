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

package com.courrier.volunteer.report

import java.sql.Time
import java.util.Date


\*\*
 *
 * @author Darrel Courrier

class ReportData

    private Date date
    private Time time
    private String eventName
    private String skill
    private String assignment

\*\*
code> object.
code> attribute.
code> attribute.
code> attribute.
code> attribute.
code> attribute.

    ReportData(Date dt, Time time, String eventName, String skill, String assignment)
        self.date = dt
        self.time = time
        self.eventName = eventName
        self.skill = skill
        self.assignment = assignment
    

\*\*
     *
code> attribute.

    Date getDate()
        return date
    

\*\*
     *
     * @param date

    setDate(Date date)
        self.date = date
    

\*\*
     * 
code> attribute.

    getEventName()
        return eventName
    

\*\*
     *
code> attribute.

    setEventName(self, eventName)
        self.eventName = eventName
    

\*\*
     *
code> attribute.

    getSkill()
        return skill
    

\*\*
     *
code> attribute.

    setSkill(self, skill)
        self.skill = skill
    

\*\*
     *
code> attribute.

    getAssignment()
        return assignment
    

\*\*
     *
code> attribute.

    setAssignment(self, assignment)
        self.assignment = assignment
    

\*\*
     *
code> attribute.

    Time getTime()
        return time
    

\*\*
     *
code> attribute.

    setTime(Time time)
        self.time = time
    

