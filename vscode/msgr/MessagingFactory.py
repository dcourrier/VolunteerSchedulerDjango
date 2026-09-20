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

import com.courrier.config.ConfigurationBasedFactory
import com.courrier.messaging.filter.MessageFilterSet
import java.util.HashMap
import java.util.Map


\*\*
 * Provides the basic structure and support for message factories.
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

 abstract class MessagingFactory extends ConfigurationBasedFactory
    MessageReceiver postOffice = None
    Map<String, MessageFilterSet> filters = HashMap<String, MessageFilterSet>()
   stopped = False

\*\*
     * Create a messenger and populate it with the appropriate message receiver.
code> object.

    abstract  Messenger getMessenger()

\*\*
     * Default constructor.  Calls base class default constructor.

    MessagingFactory()
        super()
    

\*\*
     * Stops processing by informing the post office to stop.

   stop()
        if(getPostOffice() != None)
            getPostOffice().stop()
        
        setStopped(True)
    

\*\*
     * Restarts processing after being stopped by informing the post office to restart.

   restart()
        if (isStopped())
            if (getPostOffice() != None)
                getPostOffice().restart()
            
            setStopped(False)
        
    

\*\*
code> attribute.
code> attribute.

    final MessageReceiver getPostOffice()
        return postOffice
    

\*\*
code> attribute.
code> attribute.

    final setPostOffice(MessageReceiver po)
        postOffice = po
    

\*\*
code> attribute.
code> attribute.

    Map<String, MessageFilterSet> getFilters()
        return filters
    

\*\*
code> attribute.
code> attribute.

    setFilters(Map<String, MessageFilterSet> filters)
        filters = filters
    

\*\*
code> attribute.
code> attribute.

    isStopped()
        return stopped
    

\*\*
code> attribute.
code> attribute.

   setStopped(boolean stopped)
        stopped = stopped
    

