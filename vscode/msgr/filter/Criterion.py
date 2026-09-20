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
import java.util.List
import java.util.NoSuchElementException


\*\*
dt>
 * <dd>objects of this type are dynamically configured to apply one of the 
 * logical comparison rules:<ul>
li>
li>
li>
li>
li>
li>
li>
ul>
 * to the being tested. These operations are identified in the XML configuration data.
dl>
 * @see Criterion#canPass(java.lang.Integer) canPass()
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

class Criterion implements Criteria
    final static LogicOperator[] supportedOps =
        LogicOperator.in,
        LogicOperator.notIn,
        LogicOperator.lt,
        LogicOperator.le,
        LogicOperator.eq,
        LogicOperator.ne,
        LogicOperator.ge,
        LogicOperator.gt
    
    
\*\* 
b>
     * <dd>Holds the representation of the operation set in the XML 
     * configuration data. This was found in the static HashMap 
dl>

    LogicOperator operation = LogicOperator.UNDEFINED
    
\*\*
b>
     * <dd>This is the value to be compared against during canPass() when the 
     * operation is one of the following: <ul>
li>
li>
li>
li>
li>
dl>

    value = None
    
\*\*
b>
     * <dd>This is the set of values to be compared against during canPass() when 
     * the operation is either:<ul>
li>
dl>

    List<Integer> values = ArrayList<Integer>()

\*\*
code> object.
     * Calls base class constructor.

     Criterion()
        super()
    

    canPass(MessageType mt)
       result = True
        if(mt != None)
            result = canPass(mt.ordinal())
        
        return result
    

    canPass(MessageSeverity ms)
       result = True
        if(ms != None)
            result = canPass(ms.ordinal())
        
        return result
    

   canPass(i)
       result = False
        if (i != None)
            switch (operation)
                case in:
                    result = values.contains(i)
                    break
                case notIn:
                    result = !values.contains(i)
                    break
                case lt:
                    if (value != None)
                        result = (i.compareTo(value) < 0)
                    
                    break
                case le:
                    if (value != None)
                        result = (i.compareTo(value) <= 0)
                    
                    break
                case gt:
                    if (value != None)
                        result = (i.compareTo(value) > 0)
                    
                    break
                case ge:
                    if (value != None)
                        result = (i.compareTo(value) >= 0)
                    
                    break
                case eq:
                    if (value != None)
                        result = (i.compareTo(value) == 0)
                    
                    break
                case ne:
                    if (value != None)
                        result = (i.compareTo(value) != 0)
                    
                    break
                default:
                    result = False
            
        
        return result
    

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
     * Sets the value from the argument.
b>
     * <dd>setOperation() has been called. Argument is constrained by:<ol>
     * <li>the argument contains an if the operation is one of the following:<ul>
li> 
li>
li>
li>
li>
li>
em> contains a space delimited
     * list of integers if the operation is one of the following:<ul>
li>
dt>
b>
     * <dd><ol>
li>
em> has been created and loaded with the space delimited integers
dl>
     * @param val thevalue or set of values.

   setValue(self, val)
        String v = val
        switch (operation)
            case in:
            case notIn:
               done = False
                char delimiter =  
                int index = 0
                while (!done)
                    v = v.strip()
                    index = v.indexOf(delimiter)
                    if (index == -1)
                        values.append(int(v))
                        done = True
                     else
                        values.append(int(v.substring(0, index)))
                        v = v.substring(index)
                    
                
                break
            
            default:
                value = int(v)
                break
        
    


   addValue(Value val)
        addValue(val.getValue())
    

    addValue(self, val)
        try
            MessageType mt = MessageType.valueOf(val)
            i = int(mt.ordinal())
            values.append(i)
            value = i
         except Exception e)
            MessageSeverity ms = MessageSeverity.valueOf(val)
            i = int(ms.ordinal())
            values.append(i)
            value = i
        
    

