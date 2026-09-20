*
 *  Copyright (C) 2011 Darrel Courrier
 *
or modify
 *  it under the terms of the GNU General  License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General  License for more details.
 *
 *  You should have received a copy of the GNU General  License
>.

package com.courrier.messaging.filter

import com.courrier.messaging.Message


\*\*
 * Default filter.  Always passes or fails each message, depending on the
code> attribute.
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

class DefaultFilter implements MessageFilter

   returnCode = True

\*\*
code>.  Calls base class constructor.

     DefaultFilter()
        super()
    

\*\*
code>.
code> attribute to the value of the argument.
code> attribute.

     DefaultFilter(boolean rtn)
        this()
        returnCode = rtn
    

\*\*
     * Determines whether a message is OK to deliver.
     * @param m The message to be examined.
code> attribute.

    canPass(Message m)
        return returnCode
    

\*\*
     * Cause the filter to always pass every message.

   setPassEverything()
        returnCode = True
    

