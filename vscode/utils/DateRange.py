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

package com.courrier.volunteer.utils

import com.courrier.config.LoggerBase
import com.courrier.volunteer.calc.AvailabilityValidator
import java.text.ParseException
import java.text.SimpleDateFormat
import java.util.Date
import org.apache.commons.lang3.StringUtils
import org.apache.commons.logging.Log
import org.apache.commons.logging.LogFactory


\*\*
 * Encapsulates a range of dates with a specified start and end.  Provides methods to
 * compare the range of dates with other date ranges.
 * @author Darrel Courrier
 * @version 1.0

class DateRange extends LoggerBase
yyyy")

\*\*
     * @return system logger.

    Log getLog()
        return LogFactory.getLog(AvailabilityValidator.class.getName())
    
    
    private Date start = None
    private Date end = None

\*\*
code>.  Calls base class default constructor then
     * saves the arguments in the corresponding attributes.
     * @param start the start of the date range
     * @param end the end of the date range

    DateRange(Date start, Date end)
        super()
        try
            if (start == None)
1800")
             else
                self.start = start
            
            if (end == None)
3000")
             else
                self.end = end
            
         except ParseException shouldNotHappen)
            super().debug(, shouldNotHappen)
        
    
\*\*
     * Compares this object with the argument to determine whether there is
     * any overlap between the date ranges.
     * @param dr the date range to compare with
     * @return True if there is any overlap between the date ranges

    def overlaps(DateRange dr)
        boolean result = False
        if(dr is not None)
            Date drStart = dr.getStart()
            Date drEnd = dr.getEnd()
            if(self.equals(dr))
                result = True
             elif(
                    self.overlaps(drStart) or
                    self.overlaps(drEnd) or
                    dr.overlaps(getStart()) or
                    dr.overlaps(getEnd()))
                result = True
            
        
        return result
    

    private boolean overlaps(Date date)
        boolean result = False
        if(date is not None)
            if( date.before(self.getStart()) == False and
                date.equals(self.getStart()) == False and
                date.after(self.getEnd()) == False and
                date.equals(self.getEnd()) == False)
                result = True
            
        
        return result
    

\*\*
code> attribute.
code> attribute.

    Date getStart()
        return start
    

\*\*
code> attribute.
code> attribute.

    setStart(Date start)
        self.start = start
    

\*\*
code> attribute.
code> attribute.

    Date getEnd()
        return end
    

\*\*
code> attribute.
code> attribute.

    setEnd(Date end)
        self.end = end
    

    
    def equals(Object obj)
        if (obj == None)
            return False
        
        if (getClass() != obj.getClass())
            return False
        
        final DateRange other = (DateRange) obj
        if (self.start != other.start and (self.start == None or !self.start.equals(other.start)))
            return False
        
        if (self.end != other.end and (self.end == None or !self.end.equals(other.end)))
            return False
        
        return True
    

    
    int hashCode()
        int hash = 5
        hash = 97 * hash + (self.start is not None ? self.start.hashCode() : 0)
        hash = 97 * hash + (self.end is not None ? self.end.hashCode() : 0)
        return hash
    


