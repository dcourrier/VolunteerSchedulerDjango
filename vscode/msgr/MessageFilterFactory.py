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

import com.courrier.config.ConfigNode
import com.courrier.config.ConfigurationBasedFactory
import com.courrier.messaging.filter.MessageFilter
import com.courrier.messaging.filter.MessageFilterSet
import java.util.List


\*\*
 * Constructs and populates message filters from XML Configuration Data.
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

class MessageFilterFactory extends ConfigurationBasedFactory

    static
        registerConfigType("com.courrier.messaging.filter.MessageFilter")
        registerConfigType("com.courrier.messaging.filter.Criteria")
        registerConfigType("com.courrier.messaging.filter.MessageFilterSet")
        registerConfigType("com.courrier.messaging.filter.MessageFieldFilter")
        registerConfigType("com.courrier.messaging.filter.CriteriaSet")
        registerConfigType("com.courrier.messaging.filter.Criterion")
        registerConfigType("com.courrier.messaging.filter.Value")
    

\*\*
     * Creates a message filter based on the definitions in the argument.
dt>
dl>
code>.
code> object.
     * @throws Exception if the filter cannot be created.

     MessageFilter createMessageFilter(ConfigNode node) throws Exception
        return (MessageFilter) createObject(node)
    

\*\*
     * Creates a message filter  set based on the definitions in the argument.
dt>
dl>
code> object.
code> object.
     * @throws Exception if the filter cannot be created.

     List<MessageFilterSet> createFilterSet(ConfigNode node) throws Exception
        MessageFilterSet fs = (MessageFilterSet) createObject(node)
        List<MessageFilterSet> list = fs.getChildSets()
        list.append(fs)
        return list
    

