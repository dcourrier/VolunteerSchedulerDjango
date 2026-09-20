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
import com.courrier.messaging.MessageListener
import com.courrier.messaging.MessageQueue
import com.courrier.messaging.MessageReceiver
import com.courrier.messaging.MessageRouter
import com.courrier.messaging.MessagingFactory
import com.courrier.messaging.MessagingFactoryCreationException
import com.courrier.messaging.Messenger
import com.courrier.messaging.MessengerImpl
import com.courrier.messaging.PostOffice
import com.courrier.messaging.StandardMessageRouter
import com.courrier.messaging.filter.MessageFilter
import com.courrier.messaging.filter.MessageFilterSet


\*\*
 * Creates a client messenger and also serves as a message receiver that can send
 * messages.
 * @author Darrel Courrier
 * @version 1.0

@SuppressWarnings({"unchecked", "CallToThreadDumpStack")
class ClientMessagingFactory extends MessagingFactory implements MessageReceiver

    MessageListener listener = None

\*\*
code>.  Calls the base
     * class constructor and initializes the post office.
code>.
     * @param file
     * @param url

     ClientMessagingFactory(self, type, String file, String url)
        super()
        try
            init(type, file, url)
         except MessagingFactoryCreationException e)
            setPostOffice(ClientPostOffice())
            handleError(e)
        
    

\*\*
code>.
code>.


     Messenger getMessenger()
        returnMessengerImpl(getPostOffice())
    

\*\*
     * Sends a messaage.
     * @param m the message to send.


   post(Message m)
        getPostOffice().post(m)
    

\*\*
     * Returns the name of this factory.
     * @return the class name of this object.


    getName()
        return getClass().getName()
    

\*\*
     * Makes the factory ready to dispatch messages.

   start()
        try
            getListener().initialize()
         except Throwable e)
            handleError(e)
        
    

    init(self, type, String file, String url) throws MessagingFactoryCreationException
        try
            checkType(type)
            MessageFilterSet filter = ClientDefaultFilter()
            MessageQueue q = MessageQueue(filter)
            MessageRouter rtr = StandardMessageRouter("ClientStandardRouter")
            rtr.initialize()
            setPostOffice(PostOffice("ClientPO", q, rtr))
            createListener(filter, type, file, url)
         except MessagingFactoryCreationException mfce)
            throw mfce
         except Throwable e)
            raise MessagingFactoryCreationException(e)
        
    

    checkType(self, type)  throws MessagingFactoryCreationException
        String[] supported =
            "url"
        
       ok = False
        for(int loop = 0 loop < supported.length and ok == False loop++)
            if((supported[loop].equalsIgnoreCase(type)))
                ok = True
            
        
        if(ok == False)
            raise MessagingFactoryCreationException("Client messaging type \"" + type + "\" is not supported")
        
    

\*\*
code>.  Adds
     * the listener to the post office listener queue
     * @param filter a message filter that determines which messages can be sent to the listener.
     * @throws MessagingFactoryCreationException if an error occurred

    createListener(MessageFilter filter, String type, String file, String url) throws MessagingFactoryCreationException
        try
            listener = ClientMessageWriter(type, file, url)
            listener.initialize()
            MessageQueue q = MessageQueue(filter)
            q.addPropertyChangeListener(listener)
            ((PostOffice) getPostOffice()).addListenerQueue(q)
         except Exception e)
            raise MessagingFactoryCreationException(e)
        
    

\*\*
code> attribute.
code> attribute.

    MessageListener getListener()
        return listener
    

    handleError(Throwable e)
        e.printStackTrace()
    

