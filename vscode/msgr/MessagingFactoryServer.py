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
import com.courrier.config.ConfigNodeImpl
import com.courrier.config.XMLConfiguration
import com.courrier.messaging.filter.MessageFilter
import com.courrier.messaging.filter.MessageFilterSet
import java.io.InputStream
import java.util.Collection
import java.util.Iterator
import org.apache.commons.lang3.StringUtils
import org.apache.commons.logging.Log
import org.apache.commons.logging.LogFactory


\*\*
code> objects populated with a post office as a receiver.  Configures the post office,
 * adding queues, routers, listeners and filters, based on the information stored in a configuration file.<br><br>
 *
 * A configuration file is an XML document which is defined by the XML Document Type Definition 
code>.  See the overview for more details.
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

class MessagingFactoryServer extends MessagingFactory
    static Log log = LogFactory.getLog(MessagingFactoryServer.class)

\*\*
     * Default constructor.  Calls base class and stores a pointer to this object in the
     * base class singleton attribute.  Declared because it allows an un-initialized
     * instance to be created.

    MessagingFactoryServer()
        super()
    

\*\*
code>.
     * @param configFileName the path and name of the configuration file.
     * @throws MessagingFactoryCreationException thrown if the configuration file could not be found
     * or was invalid.

     MessagingFactoryServer(self, configFileName) throws MessagingFactoryCreationException
        this()
        setFileName(configFileName)
        processConfig(configFileName)
    

\*\*
code>.
code> that contains an XML configuration file.
     * @throws MessagingFactoryCreationException thrown if the configuration file was invalid.

     MessagingFactoryServer(InputStream is) throws MessagingFactoryCreationException
        this()
        processConfig(is)
    


    Messenger getMessenger()
        returnMessengerImpl(getPostOffice())
    

    createPostOffice(ConfigNode node) throws MessagingFactoryCreationException
        String name = "Default PO Name"
        Iterator ai = node.getAttributeIterator()
        ConfigNodeImpl obj = None
        String type = None
        String value = None
        MessageFilter queueFilter = None
       multithreaded = False
       restartable = False
        while (ai.hasNext())
            obj = (ConfigNodeImpl) ai.next()
            type = obj.getElementType()
            value = obj.getValue()
            if (type.equalsIgnoreCase("ID"))
                name = value
             elif ("inputFilter".equalsIgnoreCase(type))
                queueFilter = getFilters().get(value)
                if (queueFilter == None)
                    raise MessagingFactoryCreationException("Factory unable to find a filter with ID=\"" + value + "\".")
                
             elif ("multithreaded".equalsIgnoreCase(type))
                multithreaded = value.equalsIgnoreCase("True")
             elif ("restartable".equalsIgnoreCase(type))
                restartable = value.equalsIgnoreCase("True")
            
        

        setPostOffice(PostOffice(name, createMessageQueue(queueFilter), createRouter(multithreaded)))
        createPostOfficeListeners(node)
    

    createPostOfficeListeners(ConfigNode node) throws MessagingFactoryCreationException
        Iterator iter = node.getElementIterator()
        ConfigNode obj = None
        String type = None
        String value = None
        String className = None
        MessageFilter filter = None
        String destinationName = None
        while (iter.hasNext())
 since <PostOffice> only contains <Destination> elements we can use an element iterator without
 testing the element type.
            ConfigNode dest = (ConfigNode) iter.next()
            Iterator ai = dest.getAttributeIterator()
            while (ai.hasNext())
                obj = (ConfigNode) ai.next()
                type = obj.getElementType()
                value = obj.getValue()
                if ("name".equalsIgnoreCase(type))
                    destinationName = value
                 elif ("filterId".equalsIgnoreCase(type))
                    filter = (MessageFilter) getFilters().get(value)
                    if (filter == None)
                        raise MessagingFactoryCreationException("Factory unable to find a filter with ID=\"" + value + "\".")
                    
                 elif ("className".equalsIgnoreCase(type))
                    className = value
                
            
            createAListener(destinationName, className, filter, dest)
        
    

    createAListener(self, name, String className, MessageFilter filter, ConfigNode config) throws MessagingFactoryCreationException
        MessageListener listener = None
        try
            Object object = Class.forName(className).newInstance()
            listener = (MessageListener) object
            listener.initialize(config)
         except Exception e)
            raise MessagingFactoryCreationException(e)
        

        MessageQueue q = createMessageQueue(filter)
        q.addPropertyChangeListener(listener)
        ((PostOffice) getPostOffice()).addListenerQueue(q)
    

    MessageRouter createRouter(boolean multithreaded) throws MessagingFactoryCreationException
        MessageRouter rtr = None
        try
            if (multithreaded)
                rtr = ThreadedMessageRouter()
                rtr.initialize()
             else
                rtr = StandardMessageRouter()
            
         except Exception e)
            raise MessagingFactoryCreationException(e)
        
        return rtr
    

    MessageQueue createMessageQueue(MessageFilter filter)
        returnMessageQueue(filter)
    

    createFilters(ConfigNode node) throws MessagingFactoryCreationException
        try
            MessageFilterFactory factory = MessageFilterFactory()
            Collection<MessageFilterSet> coll = factory.createFilterSet(node)
            if (coll.isEmpty() == False)
                Iterator<MessageFilterSet> iter = coll.iterator()
                while (iter.hasNext())
                    MessageFilterSet mfs = iter.next()
                    getFilters().put(mfs.getId(), mfs)
                
            
         except Exception e)
            raise MessagingFactoryCreationException(e)
        
    

    processConfig(ConfigNode configFile) throws Exception
        ConfigNode node = None
        String elementType = None
        ConfigNode root = configFile.getChildElement(0)
        Iterator iter = root.getElementIterator()
        while (iter.hasNext())
            node = (ConfigNode) iter.next()
            elementType = node.getElementType()
            if (elementType.equalsIgnoreCase("PostOffice"))
                createPostOffice(node)
             elif (elementType.equalsIgnoreCase("MessageFilterSet"))
                createFilters(node)
            
        
    

    processConfig(InputStream is) throws MessagingFactoryCreationException
        try
            ConfigNode configFile = XMLConfiguration(is)
            processConfig(configFile)
         except Throwable t)
            log.error(, t)
            raise MessagingFactoryCreationException(t)
        
    

    processConfig(self, fileName) throws MessagingFactoryCreationException
        try
            ConfigNode configFile = XMLConfiguration(fileName)
            processConfig(configFile)
         except Throwable t)
            log.error(, t)
            raise MessagingFactoryCreationException(t)
        
    

