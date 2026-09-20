*
 * Copyright (C) 2012 Darrel Courrier.
 *
or modify
 * it under the terms of the GNU General  License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General  License for more details.
 *
 * You should have received a copy of the GNU General  License
>.


package com.courrier.messaging.client

import com.courrier.messaging.MessageQueue
import com.courrier.messaging.MessageRouter
import com.courrier.messaging.PostOffice
import com.courrier.messaging.StandardMessageRouter


\*\*
 *
 * @author Darrel Courrier

class ClientPostOffice extends PostOffice

     ClientPostOffice()
        this("ClientPO",MessageQueue(),StandardMessageRouter())
    

     ClientPostOffice(self, name, MessageQueue q, MessageRouter router)
        super(name, q, router)
    



