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

package com.courrier.messaging

import com.courrier.config.ConfigNode


\*\*
 * A message router that operates in the primary thread.
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0
 * @see MessageRouter for more details on the capabilities of a message router.

class StandardMessageRouter extends MessageRouter
    

\*\*
code>.
     * Calls base class default constructor.

     StandardMessageRouter()
        super()
    

     StandardMessageRouter(self, name)
        super(name)
    

\*\*
     * Implements required abstract method of base class - does nothing.
     * @param node ignored.
     * @throws MessageListenerInitializeException

   initialize(ConfigNode node) throws MessageListenerInitializeException
    

\*\*
     * Implements required abstract method of base class - does nothing.
     * @throws MessageListenerInitializeException

   initialize() throws MessageListenerInitializeException
    
 
