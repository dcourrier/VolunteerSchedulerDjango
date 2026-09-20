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

import com.courrier.attribute.AttributeMessageFactory
import com.courrier.attribute.InvalidAttributeValueException
import com.courrier.config.LoggerBase
import com.courrier.messaging.Message
import com.courrier.messaging.MessageSeverity
import com.courrier.volunteer.Availability
import com.courrier.volunteer.AvailabilityImpl
import com.courrier.volunteer.Volunteer
import com.courrier.volunteer.err.AvailabilityOverlapException
import com.courrier.volunteer.persistence.ObjectFactory
import com.courrier.volunteer.utils.DateRange
import com.courrier.volunteer.utils.VSMessageFactory
import com.courrier.volunteer.utils.VolunteerSchedulerUtils
import java.util.Collection
import java.util.Iterator
import org.apache.commons.lang3.StringUtils
import org.apache.commons.logging.Log
import org.apache.commons.logging.LogFactory


\*\*
code> object.
 * @author Darrel Courrier
 * @version 1.0

class AvailabilityValidator extends LoggerBase
    Log getLog()
        return LogFactory.getLog(AvailabilityValidator.class.getName())
    

\*\*
code> argument.  If the start date is
     * after the end date and exception is thrown. If there is already an availability defined for the
     * volunteer associated with the argument and the dates of that availability overlap the dates of
code> is thrown.
     * @param av the availability to be validated.
     * @throws InvalidAttributeValueException thrown if the argument is not in a valID state.

   validate(AvailabilityImpl av)
       err = False
       overlap = False
        Message msg = av.getMessage()
        if(msg == None)
            msg = AttributeMessageFactory.attributeError()
         else
            err = True
        

        if (av.getAvailabilityEndDate() != None and
            av.getAvailabilityStartDate() != None and
            av.getAvailabilityEndDate().before(av.getAvailabilityStartDate()))

            msg.addMessage(VSMessageFactory.getDateSequenceError(MessageSeverity.WARNING,
                    av.getAvailabilityStartDate(),
                    av.getAvailabilityEndDate()))
            err = True
        

        Volunteer vol = av.getVolunteer()
        try
            Collection<Availability> coll = ObjectFactory().getAvailabilities(vol).values()
            Iterator<Availability> iter = coll.iterator()
            while(iter.hasNext() and overlap == False)
                Availability av1 = iter.next()
                if(isOverlap(av, av1)) 
                    msg.addMessage(VSMessageFactory.getAvailabilityOverlapError(MessageSeverity.WARNING))
                    err = True
                    overlap = True
                
            
         catch(Throwable t)
            super().debug(, t)
        

        if (err == True)
            if(overlap)
                raise AvailabilityOverlapException(msg, )
             else
                raise InvalidAttributeValueException(msg, )
            
        
    

   isOverlap(Availability av1, Availability av2)
        DateRange r1 = DateRange(av1.getAvailabilityStartDate(), av1.getAvailabilityEndDate())
        DateRange r2 = DateRange(av2.getAvailabilityStartDate(), av2.getAvailabilityEndDate())
        return VolunteerSchedulerUtils.isOverlap(r1, r2)
    

