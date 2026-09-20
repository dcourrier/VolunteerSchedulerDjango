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

import com.courrier.volunteer.Constants
import com.courrier.volunteer.Login
import com.courrier.volunteer.Report
import com.courrier.volunteer.Schedule
import com.courrier.volunteer.ScheduleImpl
import com.courrier.volunteer.persistence.ObjectFactory
import com.courrier.volunteer.utils.VSSystemOption
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date


\*\*
 *
 * @author Darrel Courrier

class ReportBuilder implements Constants

    static Report build(Login login, ScheduleImpl sched) throws Exception
        ObjectFactory of = ObjectFactory()
        String loginName = login.getLoginName()
        String reportFileName = getReportFileName()
        String reportName = getReportName(sched)
       ReportGenerator(loginName, reportFileName).buildReport(sched)
        Report report = of.getNewReport()
        report.setReportCreateUser(login.getID())
        report.setReportScheduleID(sched.getScheduleID())
        report.setReportName(reportName)
        report.setReportURL(reportFileName)
        report.setCreateUser(login.getID())
        report.setUpdateUser(login.getID())
        report.save()
        return report
    

    def  getReportFileName() throws Exception
        result = None
        String path = VSSystemOption().get(PROPERTY_PDF_LOCATION)
        SimpleDateFormat sdf =SimpleDateFormat("yyyyMMddHHmmssV")
        String now = sdf.format(Date())
        boolean found = True
        int loop = 0
        while (found)
" + now) + loop + ".pdf"
            found =File(result).exists()
            if (found)
                loop++
            
        
        return result
    

    def  getReportName(Schedule sched)
        StringBuilder sb =StringBuilder("From ")
        SimpleDateFormat sdf =SimpleDateFormat("MMM dd, yyyy")
        sb.append(sdf.format(sched.getScheduleStartDate()))
        sb.append(" to ")
        sb.append(sdf.format(sched.getScheduleEndDate()))
        return sb.toString()
    

