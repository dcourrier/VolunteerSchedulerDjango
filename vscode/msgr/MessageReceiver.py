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
 * Defines the behavior of objects that can receive messages.
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

 interface MessageReceiver

\*\*
code> method has been executed.

    isStopped()

\*\*
code>

    getName()

\*\*
code>.
code>.

   setName(self, name)

\*\*
code>.
code> that is to be sent.

   post(Message m)

\*\*
     * Stop processing messages.

   stop()

\*\*
     * Restart processing messages after being stopped.

   restart()
 
