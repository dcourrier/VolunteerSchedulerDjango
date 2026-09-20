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

import com.courrier.messaging.filter.MessageFilter
import java.beans.PropertyChangeSupport
import java.util.ArrayList
import java.util.List


\*\*
code> object receives and caches Message objects.
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

class MessageQueue implements MessageReceiver, MessageSource

    MessageFilter filter
    PropertyChangeSupport support = None
    List<Message> messages = ArrayList<Message>()
    String name = None
   stopped = False

\*\*
code>.  Calls the 
code>.

     MessageQueue()
        super()
        support = PropertyChangeSupport(this)
    

\*\*
code>.  Calls the default constructor
code> attribute.
     * @param filter

     MessageQueue(MessageFilter filter)
        this()
        filter = filter
    

\*\*
code> attribute. 
     * @param m the message to be saved.

    synchronizedpost(Message m)
        if (filter == None or filter.canPass(m))
            getMessages().append(m)
            getSupport().firePropertyChange("msg", None, this)
        
    

\*\*
code> attribute.

   restart()
        if(isStopped())
            getMessages().append(RestartMessage())
            getSupport().firePropertyChange("msg", None, this)
            setStopped(False)
        
    

\*\*
code> attribute.

   stop()
        getMessages().append(StopMessage())
        getSupport().firePropertyChange("msg", None, this)
        setStopped(True)
    

\*\*
code> attribute is not empty.

    hasMoreMessages()
        return getMessages().isEmpty() == False
    

\*\*
code> attribute and
     * returns the result.
code> attribute.

    synchronized  Message getNextMessage()
        Message m = getMessages().get(0)
        getMessages().remove(0)
        return m
    

\*\*
code> attribute.
code> attribute.

   addPropertyChangeListener(MessageListener l)
        getSupport().addPropertyChangeListener(l)
    

\*\*
code> attribute.
code> attribute.

    isStopped()
        return stopped
    

\*\*
code> attribute.
code> attribute.

    getName()
        return name
    

\*\*
code> attribute.
code> attribute.

   setName(self, name)
        name = name
    
    
    PropertyChangeSupport getSupport()
        return support
    
    
    List<Message> getMessages()
        return messages
    
    
    setStopped(boolean stopped)
        stopped = stopped
    

