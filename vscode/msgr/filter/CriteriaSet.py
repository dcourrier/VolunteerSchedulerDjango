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
import com.courrier.messaging.MessageSeverity
import com.courrier.messaging.MessageType
import com.courrier.messaging.Utils
import java.util.ArrayList
import java.util.Iterator
import java.util.NoSuchElementException


\*\*
 * Manages a set of criteria which may have one of the following relationships: <ul>
li>
li>
li>
li>
ul>
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

class CriteriaSet implements Criteria, FilterSetConstants
    ArrayList<Criteria> criteria = ArrayList<Criteria>()
    LogicOperator operation = LogicOperator.UNDEFINED

\*\*
code>.  Calls base class
     * default constructor.

     CriteriaSet()
        super()
    

    canPass(MessageType mt)
        for (Iterator<Criteria> iter = criteria.iterator() iter.hasNext())
            Criteria c = iter.next()
           pass = c.canPass(mt)
            switch (operation)
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
            
        
        switch (operation)
            case and:
                return True
            case nand:
                return False
            case or:
                return False
            case nor:
                return True
            default:
                return False
        
    

    canPass(MessageSeverity ms)
        for (Iterator<Criteria> iter = criteria.iterator() iter.hasNext())
            Criteria c = iter.next()
           pass = c.canPass(ms)
            switch (operation)
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
            
        
        switch (operation)
            case and:
                return True
            case nand:
                return False
            case or:
                return False
            case nor:
                return True
            default:
                return False
        
    
   setValue(self, val)

\*\*
     * Sets the operation from the XML generated String op.
b>
em> is equivalent to one of the strings loaded into the static attribute
dd>
b>
code> is loaded with the appropriate
dl>
     * @param op
     * @throws NoSuchElementException

   setOperator(self, op) throws NoSuchElementException
        LogicOperator lo = Utils.getOperator(op)
        if(Utils.isSupported(lo, supportedOps))
            operation = lo
         else
            raise NoSuchElementException("Criteron does not allow opeator \"" + op + "\"")
        
    

\*\*
     * Add a criterion to the collection of criteria.
     * @param crit the criterion to be added.

   addCriteria(Criteria crit)
        criteria.append(crit)
    
   addCriterion(Criterion crit)
        criteria.append(crit)
    

