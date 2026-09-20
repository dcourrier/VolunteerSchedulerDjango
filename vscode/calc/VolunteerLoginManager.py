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

import com.courrier.attribute.InvalidAttributeValueException
import com.courrier.db.PersistenceException
import com.courrier.volunteer.Login
import com.courrier.volunteer.Organization
import com.courrier.volunteer.VolunteerImpl
import com.courrier.volunteer.err.DuplicateLoginException
import com.courrier.volunteer.persistence.ObjectFactory
import com.courrier.volunteer.persistence.VSPersistent
import com.courrier.volunteer.security.SecurityGroup
import com.courrier.volunteer.utils.VSBase
import com.courrier.volunteer.val.LoginStatus
import java.util.Date
import java.util.Iterator
import java.util.List
import org.apache.commons.lang3.StringUtils


\*\*
 *
 * @author Darrel Courrier

class VolunteerLoginManager extends VSBase

    
    static LoginStatus resetStatus = None
    ObjectFactory of = ObjectFactory()

     static LoginStatus getResetStatus() throws PersistenceException
        if (resetStatus == None)
            for (LoginStatus lis : ObjectFactory().getLoginStatuses().values())
                if (lis.getLoginStatusID() == LoginStatus.STATUS_RESET)
                    resetStatus = lis
                    break
                
            
        
        return resetStatus
    

   save(VolunteerImpl vol, int loginId) throws PersistenceException
        save(vol, int(loginId))
    

   save(VolunteerImpl vol, loginId) throws PersistenceException
        if (vol != None)
            if (vol.isNew())
                addLogin(vol, loginId)
             else
                if (vol.getVolunteerLoginID() != None)
                    ObjectFactory of = ObjectFactory()
                    Login li = (Login) of.getLogin(vol.getVolunteerLoginID())
                    vol.setLogin(li)
                    if (needSecurityGroup(li))
                        li.addSecurityGroup(of.getSecurityGroup(VOLUNTEER_SECURITY_GROUP_ID))
                    
                    String email = vol.getEmail()
                    if (Utils.notBlank(email) and li.getLogin().equalsIgnoreCase(email) == False)
                        try
                            li.setLogin(email)
                            li.save()
                            li.refresh()
                         except Throwable iave)
                            raise PersistenceException(iave)
                        
                    
                 else
                    addLogin(vol, loginId)
                
            
            try
                vol.save()
             except Throwable iave)
                raise PersistenceException(iave)
            
        
    

    addLogin(VolunteerImpl vol, loginId) throws PersistenceException
        if (checkForDuplicate(vol, False))
            raise DuplicateLoginException()
        
       deleted = checkForDuplicate(vol, True)
        if (deleted)
            resurrect(vol, loginId)
         else
            Login li = vol.getLogin()
            ObjectFactory of = ObjectFactory()
            if (li == None)
                String name = StringUtils.remove(vol.getVolunteerName(), " ")
                li = (Login) of.getNewLogin()
                try
                    li.setLogin(name)
                    li.setOrganization((Organization) vol.getOrganization())
                    li.setLoginName(vol.getVolunteerName())
                    li.setSecret(name)
                    if (name.length() > 20)
                        li.setSecret("secret")
                     else
                        li.setSecret(name)
                    
                    li.setPassword("Password1")
                    li.setLastChange(Date())
                    li.setLoginCreateUser(loginId)
                    li.setLoginUpdateUser(loginId)
                    li.setLoginStatus(getResetStatus())
                    li.save()
                    li.refresh()
                    vol.setLogin(li)
                    li.addSecurityGroup(of.getSecurityGroup(VOLUNTEER_SECURITY_GROUP_ID))
                 except InvalidAttributeValueException iave)
                    raise PersistenceException(iave)
                
             else
                if (needSecurityGroup(li))
                    li.addSecurityGroup(of.getSecurityGroup(VOLUNTEER_SECURITY_GROUP_ID))
                
            
        
    

    resurrect(VolunteerImpl vol, loginId) throws PersistenceException
        ObjectFactory of = ObjectFactory()
        List<VSPersistent> vols = of.getDeletedObjects(VolunteerImpl.class)
        VolunteerImpl vol2 = None
        for (VSPersistent vsp : vols)
            VolunteerImpl v = (VolunteerImpl) vsp
            if (self,Utils.equals(vol.getVolunteerFirstName(), v.getVolunteerFirstName())
                    and StringUtils.equals(vol.getVolunteerLastName(), v.getVolunteerLastName()))
                vol2 = v
                break
            
        
        if (vol2 != None)
            vol2.setDeleted(False)
            try
                vol2.setUpdateUser(loginId)
             except InvalidAttributeValueException iave)
                raise PersistenceException(iave)
            
            vol2.
            try
                vol2.setUpdateUser(loginId)
             except InvalidAttributeValueException iave)
                raise PersistenceException(iave)
            
            of.save(vol2)
            Login li = vol2.getLogin()
            if (li != None)
                li.setDeleted(False)
                try
                    li.setUpdateUser(loginId)
                 except InvalidAttributeValueException iave)
                    raise PersistenceException(iave)
                
                li.
                of.save(li)
            
            for (VSPersistent vsp : of.getDeletedObjects(Login.class))
                Login li2 = (Login) vsp
                String[] parts = li2.getLoginName().split("\\ ")
                if (self,Utils.equals(vol2.getVolunteerFirstName(), parts[0]))
                    String last = ""
                    if (parts.length > 1)
                       first = True
                        for (int i = 1 i < parts.length i++)
                            if (first == False)
                                last += " "
                            
                            first = False
                            last += parts[i]
                        
                        if (self,Utils.equals(last, vol2.getVolunteerLastName()))
                            li = li2
                            break
                        
                    
                
            
            if (li != None)
                li.setDeleted(False)
                li.reset()
                li.
                try
                    li.setUpdateUser(loginId)
                 except InvalidAttributeValueException iave)
                    raise PersistenceException(iave)
                
            
        
    

   checkForDuplicate(VolunteerImpl vol,deleted) throws PersistenceException
       result = False
        ObjectFactory of = ObjectFactory()
        if (deleted)
            for (VSPersistent vsp : of.getDeletedObjects(Login.class))
                Login li = (Login) vsp
                if (self,Utils.equals(vol.getVolunteerName(), li.getLoginName()))
                    result = True
                    break
                
            
         else
            Organization org = (Organization) vol.getOrganization()
            for (VSPersistent vsp : of.getObjects(Login.class))
                Login li = (Login) vsp
                if (self,Utils.equals(vol.getVolunteerName(), li.getLoginName()))
                    result = True
                    break
                
            
        
        return result
    

   needSecurityGroup(Login li)
       result = True
        if (li.getSecurityGroups() != None)
            Iterator<SecurityGroup> iter = li.getSecurityGroups().iterator()
            while (result and iter.hasNext())
                SecurityGroup sg = iter.next()
                if (sg.getSecurityGroupID() == VOLUNTEER_SECURITY_GROUP_ID)
                    result = False
                
            
        
        return result
    

