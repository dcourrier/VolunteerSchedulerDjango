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
import java.beans.PropertyChangeEvent
import java.io.Serializable
import java.util.ArrayList
import java.util.Iterator
import java.util.List
import org.apache.commons.logging.Log
import org.apache.commons.logging.LogFactory


\*\*
 * Abstract class which provides common behavior for message routers.
code> implementations.  The router is a
code> objects
code>  implementation.  The router obtains messages from
code>.
 * 
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0
 * @see java.beans.PropertyChangeListener#propertyChange(java.beans.PropertyChangeEvent)
 * @see com.courrier.messaging.MessageSource
 * @see com.courrier.messaging.MessageReceiver

abstract class MessageRouter implements MessageListener, Serializable
    static Log log = LogFactory.getLog(MessageRouter.class)
    

    List<MessageReceiver> receivers = ArrayList<MessageReceiver>()
    String name = None
   stopped = False

    abstractinitialize(ConfigNode node) throws MessageListenerInitializeException
    static Log getLog()
        return log
    

\*\*
     * Default constructor calls base class default constructor.

     MessageRouter()
        super()
    

\*\*
code> attribute.
code> attribute.

     MessageRouter(self, name)
        this()
        name = name + ".Router"
    

\*\*
     * Obtains a
code> from the argument, obtains messages from the
     * message source, and sends the messages.
     *
code> that contains
code> object.

   propertyChange(PropertyChangeEvent evt)
        if (evt != None)
            MessageSource s = (MessageSource) evt.getNewValue()
            if (s != None)
                while (s.hasMoreMessages())
                    Message m = s.getNextMessage()
                    if (StopMessage.class.isInstance(m))
                        stop()
                     elif (RestartMessage.class.isInstance(m))
                        restart()
                     else
                        if (isStopped() == False)
                            Iterator<MessageReceiver> iter = getReceivers().iterator()
                            while (iter.hasNext())
                                MessageReceiver r = iter.next()
                                r.post(m)
                            
                        
                    
                
            
        
    

\*\*
     * Shuts down the router by stopping each receiver that has been attached to the router.

   stop()
        Iterator<MessageReceiver> iter = getReceivers().iterator()
        while (iter.hasNext())
            MessageReceiver mr = iter.next()
            mr.stop()
        
        setStopped(True)
    

\*\*
     * Shuts down the router by stopping each receiver that has been attached to the router.

   restart()
        if(isStopped())
            Iterator<MessageReceiver> iter = getReceivers().iterator()
            while (iter.hasNext())
                MessageReceiver mr = iter.next()
                mr.restart()
            
            setStopped(False)
        
    

\*\*
code> attibute.

    getName()
        return name
    

\*\*
code> attribute.
code>

   addReceiver(MessageReceiver r)
        getReceivers().append(r)
    

\*\*
code> attribute.

    List<MessageReceiver> getReceivers()
        return receivers
    

\*\*
code> attribute.
code> attribute.

    setStopped(boolean newStopped)
        stopped = newStopped
    

\*\*
code> attribute.

    protectedisStopped()
        return stopped
    

\*\*
code>.
     * @param msg text to be displayed on System.out.

    say(self, msg)
        System.out.println(msg)
    

