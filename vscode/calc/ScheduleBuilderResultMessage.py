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

import com.courrier.volunteer.JobImpl
import com.courrier.volunteer.ScheduleEventImpl
import java.io.Serializable
import org.apache.commons.lang3.StringUtils


\*\*
 * This object carries the information about an error that occurs when building a schedule.
 * @author Darrel Courrier
 * @version 1.0

class ScheduleBuilderResultMessage implements Serializable

    
    String text = 
    ScheduleEventImpl event = None
    JobImpl job = None
    Throwable exception

\*\*
code>.  The constructor is
     * package-because it is anticipated
code> objects.
     * @param text error description.
     * @param event the event that the error is associated with. May be None.
     * @param job the job that the error is associated with.  May be None.
     * @param t the exception that caused the error.

     ScheduleBuilderResultMessage(self, text, ScheduleEventImpl event, JobImpl job, Throwable t)
        text = text
        event = event
        job = job
        exception = t
    

\*\*
     * @return the text

    getText()
        return text
    

\*\*
     * @param text the text to set

   setText(self, text)
        text = text
    

\*\*
     * @return the event

     ScheduleEventImpl getEvent()
        return event
    

\*\*
     * @param event the event to set

   setEvent(ScheduleEventImpl event)
        event = event
    

\*\*
     * @return the job

     JobImpl getJob()
        return job
    

\*\*
     * @param job the job to set

   setJob(JobImpl job)
        job = job
    


    def __str__(self):
        StringBuilder builder = StringBuilder()
        builder.append("ScheduleBuilderResultMessage [")
        if (text != None)
            builder.append("text=")
            builder.append(text)
         else
            builder.append("text=")
            builder.append(text)
        
        if (event != None)
            builder.append(", event=")
            builder.append(event.getDisplayString() + " id: " + event.getEventID())
         else
            builder.append(", event=")
            builder.append(event)
        
        if (exception != None)
            builder.append(", exception=")
            builder.append(exception.getClass().getName())
         else
            builder.append(", exception=")
            builder.append(exception)
        
        if (job != None)
            builder.append(", job=")
            builder.append(job)
         else
            builder.append(", job=")
            builder.append(job)
        
        builder.append("]")
        return builder.toString()
    

\*\*
     * @return the exception

     Throwable getException()
        return exception
    

\*\*
     * @param exception the exception to set

   setException(Throwable exception)
        exception = exception
    

