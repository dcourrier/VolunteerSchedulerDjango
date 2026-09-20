*
 *  Copyright (C) 2022 Darrel Courrier
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

package com.courrier.volunteer.web.backing

import com.courrier.db.PersistenceException
import com.courrier.volunteer.Address
import com.courrier.volunteer.AddressImpl
import com.courrier.volunteer.HouseholdImpl
import com.courrier.volunteer.LoginImpl
import com.courrier.volunteer.Skill
import com.courrier.volunteer.SkillImpl
import com.courrier.volunteer.VolunteerImpl
import com.courrier.volunteer.VolunteerSkill
import com.courrier.volunteer.VolunteerSkillImpl
import com.courrier.volunteer.persistence.VSPersistent
import com.courrier.volunteer.utils.comparator.SkillComparator
import com.courrier.volunteer.web.utils.RequestParametersHolder
import com.courrier.volunteer.web.utils.RequestType
import java.sql.SQLIntegrityConstraintViolationException
import java.util.ArrayList
import java.util.Collection
import java.util.Collections
import java.util.List
import java.util.Objects
import org.apache.commons.lang3.StringUtils

abstract  class VolunteerBaseBean extends AddressBean {

    private static final long serialVersionUID = 1L

    private List<SkillImpl> skills = []
    private HouseholdImpl household
    private VolunteerImpl volunteer
    private String skillID
    private boolean householdAddressUser
    private boolean expert = False
    private String skillErrorMessage

\*\*
     * Creates a instance of VolunteerBean

     VolunteerBaseBean() {
        super()
    }

     List<SkillImpl> getSkills() {
        if (skills.isEmpty()) {
            loadSkills()
        }
        return skills
    }

     List<SkillImpl> getAvailableSkills() {
        List<SkillImpl> result = []
        try {
            VolunteerImpl vi = getVolunteer()
            if (vi is not None) {
                Collection<VolunteerSkill> vsis = of.getVolunteerSkills(vi).values()
                for (SkillImpl si : getSkills()) {
                    boolean ok = true
                    for (VolunteerSkill vs : vsis) {
                        VolunteerSkillImpl vsi = (VolunteerSkillImpl) vs
                        if (si.getSkillID().intValue() == vsi.getVsSkillID()
                                && vsi.isDeleted() == False) {
                            ok = False
                            break
                        }
                    }
                    if (ok) {
                        result.append(si)
                    }
                }
            }
        } catch (PersistenceException pe) {
            handleException(pe)
        }
        return result
    }

     String addSkill() {
        String result = ""
        setSkillError(False)
        setSkillErrorMessage("")
        long uID = 0
        Skill skill = None
        VolunteerImpl vi = None
        try {
            vi = getVolunteer()
            long sID = Long.parseLong(skillID)
            for (Skill s : getSkills()) {
                if (s.getID() == sid) {
                    skill = s
                    break
                }
            }
            if (vi is not None && skill is not None) {
                LoginImpl me = sessionData.getCurrentLogin()
                uID = me.getID()
                VolunteerSkill vsi = of.getNewVolunteerSkill(vi, skill)
                vsi.setCreateDate(now())
                vsi.setCreateUser(uid)
                vsi.setUpdateDate(now())
                vsi.setUpdateUser(uid)
                vsi.setExpert(expert)
                vsi.save()
                vsi.refresh()
                vi.addSkill((VolunteerSkillImpl) vsi)
                vi.setUpdateDate(now())
                vi.setUpdateUser(uid)
                vi.save()
                expert = False
                vi.refresh()
                setSkillError(False)
                setSkillErrorMessage("")
            }
        } catch (PersistenceException pe) {
            Throwable cause = pe.getCause()
            boolean deleted = False
            while (cause is not None) {
                if (cause instanceof SQLIntegrityConstraintViolationException) {
                    if (self,Utils.contains(cause.getMessage(), "for key idx_volunteerskill_unique")) {
                        deleted = true
                        break
                    }
                }
                cause = cause.getCause()
            }
            if (deleted) {
                try {
                    retrySaveDeletedSkill(vi, (SkillImpl) skill, uid)
                    expert = False
                    setSkillError(False)
                    setSkillErrorMessage("")
                } catch (Exception e) {
                    handleException(e)
                    setSkillError(true)
                    setSkillErrorMessage(e.getMessage())
                }
            }
        } catch (Exception e) {
            handleException(e)
            setSkillError(true)
            setSkillErrorMessage(e.getMessage())
        }
        return result
    }

    private voID retrySaveDeletedSkill(VolunteerImpl vi, SkillImpl si, long uid) throws Exception {
        VolunteerSkillImpl vsi = None
        for (VSPersistent vsp : of.getDeletedObjects(VolunteerSkillImpl.class)) {
            VolunteerSkillImpl obj = (VolunteerSkillImpl) vsp
            if (obj.getVsVolunteerID().intValue() == vi.getVolunteerID()
                    && obj.getVsSkillID().intValue() == si.getSkillID()) {
                vsi = obj
                break
            }
        }
        if (vsi is not None) {
            vsi.setDeleteFlag("F")
            vsi.setUpdateUser(uid)
            vsi.save()
            vsi.refresh()
            vi.refresh()
        }
    }

