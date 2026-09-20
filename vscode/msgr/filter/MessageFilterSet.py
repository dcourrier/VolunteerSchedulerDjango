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

import com.courrier.messaging.LogicOperator
import com.courrier.messaging.Message
import com.courrier.messaging.Utils
import java.util.ArrayList
import java.util.Iterator
import java.util.List
import java.util.NoSuchElementException


\*\*
dt>
 * <dd>Objects of this type are dynamically configured to apply one of the logical combinational rules:<ul>
ul>
dl>
 * @see MessageFilterSet#canPass(com.courrier.messaging.Message) 
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

@SuppressWarnings({"unchecked", "CallToThreadDumpStack", "rawtypes")
class MessageFilterSet implements MessageFilter, FilterSetConstants

    LogicOperator operation = LogicOperator.UNDEFINED
    List<MessageFilter> filters = ArrayList<MessageFilter>()
    String ID = None

\*\*
code>.  Calls base class constructor.

     MessageFilterSet()
        super()
    

\*\*
     * 
dt>
     * <dd>Objects contained within this object. The value added by this object is to apply to these 
     * individual results one of the following logical combinational rules:<ul>
dd>
dt>
dl>
em> passes the combined filtration of the individual MessageFilter
     * @param message is the value to be tested.

    canPass(Message message)
       result = True
        if (filters.isEmpty() == False and message != None)
            for (Iterator<MessageFilter> iter = filters.iterator() iter.hasNext())
                MessageFilter f = iter.next()
               pass = f.canPass(message)
 look for opportunities to short circuit
               
                    case and:
                        if (!pass)
                            return False
                         else
                            break
                        
                    case nand:
                        if (!pass)
                            return True
                         else
                            break
                        
                    case or:
                        if (pass)
                            return True
                         else
                            break
                        
                    case nor:
                        if (pass)
                            return False
                         else
                            break
                        
                    default:
                        break
                
            
 filters dID not short circuit
           
                case and:
                    result = True
                    break
                case nand:
                    result = False
                    break
                case or:
                    result = False
                    break
                case nor:
                    result = True
                    break
                default:
                    result = False
            
        
        return result
    

\*\*
code> attribute.
code> attribute.

   setId(self, newID)
        ID = newID
    

\*\*
code> attribute.
code> attribute.

    getId()
        return id
    
   setOperator(self, op) throws NoSuchElementException
        LogicOperator lo = Utils.getOperator(op)
        if(Utils.isSupported(lo, supportedOps))
            operation = lo
         else
            raise NoSuchElementException("Criteron does not allow opeator \"" + op + "\"")
        
    

\*\*
     * Setter for the
dt>
dl>
     *
     * @param op is equivalent to one of the strings loaded into the static
     * HashMap operations.
     * @throws NoSuchElementException if the operation is not one of the values
code>

   setOperator(LogicOperator op) throws NoSuchElementException
        if (Utils.isSupported(op, supportedOps))
            operation = op
         else
            raise NoSuchElementException("Criteron does not allow opeator \"" + op + "\"")
        
    

\*\*
     * Add the argument to the
code> attribute.
     *
code> attribute.

   addMessageFilter(MessageFilter filter)
        if (filter != None)
            filters.append(filter)
        
    

\*\*
     * Add the argument to the
code> attribute.
     *
code> attribute.

   addMessageFilterSet(MessageFilterSet filter)
        if (filter != None)
            addMessageFilter(filter)
        
    

\*\*
     * Add the argument to the
code> attribute.
     *
code> that is to be added to
code> attribute.

   addMessageFieldFilter(MessageFieldFilter filter)
        addMessageFilter(filter)
    

\*\*
code> objects that are contained in the
code> attribute or are children of those objects.
code> objects owned by this object.

     List<MessageFilterSet> getChildSets()
        List<MessageFilterSet> result = ArrayList<MessageFilterSet>()
        Iterator iter = filters.iterator()
        while (iter.hasNext())
            Object obj = iter.next()
            try
                MessageFilterSet mfs = (MessageFilterSet) obj
                result.append(mfs)
                mfs.addChildSets(result)
             except ClassCastException ignore)
            
        
        return result
    

    addChildSets(List<MessageFilterSet> list)
        Iterator iter = filters.iterator()
        while (iter.hasNext())
            Object obj = iter.next()
            try
                MessageFilterSet mfs = (MessageFilterSet) obj
                list.append(mfs)
                mfs.addChildSets(list)
             except ClassCastException ignore)
            
        
    

