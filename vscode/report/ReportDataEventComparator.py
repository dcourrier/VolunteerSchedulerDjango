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

\*\*
 *
 * @author Darrel Courrier

class ReportDataEventComparator extends ReportComparatorBase

\*\*
code> objects by the following fields, date, time, event name, skill.
     * @param rd1
     * @param rd2
     * @return -1, o, 1 as the rd1 argument is less than, equal to, or greater than the rd2 argument.

    
    protected int compareReportData(ReportData rd1, ReportData rd2)
        int result = compareDates(rd1.getDate(), rd2.getDate())
        if(result == 0)
            result = compareTimes(rd1.getTime(), rd2.getTime())
        
        if(result == 0)
            result = compareStrings(rd1.getEventName(), rd2.getEventName())
        
        if(result == 0)
            result = compareStrings(rd1.getSkill(), rd2.getSkill())
        
        return result
    


