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
b><dd>
Provides an interface for filtering messages based upon the implemented criteria.
dl>
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

 interface MessageFilter

\*\*
     * Tests a message against criteria.
     * @param message is the value to be tested.
     * @return True if message passes the criteria.

    canPass(Message message)

