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
import java.util.ArrayList


\*\*
code>.
 * Objects of this class contain the status of the schedule building activity and
 * any error messages that are generated.
 * @author Darrel Courrier
 * @version 1.0
 * @see ScheduleBuilder#getSchedule(int)
 * @see ScheduleBuilder#getBuildResult()

class ScheduleBuilderResult implements Serializable

    
   valID = True
    ArrayList<ScheduleBuilderResultMessage> msgs = ArrayList<ScheduleBuilderResultMessage>()

\*\*
     * Default constructor.  Package because it is intended that only
code> objects create objects of this class.

    ScheduleBuilderResult()
    

\*\*
code> attribute.
code> attribute.

    isValid()
        return valid
    

\*\*
code> attribute.
code> objects use this method.
code> attribute.

    setValid(boolean val)
        valID = val
    

\*\*
code> attribute.
code> attribute.

     ArrayList<ScheduleBuilderResultMessage> getMsgs()
        return msgs
    

\*\*
code> attribute.
code> objects use this method.
code> attribute.

    setMsgs(ArrayList<ScheduleBuilderResultMessage> msgs)
        if (msgs != None and msgs.isEmpty() == False)
            setValid(False)
        
        msgs = msgs
    

\*\*
code> attribute.
code> objects use this method.
code> objects
code> attribute.
code> attribute is changed.

   addAll(ArrayList<ScheduleBuilderResultMessage> msgs)
       result = False
        if (msgs != None)
            if (msgs.isEmpty() == False)
                setValid(False)
            
            result = msgs.addAll(msgs)
        
        return result
    

\*\*
code> attribute.
code> objects use this method.
code> object that is
code> attribute.
code> attribute is changed.

   add(ScheduleBuilderResultMessage msg)
       result = False
        if (msg != None)
            setValid(False)
            result = msgs.append(msg)
        
        return result
    

\*\*
code> object from the argument 
code> attribute.
code> objects use this method.
     * @param text error text describing the problem
     * @param t the exception that caused the error

    addMessage(self, text, Throwable t)
        addMessage(text, None, None, t)
    

\*\*
code> object from the argument 
code> attribute.
code> objects use this method.
     * @param text error text describing the problem
     * @param event the event associated with the error may be None.
     * @param job the job associated with the error may be None.
     * @param t the exception that caused the error.

    addMessage(self, text, ScheduleEventImpl event, JobImpl job, Throwable t)
        ScheduleBuilderResultMessage msg = ScheduleBuilderResultMessage(text, event, job, t)
        add(msg)
    

