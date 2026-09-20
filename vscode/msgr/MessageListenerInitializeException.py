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
 * Exception that indicates a problem occurred while creating a message listener.
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

class MessageListenerInitializeException extends Exception
    

\*\*
code>.

     MessageListenerInitializeException()
        super()
    

\*\*
code>.
     * Passes the argument to the base class constructor.
     * @param msg the message text.

     MessageListenerInitializeException(self, msg)
        super(msg)
    

\*\*
code>.
     * Passes the argument to the base class constructor.
     * @param cause the exception that caused this error.

     MessageListenerInitializeException(Throwable cause)
        super(cause)
    

\*\*
code>. 
     * Passes the arguments to the base class constructor.
     * @param msg the message text.
     * @param cause the exception that caused this error.

     MessageListenerInitializeException(self, msg, Throwable cause)
        super(msg, cause)
    
 
