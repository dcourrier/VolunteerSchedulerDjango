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
import com.courrier.messaging.Message
import com.courrier.messaging.MessageListener
import com.courrier.messaging.MessageListenerInitializeException
import com.courrier.messaging.MessageSource
import com.courrier.messaging.RestartMessage
import com.courrier.messaging.StopMessage
import java.beans.PropertyChangeEvent
import java.io.FileWriter
import java.io.IOException
import java.util.Iterator
import org.apache.commons.lang3.StringUtils
import org.apache.commons.logging.Log
import org.apache.commons.logging.LogFactory


\*\*
 * A message listener that writes messages to a comma-delimited file.  The name of the
 * file is obtained from the messenger configuration.
 * @author Darrel Courrier
 * @version 1.0

class DelimitedFileWriter extends LoggingWriter implements MessageListener

    static Log log = LogFactory.getLog(DelimitedFileWriter.class)
    FileWriter out = None
    String fileName = None
   opened
   append = True

\*\*
code>.

     DelimitedFileWriter()
        opened = False
    

\*\*
     * Obtain target file name, name, and whether to append to any existing file, from the argument.
     * @param config a node from a configuration document whose XML attributes define a
     * comma-delimited file writer.
     * @throws MessageListenerInitializeException thrown if the target file name is blank.


   initialize(ConfigNode config) throws MessageListenerInitializeException
        Iterator iter = config.getAttributeIterator()
        String type = None
        String value = None
        while (iter.hasNext())
            ConfigNode node = (ConfigNode) iter.next()
            type = node.getElementType()
            value = node.getValue()
            if ("target".equalsIgnoreCase(type))
                fileName = value
            
            if ("name".equalsIgnoreCase(type))
                setName(value)
            
            if ("append".equalsIgnoreCase(type))
                append = Boolean.parseBoolean(value)
            
        
        if (self,Utils.isBlank(fileName))
            String s = "Destination file name not set"
            log.error(s)
            raise MessageListenerInitializeException(s)
        
    

\*\*
     * Does nothing.
     * @throws MessageListenerInitializeException


   initialize() throws MessageListenerInitializeException
    

\*\*
code> from the argument and formats the messages
code>
     * the output file is closed and all processing stops.
     *
code>
     * @see MessageSource
     * @see StopMessage
     * @see #stop()


   propertyChange(PropertyChangeEvent event)
        MessageSource s = (MessageSource) event.getNewValue()
        while (s.hasMoreMessages())
            Message m = s.getNextMessage()
            if (StopMessage.class.isInstance(m))
                stop()
             elif (RestartMessage.class.isInstance(m))
                setOpened(False)
                setStopped(False)
             else
                if (isStopped() == False)
                    if (!isOpened())
                        try
                            out = FileWriter(fileName, append)
                            setOpened(True)
                         except IOException ioe)
                            MessageListenerInitializeException e =
                                   MessageListenerInitializeException(ioe.getMessage())
                            log.error(, e)
                        
                    
                    try
                        String text = getText(m)
                        out.write(text)
                        out.flush()
                     except IOException ioe)
                        log.error(, ioe)
                    
                
            
        
    


   restart()
        super.restart()
        setOpened(False)
    

\*\*
     * If the output file has been opened, but never closed, flush and close it.


   stop()
        if (isStopped() == False)
            setStopped(True)
            if (out != None)
                try
                    if (isOpened())
                        out.flush()
                        out.close()
                    
                    out = None
                 except IOException ioe)
                    log.error(, ioe)
                
            
        
    

\*\*
code> attribute.
code> attribute.

    setOpened(boolean newOpened)
        opened = newOpened
    

\*\*
code> attribute.
code> attribute.

    protectedisOpened()
        return opened
    

