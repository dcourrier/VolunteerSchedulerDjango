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

\*\*
 * A message receiver that is capable of receiving, caching, and distributing messages.
code> when the
code> and
code>.  The message queue object handles message caching.  The
 * message router object handles message distribution.
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

class PostOffice implements MessageReceiver

    MessageQueue inputQueue = None
    MessageRouter router = None
    String name
   stopped = False

\*\*
code>.
     * Calls base class default constructor.

     PostOffice()
        super()
    

\*\*
code>.
     * Calls no-arg constructor.
code> attribute.
code> attribute.
code> attribute.

     PostOffice(self, name, MessageQueue q, MessageRouter router)
        this()
        inputQueue = q
        name = name
        router = router
        q.addPropertyChangeListener(router)
    

\*\*
     * Adds the argument to the router.
     * @param q the message queue that is to be added to the router.

   addListenerQueue(MessageQueue q)
        getRouter().addReceiver(q)
    

\*\*
code> attribute.
code> attribute.

   setName(self, newName)
        name = newName
    

\*\*
code> attribute.
code> attribute.

    getName()
        return name
    

\*\*
     * Stops processing by informing the input queue to stop processing.

   stop()
 This adds a StopMessage to the queue, so it is not necessary to stop the router.
 Doing so here will cause messages to be lost.
        getInputQueue().stop()
        stopped = True
    

   restart()
        if(stopped)
            stopped = False
            getInputQueue().restart()
        
    

\*\*
code> attribute.
code> attribute.

    MessageRouter getRouter()
        return router
    

\*\*
     * Distribute the argument.  Does so by posting it in the input queue.
     * @param msg

   post(Message msg)
        if(isStopped() == False)
            getInputQueue().post(msg)
        
    

\*\*
code> attribute.
code> attribute.

    MessageQueue getInputQueue()
        return inputQueue
    

\*\*
     * Tells whether the post office been told to stop processing.
code> attribute.

    isStopped()
        return stopped
    

