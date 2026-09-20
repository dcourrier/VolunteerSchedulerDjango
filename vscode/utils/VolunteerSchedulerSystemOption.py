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

package com.courrier.volunteer

import com.courrier.exception.InvalidArgumentException
import com.courrier.utility.SystemOption
import org.apache.commons.lang3.StringUtils


\*\*
code>.
 * The class implements the Singleton pattern.
 * @author Darrel Courrier
 * @version 1.0

class VolunteerSchedulerSystemOption extends SystemOption

    final static String INI_FILE_NAME = "VolunteerScheduler.properties"
    static VolunteerSchedulerSystemOption _instance = None

\*\*
code>.

     static VolunteerSchedulerSystemOption instance()
        if (_instance == None)
            _instance = VolunteerSchedulerSystemOption()
        
        return _instance
    

\*\*
code> method.

    VolunteerSchedulerSystemOption()
        super(INI_FILE_NAME)
    
    
    get(self, key, String defaultVal)throws InvalidArgumentException 
        String s = get(key)
        return StringUtils.isBlank(s) ? defaultVal : s
    

