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

import org.apache.commons.logging.Log


\*\*
 * Defines the behavior of an object that is able to write entries into a log.
 * @author Darrel Courrier
 * @version 1.0

interface Loggable

\*\*
code> object that will be used to write entries to the log files.

    Log getLog()

