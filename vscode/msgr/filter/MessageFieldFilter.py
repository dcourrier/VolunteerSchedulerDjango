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

import com.courrier.messaging.Message
import com.courrier.messaging.MessageSeverity
import com.courrier.messaging.MessageType
import java.lang.reflect.InvocationTargetException
import java.lang.reflect.Method
import org.apache.commons.lang3.StringUtils
import org.apache.commons.logging.Log
import org.apache.commons.logging.LogFactory


\*\*
dt> <dd>filters messages based upon the contents of
dl>
 *
 * @author Scott Fleming &amp Darrel Courrier
 * @version 1.0

class MessageFieldFilter implements MessageFilter

    final static Log log = LogFactory.getLog(MessageFieldFilter.class)
    Criteria criteria
    Method messageAttrGetter = None
    final static String[] VALID_FIELD_NAMES ="category", "severity"

\*\*
     * Creates an instance of
code>. Calls base class default constructor.

     MessageFieldFilter()
        super()
    

\*\*
     * Tests a pre identified field in the message against preset criteria.
dt>
     * <dd>{@link #setFieldName(self,) setFieldName has been called.
     *@link #addCriteria(Criteria) addCriteria has been called
dl>
     *
     * @return True if the message passes the criteria for the field identified
     * by the call to@link #setFieldName(self,) setFieldName and the
     * criteria identified by the call to
     *@link #addCriteria(Criteria) addCriteria.
     * @param message is the value to be tested.

    canPass(Message message)
       result = False
        if (message != None and messageAttrGetter != None)
            Object methodResult = None
            try
                Object[] objs = None
                methodResult = messageAttrGetter.invoke(message, objs)
                try
                    MessageSeverity ms = (MessageSeverity) methodResult
                    if(criteria == None)
                        result = True
                     else
                        result = criteria.canPass(ms)
                    
                 except ClassCastException cce1)
                    MessageType mt = (MessageType) methodResult
                    if(criteria == None)
                        result = True
                     else
                        result = criteria.canPass(mt)
                    
                
             except IllegalArgumentException e)
                String messClass = message.getClass().getName()
            Method[] m = message.getClass().getDeclaredMethods()
                say(messageAttrGetter.toString() + " is not in " + messClass + ".")
                log.error(, e)
             except InvocationTargetException e)
                say("Could not access Target object of type Message.")
                log.error(, e)
             except IllegalAccessException e)
                say("could not access method Message." + messageAttrGetter.getName() + "().")
                log.error(, e)
             except ClassCastException cce)
                say("could not access method Message."
                        + messageAttrGetter.getName()
                        + "() with return type"
                        + methodResult.getClass().getName())
                log.error(, cce)
            
        
        return result
    

\*\*
     * Identifies which field will be evaluated in
dt>
dd> <dt><b>Post
b> <dd>The
dl>
     *
code>
     * attribute.
code> is not a readable property of
code>.
     * @see Message

   setFieldName(self, fieldName) throws Exception
        try
            
            Class[] cls = None
            messageAttrGetter = Message.class.getMethod(
                    "get" + fieldName.substring(0, 1).toUpperCase() + fieldName.substring(1),
                    cls)
         except NoSuchMethodException e)
            raise Exception("could not find method Message.get" + fieldName.substring(0, 1).toUpperCase() + fieldName.substring(1) + "()")
        
    

\*\*
     * Identifies which Criteria will be used in
     *@link #canPass(Message) canPass to evaluate the message property set in
     *@link #setFieldName(self,) setFieldName. <dl><dt><b>Post
dd>
dl>
     *
     * @param crit the criteria that will be used.

   addCriteria(Criteria crit)
        criteria = crit
    

   addCriterion(Criterion crit)
        criteria = crit
    

\*\*
     * Identifies which Criteria will be used in
     *@link #canPass(Message) canPass to evaluate the message property set in
     *@link #setFieldName(self,) setFieldName. <dl><dt><b>Post
dd>
dl>
     *
     * @param crit the criteria that will be used.

   addCriteriaSet(CriteriaSet crit)
        addCriteria(crit)
    

\*\*
     * Displays the argument on System.out.

    say(self, msg)
        System.out.println(msg)
    

