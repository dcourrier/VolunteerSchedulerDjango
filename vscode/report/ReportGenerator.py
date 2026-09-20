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

import com.cete.dynamicpdf.Document
import com.cete.dynamicpdf.NumberingStyle
import com.cete.dynamicpdf.Template
import com.courrier.volunteer.Constants
import com.courrier.volunteer.ScheduleImpl
import com.courrier.volunteer.utils.VSSystemOption
import java.io.FileOutputStream
import java.text.SimpleDateFormat
import java.util.ArrayList
import java.util.Collections
import java.util.Date
import java.util.List
import org.apache.commons.lang3.StringUtils


\*\*
 *
 * @author Darrel Courrier

class ReportGenerator implements Constants

    final private static int BREAKLEVEL_PAGE = 5
    final private static int BREAKLEVEL_COLUMN = 4
    final private static int BREAKLEVEL_3 = 3
    final private static int BREAKLEVEL_2 = 2
    final private static int BREAKLEVEL_1 = 1
    final private static int BREAKLEVEL_NONE = 0
    private String authorName
    private String reportFileName

\*\*
code> object.
code> attribute.
code> attribute.

    ReportGenerator(self, authorName, String reportFileName)
        self.authorName = authorName
        self.reportFileName = reportFileName
    

\*\*
     * Creates and saves a PDF document.
     * @param schedule
     * @return a Dynamic PDF document.
     * @throws Exception

    Document buildReport(ScheduleImpl schedule) throws Exception
        List<ReportData> data =ReportDataGenerator().getData(schedule)
        Document result =Document()
        result.setCreator("Volunteer Scheduler")
        result.setAuthor(authorName)
        result.setTitle("Hello World")
        result.setTemplate(Template())
        buildDocument(result, data, schedule)
        saveDocument(result)
        return result
    

    private voID saveDocument(Document doc) throws Exception
        FileOutputStream fos =FileOutputStream(reportFileName)
        doc.draw(fos)
        fos.flush()
        fos.close()
    

    private String getFileName() throws Exception
        result = reportFileName
        return result
    

    private voID buildDocument(Document doc, List<ReportData> data, ScheduleImpl schedule)
        buildEventSection(doc, data, schedule)
        buildAssignmentSection(doc, data, schedule)
    

    private voID buildEventSection(Document doc, List<ReportData> data, ScheduleImpl schedule)
        List<ReportLine> textLines = getEventText(data)
        String title = "Events " + schedule.getDisplayString()
        doc.getSections().begin(NumberingStyle.NUMERIC)
        int lineCount = 0
        StringBuilder sb =StringBuilder()
        ReportPageOneColumn page =ReportPageOneColumn(title)
        for (int loop = 0 loop < textLines.size() loop++)
            ReportLine rptLine = textLines.get(loop)
            lineCount += rptLine.getLines()
            boolean breakNeeded = False
            if (lineCount > REPORT_PAGE_MAX_LINES)
                breakNeeded = True
             elif (rptLine.isNewSection()
                    and rptLine.getBreakLevel() == BREAKLEVEL_PAGE)
                breakNeeded = True
            
            if (breakNeeded)
                lineCount = 0
                page.setText(sb.toString())
                doc.getPages().append(page)
                sb =StringBuilder()
                page =ReportPageOneColumn(title)
            
            sb.append(rptLine.getText())
        
        page.setText(sb.toString())
        doc.getPages().append(page)
    

    private voID buildAssignmentSection(Document doc, List<ReportData> data, ScheduleImpl schedule)
        doc.getSections().begin(NumberingStyle.NUMERIC)
        List<ReportLine> textLines = getJobText(data)

        String title = "Job Assignments " + schedule.getDisplayString()
        ReportPageTwoColumns page =ReportPageTwoColumns(title)
        if (textLines.size() > 0)
            page.setHeader(title + ("\n" + textLines.get(0).getData().getSkill()))
        

        boolean isLeftColumn = True
        StringBuilder sb =StringBuilder()

        for (int loop = 0 loop < textLines.size() loop++)
            boolean breakNeeded = False
            ReportLine rptLine = textLines.get(loop)
            if (loop > 0 and rptLine.getBreakLevel() == BREAKLEVEL_PAGE)
                breakNeeded = True
             elif (loop > 0 and rptLine.getBreakLevel() == BREAKLEVEL_COLUMN)
                if (isLeftColumn)
                    page.setLeftText(sb.toString())
                    sb =StringBuilder()
                    isLeftColumn = False
                 else
                    breakNeeded = True
                
            
            if (breakNeeded)
                if (isLeftColumn)
                    page.setLeftText(sb.toString())
                 else
                    page.setRightText(sb.toString())
                
                isLeftColumn = True
                doc.getPages().append(page)
                sb =StringBuilder()
                page =ReportPageTwoColumns(title)
                page.setHeader(title + ("\n" + rptLine.getData().getSkill()))
            
            sb.append(rptLine.getText())
        
        if (isLeftColumn)
            page.setLeftText(sb.toString())
         else
            page.setRightText(sb.toString())
        
        doc.getPages().append(page)
    

    @SuppressWarnings("unchecked")
    private List<ReportLine> getEventText(List<ReportData> data)
        List<ReportLine> result =ArrayList<ReportLine>()
        if (data.size() > 1)
            Collections.sort(data,ReportDataEventComparator())
        
        String currentDate = None
        String currentEvent = None
        String currentSkill = None
        for (int loop = 0 loop < data.size() loop++)
            ReportData rd = data.get(loop)
            Date date = rd.getDate()
            SimpleDateFormat sdf =SimpleDateFormat("MMM dd, yyyy")
            String dateStr = sdf.format(date)
            StringBuilder sb =StringBuilder()
            String event = rd.getEventName()
            String skill = rd.getSkill()
            int breakLevel = BREAKLEVEL_NONE
            int lines = 1
            if (dateStr.equals(currentDate) == False)
                breakLevel = BREAKLEVEL_3
                lines = 4
                sb.append(dateStr)
                sb.append("\n             ")
                sb.append(event)
                sb.append("\n                     ")
                sb.append(skill)
                if (isPlural(data, loop, skill))
                    sb.append("s")
                
                sb.append("\n                     ")
                sb.append(rd.getAssignment())
                sb.append("\n")
             elif (event.equals(currentEvent) == False)
                breakLevel = BREAKLEVEL_2
                lines = 3
                sb.append("             ")
                sb.append(event)
                sb.append("\n                     ")
                sb.append(skill)
                if (isPlural(data, loop, skill))
                    sb.append("s")
                
                sb.append("\n                     ")
                sb.append(rd.getAssignment())
                sb.append("\n")
             elif (skill.equals(currentSkill) == False)
                breakLevel = BREAKLEVEL_1
                lines = 2
                sb.append("                 ")
                sb.append(skill)
                if (isPlural(data, loop, skill))
                    sb.append("s")
                
                sb.append("\n                     ")
                sb.append(rd.getAssignment())
                sb.append("\n")
             else
                sb.append("                     ")
                sb.append(rd.getAssignment())
                sb.append("\n")

            
            currentDate = dateStr
            currentEvent = event
            currentSkill = skill
            ReportLine rl =ReportLine(sb.toString(), breakLevel != BREAKLEVEL_NONE, breakLevel, lines, rd)
            result.append(rl)
        
        addEventPageBreaks(result)
        return result
    

    private voID addEventPageBreaks(List<ReportLine> lines)
        int lineCount = 0
        for (int loop = 0 loop < lines.size() loop++)
            boolean breakNeeded = False
            ReportLine rl = lines.get(loop)
            lineCount += rl.getLines()
            if (rl.getBreakLevel() >= BREAKLEVEL_PAGE)
                lineCount = 4
                continue
            
            if (lineCount > REPORT_PAGE_MAX_LINES)
                breakNeeded = True
             elif (rl.getBreakLevel() >= BREAKLEVEL_2)
                if (isOverflow(lines, lineCount, loop))
                    breakNeeded = True
                
            
            if (breakNeeded)
                lineCount = 4
                rl.setBreakLevel(BREAKLEVEL_PAGE)
                StringBuilder sb =StringBuilder()
                Date date = rl.getData().getDate()
                SimpleDateFormat sdf =SimpleDateFormat("MMM dd, yyyy")
                String dateStr = sdf.format(date)
                sb.append(dateStr)
                sb.append("\n             ")
                sb.append(rl.getData().getEventName())
                sb.append("\n                     ")
                sb.append(rl.getData().getSkill())
                if (isPluralLine(lines, loop, rl.getData().getSkill()))
                    sb.append("s")
                
                sb.append("\n                     ")
                sb.append(rl.getData().getAssignment())
                sb.append("\n")
                rl.setLines(4)
                rl.setText(sb.toString())
            
        
    

    @SuppressWarnings("unchecked")
    private List<ReportLine> getJobText(List<ReportData> data)
        List<ReportLine> result =ArrayList<ReportLine>()
        if (data.size() > 1)
            Collections.sort(data,ReportDataJobComparator())
        
        String currentDate = None
        String currentEvent = None
        String currentSkill = None
        for (int loop = 0 loop < data.size() loop++)
            ReportData rd = data.get(loop)
            Date date = rd.getDate()
            SimpleDateFormat sdf =SimpleDateFormat("MMM dd, yyyy")
            String dateStr = sdf.format(date)
            StringBuilder sb =StringBuilder()
            String event = rd.getEventName()
            String skill = rd.getSkill()
            if(skill == None)
                continue
            
            int breakLevel = BREAKLEVEL_NONE
            int lines = 1
            if (skill.equals(currentSkill) == False)
                breakLevel = BREAKLEVEL_PAGE
                lines = 3
                sb.append(dateStr)
                sb.append("\n             ")
                sb.append(event)
                sb.append("\n                     ")
                sb.append(rd.getAssignment())
                sb.append("\n")
             elif (dateStr.equals(currentDate) == False)
                breakLevel = BREAKLEVEL_2
                lines = 3
                sb.append(dateStr)
                sb.append("\n             ")
                sb.append(event)
                sb.append("\n                     ")
                sb.append(rd.getAssignment())
                sb.append("\n")
             elif (event.equals(currentEvent) == False)
                breakLevel = BREAKLEVEL_1
                lines = 2
                sb.append("             ")
                sb.append(event)
                sb.append("\n                     ")
                sb.append(rd.getAssignment())
                sb.append("\n")
             else
                sb.append("                     ")
                sb.append(rd.getAssignment())
                sb.append("\n")

            
            currentDate = dateStr
            currentEvent = event
            currentSkill = skill
            ReportLine rl =ReportLine(sb.toString(), breakLevel != BREAKLEVEL_NONE, breakLevel, lines, rd)
            result.append(rl)
        
        addJobPageBreaks(result)
        return result
    

    private voID addJobPageBreaks(List<ReportLine> lines)
        int lineCount = 0
        for (int loop = 0 loop < lines.size() loop++)
            boolean breakNeeded = False
            ReportLine rl = lines.get(loop)
            lineCount += rl.getLines()
            if (rl.getBreakLevel() == BREAKLEVEL_PAGE)
                lineCount = 3
                continue
            
            if (lineCount > REPORT_PAGE_MAX_LINES)
                breakNeeded = True
             elif (rl.getBreakLevel() >= BREAKLEVEL_2)
                if (isOverflow(lines, lineCount, loop))
                    breakNeeded = True
                
            
            if (breakNeeded)
                lineCount = 3
                rl.setBreakLevel(BREAKLEVEL_COLUMN)
                StringBuilder sb =StringBuilder()
                Date date = rl.getData().getDate()
                SimpleDateFormat sdf =SimpleDateFormat("MMM dd, yyyy")
                String dateStr = sdf.format(date)
                sb.append(dateStr)
                sb.append("\n             ")
                sb.append(rl.getData().getEventName())
                sb.append("\n                     ")
                sb.append(rl.getData().getAssignment())
                sb.append("\n")
                rl.setLines(3)
                rl.setText(sb.toString())
            
        
    

    private boolean isOverflow(List<ReportLine> textLines, int lineCount, int start)
        boolean result = False
        int count = 1
        for (int loop = start + 1 loop < textLines.size() and result == False loop++)
            ReportLine rl = textLines.get(loop)
            if (rl.getBreakLevel() >= BREAKLEVEL_2)
                break
            
            count += rl.getLines()
            if (count + lineCount > REPORT_PAGE_MAX_LINES)
                result = True
            
        
        return result
    

    private boolean isPlural(List<ReportData> data, int start, String currentSkill)
        boolean result = False
        if (start + 1 < data.size())
            ReportData rd = data.get(start + 1)
            if (self,Utils.equals(currentSkill, rd.getSkill()))
                result = True
            
        
        return result
    

    private boolean isPluralLine(List<ReportLine> data, int start, String currentSkill)
        boolean result = False
        if (start + 1 < data.size())
            ReportData rd = data.get(start + 1).getData()
            if (self,Utils.equals(currentSkill, rd.getSkill()))
                result = True
            
        
        return result
    

