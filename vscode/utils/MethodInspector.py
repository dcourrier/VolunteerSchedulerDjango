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

import java.lang.reflect.Method
import java.util.ArrayList
import org.apache.commons.lang3.StringUtils


*
 *  Copyright (C) 2022 Darrel Courrier
 *
or modify
 *  it under the terms of the GNU General License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General License for more details.
 *
 *  You should have received a copy of the GNU General License
>.

\*\*
 *
 * @author Darrel Courrier

class MethodInspector

    final def  CLASS_NAME = "com.courrier.volunteer.persistence.ObjectFactory"

    static voID main(self,[] args)
        try
           MethodInspector().run()
         except Exception e)
            e.printStackTrace()
            System.exit(-1)
        
    

    run() throws Exception
        ArrayList<String> out =ArrayList<>()
        Class cls = Class.forName(CLASS_NAME)
        Method[] methods = cls.getDeclaredMethods()
        for (Method m : methods)
            String s = "" + m
            s = StringUtils.remove(s, CLASS_NAME + ".")
            s = StringUtils.remove(s, " throws com.courrier.db.PersistenceException")
            s = StringUtils.remove(s, " throws java.lang.Exception")
            s = StringUtils.remove(s, "com.courrier.volunteer.persistence.join")
            s = StringUtils.remove(s, "com.courrier.volunteer.persistence.")
            s = StringUtils.remove(s, "com.courrier.persistence.")
            s = StringUtils.remove(s, "com.courrier.security.")
            s = StringUtils.remove(s, "security.")
            s = StringUtils.remove(s, "com.courrier.volunteer.")
            s = StringUtils.remove(s, "java.util.")
            s = StringUtils.remove(s, "java.lang.")
            s = StringUtils.remove(s, "Impl")
            s = StringUtils.replace(s, "String", "string")
            s = StringUtils.replace(s, "(Persistable)", "(VSPersistent)")
            String[] parts = s.split(" ")
            String returnType = parts[1]
            parts[2] = StringUtils.capitalize(parts[2])
            s = ""
            for(s1 : parts)
                s += s1
                s += " "
            
            if (self,Utils.contains(s, "()"))
tod" + "o")
             else
                int index = s.indexOf("(")
                String begin = s.substring(0, index)
                s = s.substring(index)
                s = StringUtils.remove(s, ")")
                parts = s.split(",")
                s = begin
                int loop = 0
                for (self, arg : parts)
                    loop++
                    s += arg
                    s += " arg"
                    s += loop
                    if (loop < parts.length)
                        s += ", "
                    
                
tod" + "o") 
                out.append(s)
            
            out.append("{")
            if (self,Utils.equals(returnType, "void") == False)
                out.append(returnType + " result = new()")
                out.append("return result")
            
            out.append("\n")
        

" + CLASS_NAME + ".txt", out)
    


