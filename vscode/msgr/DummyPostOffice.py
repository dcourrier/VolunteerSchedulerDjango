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
code> that doesnt post any messages.  Intended to be
 * used in cases where message posting is handled outside the normal procedures.
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

class DummyPostOffice extends PostOffice

\*\*
code>.  Calls
     * base class constructor.

     DummyPostOffice()
        super()
    

\*\*
     * Does nothing.
     * @param msg the message to be delivered.


    synchronizedpost(Message msg)
 Do nothing
    

