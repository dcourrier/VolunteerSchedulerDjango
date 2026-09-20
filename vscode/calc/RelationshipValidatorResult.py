* 
 * Copyright 2026 Darrel Courrier.
 *
 * Licensed under the Apache License, Version 2.0 (the "License")
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.

package com.courrier.volunteer.calc

import com.courrier.volunteer.RelationshipImpl
import java.util.ArrayList
import java.util.List


\*\*
code>.
 * @author Darrel Courrier
 * @version 1.0

class RelationshipValidatorResult

   valID = True
    List<String> messages = ArrayList<String>()
    List<MergedRelationship> merged = ArrayList<MergedRelationship>()

\*\*
code>.  Calls base class default constructor then
code> attribute.  This is the only constructor and is 
code> objects
     * will create objects of this class.
code> attribute.

    RelationshipValidatorResult(boolean valid)
        super()
        valID = valid
    

\*\*
code> attribute.
code> attribute.

    isValid()
        return valid
    

\*\*
code> attribute.
code> attribute.

   setValid(boolean valid)
        valID = valid
    

\*\*
code> attribute.
code> attribute.

     List<String> getMessages()
        return messages
    

\*\*
code> attribute. This method is
code> objects
     * will invoke it.
     * @param msg the message to be added.

    addMessage(self, msg)
        messages.append(msg)
    

\*\*
     * Generates a message from the arguments and adds the result  to the collection in the
code> attribute.This method is
code> objects
     * will invoke it.
     * @param left the first relationship that caused a problem.
     * @param right the second relationship that caused a problem.
     * @param rel the third relationship that caused a problem.

    addMessage(RelationshipImpl left,
            RelationshipImpl right,
            RelationshipImpl rel)
        setValid(False)
        MergedRelationship mr = MergedRelationship(left, right, rel)
       notFound = True
        for (int loop = 0 loop < merged.size() and notFound loop++)
            MergedRelationship mr1 = merged.get(loop)
            if (mr1.equals(mr))
                notFound = False
            
        
        if (notFound)
            merged.append(mr)
            addMessage(mr.toString())
        
    


    def __str__(self):
        StringBuilder sb = StringBuilder("Result = ")
        sb.append(valid)
        sb.append("\nMessages ( ")
        sb.append(messages.size())
        sb.append(")\nMessages:\n{\n")
        for (int loop = 0 loop < messages.size() loop++)
            sb.append("\t")
            sb.append(messages.get(loop))
            sb.append("\n")
        
        return sb.toString()
    

    class MergedRelationship

        key1
        key3
        key2
        RelationshipImpl left
        RelationshipImpl right
        RelationshipImpl rel

         MergedRelationship(RelationshipImpl left,
                RelationshipImpl right,
                RelationshipImpl rel)

            key1 = left.getRelationshipID()
            key2 = right.getRelationshipID()
            key3 = rel.getRelationshipID()
            left = left
            right = right
            rel = rel
        

    
        equals(Object obj)
           result = True
            try
                MergedRelationship mr = (MergedRelationship) obj
                Integer[] i1 = Integer[3]
                Integer[] i2 = Integer[3]
                i1[0] = key1
                i1[1] = key2
                i1[2] = key3
                i2[0] = mr.key1
                i2[1] = mr.key2
                i2[2] = mr.key3
                for (int oLoop = 0 oLoop < i1.length oLoop++)
                    for (int iLoop = 0 iLoop < i2.length iLoop++)
                        if (i1[oLoop] != None and
                                i2[iLoop] != None and
                                i1[oLoop] == i2[iLoop])
                            i1[oLoop] = None
                            i2[iLoop] = None
                        
                    
                
                for (int loop = 0 loop < i1.length and result loop++)
                    if (i1[loop] != None)
                        result = False
                    
                
                for (int loop = 0 loop < i2.length and result loop++)
                    if (i2[loop] != None)
                        result = False
                    
                

             except ClassCastException cce)
                result = False
            
            return result
        

    
        def __str__(self):
            StringBuilder sb = StringBuilder(left.toString())
            sb.append(" | ")
            sb.append(right.toString())
            sb.append(" | ")
            sb.append(rel.toString())
            return sb.toString()
        
    

