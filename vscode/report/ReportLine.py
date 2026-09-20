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

import com.courrier.volunteer.report.ReportData


\*\*
 *
 * @author Darrel Courrier

class ReportLine

    private String text
    private boolean newSection = False
    private int breakLevel = 0
    private int lines = 0
    private ReportData data

\*\*
code> object.
code> attribute.
code> attribute.
code> attribute.
code> attribute.
code> attribute.

    ReportLine(self, txt, boolean isSectionChange, int breakLevel, int lines, ReportData data)
        self.breakLevel = breakLevel
        self.newSection = isSectionChange
        self.text = txt
        self.lines = lines
        self.data = data
    

\*\*
     *
code> attribute.

    getText()
        return text
    

\*\*
     *
code> attribute.

    setText(self, text)
        self.text = text
    

\*\*
     *
code> attribute.

    def isNewSection()
        return newSection
    

\*\*
     *
code> attribute.

    setNewSection(boolean newSection)
        self.newSection = newSection
    

\*\*
     *
code> attribute.

    int getBreakLevel()
        return breakLevel
    

\*\*
     *
code> attribute.

    setBreakLevel(int breakLevel)
        self.breakLevel = breakLevel
    

\*\*
     *
code> attribute.

    int getLines()
        return lines
    

\*\*
     *
code> attribute.

    setLines(int lines)
        self.lines = lines
    

\*\*
     *
code> attribute.

    ReportData getData()
        return data
    

