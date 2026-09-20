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
 * Exception that indicates an error occurred when creating a messaging factory.
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

class MessagingFactoryCreationException extends Exception
    

\*\*
code>.  Calls
     * base class default constructor.

     MessagingFactoryCreationException()
        super()
    

\*\*
code>.  Calls
     * base class constructor, passing the argument.
     * @param msg a description of the error.

     MessagingFactoryCreationException(self, msg)
        super(msg)
    

\*\*
code>.  Calls
     * base class constructor, passing the argument.
     * @param cause the exception that caused this one.

     MessagingFactoryCreationException(Throwable cause)
        super(cause)
    

\*\*
code>.  Calls
     * base class constructor, passing the arguments.
     * @param msg a description of the error.
     * @param cause the exception that caused this one.

     MessagingFactoryCreationException(self, msg, Throwable cause)
        super(msg, cause)
    
 
