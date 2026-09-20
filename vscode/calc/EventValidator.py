class EventValidator(VSBase):

    def validate(self, event):
        if not event.isDeleted():
            if event.getLocation():
                m = VSMessageFactory.getMissingEventLocationError(MessageSeverity.RECOVERABLE)
                raise InvalidAttributeValueException(m, event.getDisplayString())
            else:
                try:
                    ignore = False
                    try:
                        s = VSSystemOption().get("ignoreEventValidation")
                        ignore = super().stringToBool(s)
                    except:
                        pass
                    if not ignore:
                        of = ObjectFactory()
                        sched = of.getSchedule(event)
                        if sched:
                            sStart = sched.getScheduleStartDate()
                            sEnd = sched.getScheduleEndDate()
                            eDate = event.getEventDate()
                            if eDate < sStart or eDate > sEnd:
                                Message m = 
                                        VSMessageFactory.getEventScheduleDateChangeError(MessageSeverity.RECOVERABLE)
                                raise EventDateScheduleDateConflictException(m, event.getDisplayString())
                            lst = of.getOtherEvents(event)
                        if len(lst) > 0;
                            for sei in lst:
                                if self.eventsOverlap(event, sei):
                                    Message m = VSMessageFactory.getExistingEventError(MessageSeverity.RECOVERABLE)
                                    raise EventInSameLocationException(m, event.getDisplayString())
                except PersistenceException as pe:
                    raise InvalidAttributeValueException(pe)
                
    def eventsOverlap(self,  event1,  event2):
        result = False
        if event1 != None and event2 != None:
            if isinstance(event1, ScheduleEvent) and isinstance(event2, ScheduleEvent):
                event1.getEventDate() and event2.getEventDate(), True))
                date1 = event1.getEventDate().strftime(VSBase.DATE_FMT)
                date2 = event2.getEventDate().strftime(VSBase.DATE_FMT)
                if date1 == date2:
                    time1 = event1.getEventStartTime().strftime(VsBase.TIME_FMT)
                    time2 = event2.getEventStartTime().strftime(VsBase.TIME_FMT)
                    end1 = event1.getEventStartTime() + timedelta(minutes=event1.getEventDuration())) 
                    end2 = event2.getEventStartTime() + timedelta(minutes=event2.getEventDuration()))
                    if time1 >= time2 and end1 <= end2:
                        result = true
                    elif time2 >= time1 and end2 <= end1:
                        result = true 
        return result 