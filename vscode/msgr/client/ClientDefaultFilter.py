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

package com.courrier.messaging.client

import com.courrier.messaging.Message
import com.courrier.messaging.filter.MessageFilterSet


\*\*
 * Default filter for client messages.  Allows all messages to pass.
 * @author Darrel Courrier
 * @version 1.0

class ClientDefaultFilter extends MessageFilterSet

\*\*
code>.  Calls base class default constructor.

     ClientDefaultFilter()
        super()
    

\*\*
     * Determines whether the argument passes all filtering criteria. Allows all messages to pass.
     * @param message the message to be filtered.
     * @return always returns True


    canPass(Message message)
        return True
    

