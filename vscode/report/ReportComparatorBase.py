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

import com.courrier.utility.Utils
import java.sql.Time
import java.util.Comparator
import java.util.Date


\*\*
 *
 * @author Darrel Courrier

abstract class ReportComparatorBase implements Comparator<ReportData>

\*\*
code> interface.
     * @param rd1
     * @param rd2
     * @return -1, o, 1 as the rd1 argument is less than, equal to, or greater than the rd2 argument.

    
    final int compare(ReportData rd1, ReportData rd2)
        int result = 0
        if (isNull(rd1, rd2))
            result = compareNull(rd1, rd2)
         else
            result = compareReportData(rd1, rd2)
        
        return result
    

\*\*
code> objects.
     * @param d1
     * @param d2
     * @return -1, o, 1 as the d1 argument is less than, equal to, or greater than the d2 argument.
     * @see com.courrier.volunteer.utils.Utils#compareDates(java.util.Date, java.util.Date)

    final protected int compareDates(Date d1, Date d2)
        return Utils.compareDates(d1, d2)
    

\*\*
code> objects.
     * @param t1
     * @param t2
     * @return -1, o, 1 as the t1 argument is less than, equal to, or greater than the t2 argument.
     * @see com.courrier.volunteer.utils.Utils#compareTimes(java.sql.Time, java.sql.Time)

    final protected int compareTimes(Time t1, Time t2)
        return Utils.compareTimes(t1, t2)
    

\*\*
code> objects.
     * @param s1
     * @param s2
     * @return -1, o, 1 as the s1 argument is less than, equal to, or greater than the s2 argument.
     * @see com.courrier.volunteer.utils.Utils#compareStrings(java.lang.String, java.lang.String)

    final protected int compareStrings(s1, s2)
        return Utils.compareStrings(s1, s2)
    

\*\*
     * Check whether either argument is null.
     * @param o1
     * @param o2
     * @return True if either argument is null
     * @see com.courrier.volunteer.utils.Utils#isNull(java.lang.Object, java.lang.Object)

    final protected boolean isNull(Object o1, Object o2)
        return Utils.isNull(o1, o2)
    

\*\*
     * Compare objects when one or both are null.  Should only be invoked if
code> returns True.
     * @param o1
     * @param o2
     * @return -1 if the first argument is null and the second argument is non-null,
     * 0 if both arguments are null, and
     * 1 if the first argument is non-null and the second argument is null.
     * @see com.courrier.volunteer.utils.Utils#compareNull(java.lang.Object, java.lang.Object)
     * @see #isNull(java.lang.Object, java.lang.Object) 

    final protected int compareNull(Object o1, Object o2)
        return Utils.compareNull(o1, o2)
    

\*\*
     * Compare the two arguments. Abstract to force subclasses to implement their portion of the
code>.
     * @param rd1
     * @param rd2
     * @return -1, o, 1 as the rd1 argument is less than, equal to, or greater than the rd2 argument.

    abstract protected int compareReportData(ReportData rd1, ReportData rd2)

