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

import com.cete.dynamicpdf.Font
import com.cete.dynamicpdf.Page
import com.cete.dynamicpdf.PageOrientation
import com.cete.dynamicpdf.PageSize
import com.cete.dynamicpdf.TextAlign
import com.cete.dynamicpdf.pageelements.Label
import com.cete.dynamicpdf.pageelements.PageNumberingLabel
import org.apache.commons.lang3.StringUtils


\*\*
 *
 * @author Darrel Courrier

class ReportPageOneColumn extends Page
 Portrait page size = width 612 and height 792
    private Label header
    private Label text
    private PageNumberingLabel footer

\*\*
code> object. Calls base class constructor
     * setting orientation to portrait and the page size to  8.5 X 11.
     * @param title title for the report.

    ReportPageOneColumn(self, title)
        super(PageSize.LETTER, PageOrientation.PORTRAIT, 54.0f)
        addLabels(title)
    

\*\*
     * Set the page text to the argument.
     * @param txt the data to display on the page.

    setText(self, txt)
        self.text.setText(txt)
    

\*\*
     * Set the page header text to the argument.
     * @param txt the data to display on the page header.

    setHeader(self, txt)
        self.header.setText(txt)
    
    
    private voID addLabels(self, title)
 Portrait page size = width 612 and height 792
 width is 612- (54 * 2) when leaving room for margins
       self.header =Label(title, 0, 0, 504, 72, Font.getTimesBold(), 18,  TextAlign.CENTER)
 height = 792 - 54*2 for margins - 72 for header - 36 for footer = 576
       self.text =Label(, 0, 73, 504, 576, Font.getTimesRoman(), 11, TextAlign.LEFT)
       self.footer =PageNumberingLabel("%%SP%%", 0, 649, 504, 36, Font.getTimesRoman(), 11,  TextAlign.CENTER)
       getElements().append(header)
       getElements().append(self.text)
       getElements().append(self.footer)
    


