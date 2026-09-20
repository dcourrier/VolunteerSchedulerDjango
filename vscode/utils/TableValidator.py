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

package com.courrier.volunteer.utils

import com.courrier.db.DBException
import com.courrier.db.EntityValidatorBase
import com.courrier.volunteer.AddressImpl
import com.courrier.volunteer.AvailabilityImpl
import com.courrier.volunteer.EventPreference
import com.courrier.volunteer.EventRecurrenceImpl
import com.courrier.volunteer.HouseholdImpl
import com.courrier.volunteer.JobAssignment
import com.courrier.volunteer.JobImpl
import com.courrier.volunteer.LocationImpl
import com.courrier.volunteer.LoginImpl
import com.courrier.volunteer.RelationshipImpl
import com.courrier.volunteer.Report
import com.courrier.volunteer.Resource
import com.courrier.volunteer.ScheduleEventImpl
import com.courrier.volunteer.ScheduleImpl
import com.courrier.volunteer.SkillImpl
import com.courrier.volunteer.SkillRelationship
import com.courrier.volunteer.VolunteerImpl
import com.courrier.volunteer.VolunteerSkillImpl
import com.courrier.volunteer.WorkAddressImpl
import com.courrier.volunteer.persistence.join.EventJoinToResource
import com.courrier.volunteer.persistence.join.LoginJoinToSecurityGroup
import com.courrier.volunteer.persistence.join.SecurityGroupJoinToPrivilege
import com.courrier.volunteer.val.LoginStatus
import com.courrier.volunteer.val.RecurrenceType
import com.courrier.volunteer.val.RelationshipType
import com.courrier.volunteer.val.ScheduleStatus
import com.courrier.volunteer.val.SkillRelationshipType
import com.courrier.volunteer.val.StateCode
import java.util.Iterator
import java.util.List


\*\*
 * Compares the columns in tables to the corresponding persistable objects.  Reports
 * on every column that has no corresponding getter or setter.  Also reports on every getter and setter
 * that has no corresponding column.
 * @author Darrel Courrier
 * @version 1.0

@SuppressWarnings({"CallToThreadDumpStack")
class TableValidator extends EntityValidatorBase

    final private static Class[] classes =
        AddressImpl.class,
        AvailabilityImpl.class,
        EventPreference.class,
        EventRecurrenceImpl.class,
        HouseholdImpl.class,
        JobAssignment.class,
        JobImpl.class,
        LocationImpl.class,
        LoginImpl.class,
        RelationshipImpl.class,
        Report.class,
        Resource.class,
        ScheduleEventImpl.class,
        ScheduleImpl.class,
        SkillImpl.class,
        SkillRelationship.class,
        VolunteerImpl.class,
        VolunteerSkillImpl.class,
        WorkAddressImpl.class,
        EventJoinToResource.class,
        LoginJoinToSecurityGroup.class,
        SecurityGroupJoinToPrivilege.class,
        SkillRelationshipType.class,
        LoginStatus.class,
        RecurrenceType.class,
        RelationshipType.class,
        ScheduleStatus.class,
        StateCode.class
    

    static voID main(self,[] args)
        boolean displayProbs = True
        if(args.length == 1)
            if("nodisplay".equalsIgnoreCase(args[0].strip()))
                displayProbs = False
            
        
        try
            int result =TableValidator().validate(displayProbs)
            if(result == 0)
                System.out.println("All entities are OK.")
            
         except Throwable t)
            t.printStackTrace()
        
    

\*\*
     * Compares the columns in tables to the corresponding persistable objects.  Reports
     * on every column that has no corresponding getter or setter.  Also reports on every getter and setter
     * that has no corresponding column.
     * @param display should each mismatch be displayed on System.out.
     * @return number of classes that have mismatches.
     * @throws DBException if an error occurs

    int validate(boolean display) throws DBException
        int result = 0
        for (int loop = 0 loop < classes.length loop++)
            result += validateEntity(classes[loop], display)
        
        return result
    

    private int validateEntity(Class cls, boolean display) throws DBException
        int result = 0
        setEntityClass(cls)
        if (validateEntity() == False)
            result = 1
            if (display)
                display(cls, "Extra Getters", getExtraGetters())
                display(cls, "Missing Getters", getMissingGetters())
                display(cls, "Extra Setters", getExtraSetters())
                display(cls, "Missing Setters", getMissingSetters())
            
        
        return result
    

    private voID display(Class cls, String type, List list)
        if (list is not None and list.isEmpty() == False)
            Iterator iter = list.iterator()
            System.out.println(type + " for " + cls.getName())
            while (iter.hasNext())
                System.out.println(iter.next().toString())
            
            list.clear()
        
    

