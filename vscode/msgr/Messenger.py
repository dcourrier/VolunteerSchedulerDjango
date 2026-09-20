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
 *  Common behavior of objects that can be used by clients to send messages.  To use:<ol>
li>
code>
li>
code> method, which is inherited
ol>
 *
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0
 * @see MessagingFactory
 * @see Message
 * @see MessageReceiver

 interface Messenger extends MessageReceiver

\*\*
     * Send an exception.
     * @param e the exception that is to be sent.

   post(MessageCarryingException e)

\*\*
     * Create a Message using the arguments and send it.
code> enum.
code> enum.
     * @param text the message text.

   post(MessageType type, MessageSeverity severity, String text)

\*\*
     * Obtain a Message, using the arguments to populate the Message objects attributes.
code> enum.
code> enum.
     * @param text the message text.
code> object with its attributes populated from the arguments.

     Message getMessage(MessageType type, MessageSeverity severity, String text)
 
