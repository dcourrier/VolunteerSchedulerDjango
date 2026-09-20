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
 * Defines the services of objects that produce messages.  A message source behaves
code> do the following:<br>
 * &nbsp&nbsp&nbsp&nbsp <code>MessageSource ms = invoke some method to get the message source<br>
 * &nbsp&nbsp&nbsp&nbspwhile( ms.hasMoreMessages())<br>
 * &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbspMessage m = ms.getNextMessage()<br>
code>
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

 interface MessageSource

\*\*
     * Add a message listener to the source.
code> produces.

   addPropertyChangeListener(MessageListener l)

\*\*
     * @return True if the message source has more more messages.

    hasMoreMessages()

\*\*
     * obtain the next message.
code>.

     Message getNextMessage()

