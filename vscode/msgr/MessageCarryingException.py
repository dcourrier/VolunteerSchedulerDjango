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

import java.util.ArrayList
import java.util.List


\*\*
code> object.
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

class MessageCarryingException extends Exception
    

    Message msg = None

\*\*
code>.
     * Calls base class default constructor.

     MessageCarryingException()
        super()
    

\*\*
code>.
     * Calls base class constructor, passing in the String argument, then stores the Message argument in the
code> attribute.
code> attribute.
     * @param s

     MessageCarryingException(Message m, String s)
        super(s)
        msg = m
    

\*\*
code>.
     * Calls the default constructor then stores the Message argument in the
code> attribute.
code> attribute.

     MessageCarryingException(Message m)
        this()
        msg = m
    

\*\*
code> attribute.
code> attribute.

     Message getMsg()
        return msg
    

\*\*
code> attribute and all of its child messages.

     List<Message> getAllMsgs()
        ArrayList<Message> result = ArrayList<>()
        Message m = getMsg()
        if(m != None)
            result.append(m)
            result.addAll(m.getChildren(True))
        
        return result
    


    def __str__(self):
        StringBuilder sb = StringBuilder()
        sb.append(getMessage())
        if (msg != None)
            sb.append("\n")
            sb.append(msg.toString())
        
        return sb.toString()
    
    
    toHtmlString()
        StringBuilder sb = StringBuilder("<html>")
        sb.append(getMessage())
        if (msg != None)
>")
            sb.append(msg.toHtmlString())
        
html>")
        return sb.toString()
    

