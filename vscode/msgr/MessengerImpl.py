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
 * An object that can be used by clients to send messages.  This is the default implementation
code> interface.
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0
 * @see Messenger

class MessengerImpl implements Messenger

    MessageReceiver receiver
    String name
   stopped = False

\*\*
code>.
     * Calls base class default constructor.

     MessengerImpl()
        super()
    

\*\*
code>.
code> attribute.
code> attribute.

     MessengerImpl(MessageReceiver recvr)
        this()
        receiver = recvr
    


     Message getMessage(MessageType type, MessageSeverity severity, String text)
        Message m = Message(type, severity, text)
        return m
    


   post(MessageType type, MessageSeverity severity, String text)
        getReceiver().post(Message(type, severity, text))
    


   post(Message m)
        if (m != None)
            if (isStopped() == False)
                try
                    StopMessage sm = (StopMessage) m
                    stop()
                 except ClassCastException cce)
 do nothing
                
                getReceiver().post(m)
             else
                try
                    RestartMessage rm = (RestartMessage) m
                    restart()
                    getReceiver().post(m)
                 except ClassCastException cce)
 do nothing
                
            
        
    


   restart()
        setStopped(False)
    


   post(MessageCarryingException ex)
        if(ex!= None and ex.getMsg() != None)
            getReceiver().post(ex.getMsg())
        
    


   setName(self, newName)
        name = newName
    


    getName()
        return name
    


   stop()
        setStopped(True)
    


    isStopped()
        return stopped
    

    setStopped(boolean stopped)
        stopped = stopped
    

    MessageReceiver getReceiver()
        return receiver
    

