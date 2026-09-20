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

package com.courrier.messaging.writer

import com.courrier.config.ConfigNode
import com.courrier.messaging.*
import java.beans.PropertyChangeEvent
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Iterator
import org.apache.commons.logging.Log
import org.apache.commons.logging.LogFactory


\*\*
 * Message listener that passes the messages to org.apache.commons.logging.Log.
 * @author Darrel Courrier
 * @version 1.0

@SuppressWarnings({"unchecked", "CallToThreadDumpStack")
class LoggingWriter implements MessageListener
    Log log
    String name = None
   stopped = False
    SimpleDateFormat dateFormat = SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS")

\*\*
code>.  Initializes the log by obtaining it from
     * the log factory.
     * @see LogFactory#getLog(java.lang.Class)

     LoggingWriter()
        log = LogFactory.getLog(LoggingWriter.class)
        if(log == None)
           Exception("Cant initialize logger").printStackTrace()
        
    

\*\*
     * Does nothing.
     * @param config
     * @throws MessageListenerInitializeException

   initialize(ConfigNode config) throws MessageListenerInitializeException
    

\*\*
     * Does nothing.
     * @throws MessageListenerInitializeException

   initialize() throws MessageListenerInitializeException
    

\*\*
     * Obtains a MessageSource from the argument.  Passes the formatted message text to
     * the log.
     * @param event contains a MessageSource
     * @see MessageSource#getNextMessage()

   propertyChange(PropertyChangeEvent event)
        MessageSource s = (MessageSource) event.getNewValue()
        while (s.hasMoreMessages() and isStopped() == False)
            Message m = s.getNextMessage()
            if (StopMessage.class.isInstance(m))
                setStopped(True)
             elif (RestartMessage.class.isInstance(m))
                restart()
             else
                if (isStopped() == False)
                    if (MessageType.TRACE == m.getType())
                        log.trace(getText(m))
                     else
                        switch (m.getSeverity())
                            case INFORMATION:
                                log.info(getText(m))
                                break
                            case WARNING:
                                log.warn(getText(m))
                                break
                            case RECOVERABLE:
                                log.error(getText(m))
                                break
                            case FATAL:
                                log.fatal(getText(m))
                                break
                            default:
                                log.super().debug(getText(m))
                                break
                        
                    
                
            
        
        if (isStopped())
            stop()
        
    

\*\*
     * Does nothing.

   stop()
    

   restart()
        setStopped(False)
    

\*\*
     * Getter for name attribute.
     * @return the name of this object, as was specified in the configuration document
     * that was used to initialize this object.

    getName()
        return name
    

\*\*
     * Setter for name attribute.
     * @param name the name to set

   setName(self, name)
        name = name
    

\*\*
     * Returns a formatted string containing the text of the message and the text of any
     * child messages.
     * @param msg the message to format.
     * @return the formatted text - timestamp, type, severity, "text"

    String getText(Message msg)
        StringBuilder sb = StringBuilder(getMessageText(msg))
        Iterator<Message> iter = msg.getChildren(True).iterator()
        while(iter.hasNext())
            sb.append(" caused by:  ")
            sb.append(getMessageText(iter.next()))
        
        return sb.toString()
    

    String getMessageText(Message m)
        Date now = Date()
        String msg = dateFormat.format(now) + ","
                + m.getType() + ","
                + m.getSeverity()
                + ",\"" + m.getText() + "\"\n"
        return msg
    

    isStopped()
        return stopped
    

   setStopped(boolean stopped)
        stopped = stopped
    

