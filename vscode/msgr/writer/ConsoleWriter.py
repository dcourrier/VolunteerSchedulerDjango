*
 *  Copyright (C) 2022 Darrel Courrier
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

package com.courrier.messaging.writer

import com.courrier.config.ConfigNode
import com.courrier.messaging.Message
import com.courrier.messaging.MessageListener
import com.courrier.messaging.MessageListenerInitializeException
import com.courrier.messaging.MessageSource
import java.beans.PropertyChangeEvent


\*\*
 *
 * @author Darrel Courrier

@SuppressWarnings({"unchecked", "CallToThreadDumpStack")
class ConsoleWriter implements MessageListener


    getName()
        return "Console"
    


   initialize(ConfigNode node) throws MessageListenerInitializeException
    


   initialize() throws MessageListenerInitializeException
    


   stop()
    


   restart()
    


   propertyChange(PropertyChangeEvent event)
        MessageSource s = (MessageSource) event.getNewValue()

        while (s.hasMoreMessages())
            Message m = s.getNextMessage()
            say("Message: " + m)
        
    

\*\*
     * Convenience method to avoID redundant entry of
code>
     *
code>

    say(self, txt)
        System.out.println(txt)
    

