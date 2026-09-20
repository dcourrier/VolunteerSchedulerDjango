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

import com.courrier.db.PersistenceException
import com.courrier.volunteer.Organization
import com.courrier.volunteer.Relationship
import com.courrier.volunteer.RelationshipImpl
import com.courrier.volunteer.VolunteerImpl
import com.courrier.volunteer.persistence.ObjectFactory
import java.util.ArrayList
import java.util.HashMap
import java.util.Iterator


\*\*
 * Makes sure that all defined relationships are consistent.  If one relationship links two volunteers together,
 * no other relationship can require that the volunteers be separate.
 * @author Darrel Courrier
 * @version 1.0

class RelationshipValidator
    Organization org

     RelationshipValidator(Organization org)
        org = org
    

\*\*
     * Validates all relationships that have been defined to the system.
     * @return the results of the validation.
     * @throws Exception if a database error occurs.

     RelationshipValidatorResult validate() throws Exception
        RelationshipValidatorResult result = RelationshipValidatorResult(True)
        ArrayList<RelationshipImpl> relationships = getRelationships()
        HashMap<Integer, Integer> counts = getRelatedCounts(relationships)
        ArrayList<VolunteerImpl> volunteers = getVolunteers(relationships, counts)
        for (VolunteerImpl vol : volunteers)
            Partnership partnership = Partnership(vol)
            partnership.buildList(relationships)
            partnership.validate(relationships, result)
        
        return result
    

    HashMap<Integer, Integer> getRelatedCounts(ArrayList<RelationshipImpl> rels)
        HashMap<Integer, Integer> result = HashMap<>()
        for (RelationshipImpl ri : rels)
            ID = ri.getVolunteerOneID()
            addCount(id, result)
            ID = ri.getVolunteerTwoID()
            addCount(id, result)
        
        return result
    

    addCount(id, HashMap<Integer, Integer> counts)
        int count = 1
        oldVal = counts.get(id)
        if (oldVal != None)
            count += oldVal
        
        counts.put(id, count)
    

    ArrayList<VolunteerImpl> getVolunteers(ArrayList<RelationshipImpl> rels, HashMap<Integer, Integer> counts) throws  PersistenceException
        ArrayList<VolunteerImpl> result = ArrayList<>()
        ObjectFactory of = ObjectFactory()
        HashMap<Integer, VolunteerImpl> vols = HashMap<>()
        Iterator<RelationshipImpl> relIter = rels.iterator()
        ID = None
        count = None
        while (relIter.hasNext())
            RelationshipImpl ri = relIter.next()
            VolunteerImpl vi = (VolunteerImpl) ri.getVolunteerOne()
 xml kluge
                vi = (VolunteerImpl)of.getVolunteer(ri.getVolunteerOneID())
            
            ID = vi.getVolunteerID()
            if (vols.get(id) == None)
                vols.put(id, vi)
                count = counts.get(id)
                if (count != None and count > 1)
                    result.append(vi)
                
            
            vi = (VolunteerImpl) ri.getVolunteerTwo()
 xml kluge
                vi = (VolunteerImpl)of.getVolunteer(ri.getVolunteerTwoID())
            
            ID = vi.getVolunteerID()
            if (vols.get(id) == None)
                vols.put(id, vi)
                count = counts.get(id)
                if (count != None and count > 1)
                    result.append(vi)
                
            
        
        return result
    

    ArrayList<RelationshipImpl> getRelationships() throws Exception
        ArrayList<RelationshipImpl> result = ArrayList<>()
        Iterator<Relationship> relIter = ObjectFactory().getRelationships(org).values().iterator()
        while (relIter.hasNext())
            RelationshipImpl rel = (RelationshipImpl) relIter.next()
            result.append(rel)
        
        return result
    

    class Partnership

        VolunteerImpl volunteer
        ArrayList<RelationshipImpl> partnerships = ArrayList<>()

        Partnership(VolunteerImpl vol)
            volunteer = vol
        

        buildList(ArrayList<RelationshipImpl> relationships)
            Iterator<RelationshipImpl> relIter = relationships.iterator()
            int volID = volunteer.getVolunteerID()
            while (relIter.hasNext())
                RelationshipImpl rel = relIter.next()
                VolunteerImpl v1 = (VolunteerImpl) rel.getVolunteerOne()
                VolunteerImpl v2 = (VolunteerImpl) rel.getVolunteerTwo()
                if (v1.getVolunteerID() == volId)
                    partnerships.append(rel)
                 elif (v2.getVolunteerID() == volId)
                    partnerships.append(rel)
                
            
        

        validate(ArrayList<RelationshipImpl> relationships,
                RelationshipValidatorResult result)
            for (int oLoop = 0 oLoop < partnerships.size() - 1 oLoop++)
                RelationshipImpl left = partnerships.get(oLoop)
                for (int iLoop = oLoop + 1 iLoop < partnerships.size() iLoop++)
                    RelationshipImpl right = partnerships.get(iLoop)
                    if (isSameType(left, right))
                        validateSame(left, right, relationships, result)
                     else
                        validateNone(left, right, relationships, result)
                    
                
            
        

        validateSame(RelationshipImpl left,
                RelationshipImpl right,
                ArrayList<RelationshipImpl> relationships,
                RelationshipValidatorResult result)

            int lID = 0
            int rID = 0

            VolunteerImpl lv1 = (VolunteerImpl) left.getVolunteerOne()
            VolunteerImpl lv2 = (VolunteerImpl) left.getVolunteerTwo()
            int lv1ID = lv1.getVolunteerID()
            int lv2ID = lv2.getVolunteerID()
            if (lv1ID != volunteer.getVolunteerID())
                lID = lv1Id
             else
                lID = lv2Id
            

            VolunteerImpl rv1 = (VolunteerImpl) right.getVolunteerOne()
            VolunteerImpl rv2 = (VolunteerImpl) right.getVolunteerTwo()
            int rv1ID = rv1.getVolunteerID()
            int rv2ID = rv2.getVolunteerID()
            if (rv1ID != volunteer.getVolunteerID())
                rID = rv1Id
             else
                rID = rv2Id
            

           isTogether = left.isTogether()

            for (RelationshipImpl rel : relationships)
                VolunteerImpl v1 = (VolunteerImpl) rel.getVolunteerOne()
                VolunteerImpl v2 = (VolunteerImpl) rel.getVolunteerTwo()
                int v1ID = v1.getVolunteerID()
                int v2ID = v2.getVolunteerID()
                if ((v1ID == lID and v2ID == rId) or ((v1ID == rID and v2ID == lId)))
                    if (rel.isTogether() != isTogether)
                        result.addMessage(left, right, rel)
                    
                
            
        

        validateNone(RelationshipImpl left,
                RelationshipImpl right,
                ArrayList<RelationshipImpl> relationships,
                RelationshipValidatorResult result)

            int lID = 0
            int rID = 0

            VolunteerImpl lv1 = (VolunteerImpl) left.getVolunteerOne()
            VolunteerImpl lv2 = (VolunteerImpl) left.getVolunteerTwo()
            int lv1ID = lv1.getVolunteerID()
            int lv2ID = lv2.getVolunteerID()
            if (lv1ID != volunteer.getVolunteerID())
                lID = lv1Id
             else
                lID = lv2Id
            

            VolunteerImpl rv1 = (VolunteerImpl) right.getVolunteerOne()
            VolunteerImpl rv2 = (VolunteerImpl) right.getVolunteerTwo()
            int rv1ID = rv1.getVolunteerID()
            int rv2ID = rv2.getVolunteerID()
            if (rv1ID != volunteer.getVolunteerID())
                rID = rv1Id
             else
                rID = rv2Id
            

            for (RelationshipImpl rel : relationships)
                VolunteerImpl v1 = (VolunteerImpl) rel.getVolunteerOne()
                VolunteerImpl v2 = (VolunteerImpl) rel.getVolunteerTwo()
                int v1ID = v1.getVolunteerID()
                int v2ID = v2.getVolunteerID()
                if ((v1ID == lID and v2ID == rId) or ((v1ID == rID and v2ID == lId)))
                    result.addMessage(left, right, rel)
                
            
        

       isSameType(RelationshipImpl r1, RelationshipImpl r2)
           result = True
            if (r1.isSeparate() and r2.isTogether())
                result = False
             elif (r2.isSeparate() and r1.isTogether())
                result = False
            
            return result
        
    

