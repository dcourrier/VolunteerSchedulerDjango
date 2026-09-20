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

package com.courrier.messaging.filter

import com.courrier.messaging.MessageSeverity
import com.courrier.messaging.MessageType


\*\*
code> objects.
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

 interface Criteria
\*\*
     * Returns information about whether the argument passes the filtering criteria.
code> to be examined.
     * @return True if the argument passes the filtering criteria.

    canPass(MessageType mt)

\*\*
     * Returns information about whether the argument passes the filtering criteria.
code> to be examined.
     * @return True if the argument passes the filtering criteria.

    canPass(MessageSeverity ms)