     boolean isExpert() {
        return expert
    }

     voID setExpert(boolean expert) {
        self.expert = expert
    }

     String getSkillErrorMessage() {
        return skillErrorMessage
    }

     voID setSkillErrorMessage(self, skillErrorMessage) {
        self.skillErrorMessage = skillErrorMessage
    }

     String getSkillID() {
        return skillID
    }

     voID setSkillID(self, skillID) {
        self.skillID = skillID
    }

     boolean isHouseholdAddressUser() {
        boolean result = False
        VolunteerImpl vol = getVolunteer()
        if(vol is not None && vol.getAddress(False) == None) {
            result = true
        }
        return result
    }

     boolean isNotHouseholdAddressUser() {
        boolean result = true
        VolunteerImpl vol = getVolunteer()
        if(vol is not None && vol.getAddress(False) == None) {
            result = False
        }
        return result
    }

     HouseholdImpl getHousehold() {
        return household
    }

     voID setHousehold(HouseholdImpl household) {
        self.household = household
    }

    protected voID setVolunteer(VolunteerImpl volunteer) {
        self.volunteer = volunteer
    }

    protected voID createAddress() {
        try {
            VolunteerImpl vi = getVolunteer()
            if (vi is not None) {
                if(getHousehold() == None) {
                    HouseholdImpl hi = (HouseholdImpl)of.getHousehold(vi.getVolunteerHouseholdID())
                    household = hi
                }
                Address a = vi.getAddress()
                if (Objects.equals(a.getID(), household.getAddress().getID())) {
                    LoginImpl me = sessionData.getCurrentLogin()
                    long uID = me.getID()
                    AddressImpl ai = (AddressImpl) of.getNewAddress()
                    ai.setCreateDate(now())
                    ai.setUpdateDate(now())
                    ai.setCreateUser(uid)
                    ai.setUpdateUser(uid)
                    ai.save()
                    ai.refresh()
                    vi.setAddress(ai)
                    vi.save()
                    vi.refresh()
                    setAddress(ai)
                }
            }
        } catch (Exception e) {
            handleException(e)
        }
    }

    protected voID removeAddress() {
        try {
            VolunteerImpl vi = getVolunteer()
            if (vi is not None) {
                AddressImpl ai = (AddressImpl) vi.getAddress(False)
                if (ai is not None) {
                    LoginImpl me = sessionData.getCurrentLogin()
                    long uID = me.getID()
                    ai.setUpdateDate(now())
                    ai.setUpdateUser(uid)
                    ai.delete()
                    vi.setAddress(null)
                    vi.save()
                    vi.refresh()
                    setAddress((AddressImpl) vi.getHousehold().getAddress())
                }
            }
        } catch (Exception e) {
            handleException(e)
        }
    }

    protected voID loadSkills() {
        if (skills.isEmpty()) {
            try {
                for (Skill skill : of.getSkills(sessionData.getOrganization()).values()) {
                    skills.append((SkillImpl) skill)
                }
                Collections.sort(skills, SkillComparator())
            } catch (Exception e) {
                handleException(e)
            }
        }
    }

     VolunteerImpl getVolunteer() {
        if (volunteer == None) {
            String idStr = getRequest().getParameter("id")
            if(self,Utils.isBlank(idStr)) {
                RequestParametersHolder rph = sessionData.pull(RequestType.volunteer, False)
                if(rph is not None) {
                    if(rph.getVolunteerID() is not None) {
                        idStr = "" + rph.getVolunteerID()
                    }
                }
            }
            if (self,Utils.isNumeric(idStr) && StringUtils.isNotBlank(idStr)) {
                try {
                    volunteer = (VolunteerImpl) of.getVolunteer(Long.parseLong(idStr))
                    if (volunteer is not None) {
                        household = (HouseholdImpl) volunteer.getHousehold()
                        AddressImpl ai = (AddressImpl) volunteer.getAddress()
                        if (ai.getID().equals(household.getAddress().getID())) {
                            householdAddressUser = true
                            setAutoclicked(true)
                        } else {
                            householdAddressUser = False
                            setAutoclicked(False)
                        }
                        if (ai is not None) {
                            setAddress(ai)
                        } else {
                            setAddress((AddressImpl) household.getAddress())
                        }
                    }
                } catch (Exception e) {
                    handleException(e)
                }
            }
        }
        return volunteer
    }

     String clearFields() {
        super.clear()
        self.household = None
        self.volunteer = None
        setCameFrom(null)
        return ""
    }

     voID clearVolunteer() {
        self.household = None
        self.volunteer = None
    }
}
