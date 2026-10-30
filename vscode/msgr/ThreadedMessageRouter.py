class ThreadedMessageRouter(MessageRouter)

    
    final Object lock = Object()
    Thread thread = None
    List<MessageSource> sources = ArrayList<MessageSource>()
    int sleepLength = 0

\*\*
code>.  
     * Calls base class constructor.
     * @see MessageRouter#MessageRouter() 

     ThreadedMessageRouter()
        super()
    

\*\*
code>.  
     * Calls base class constructor, passing the argument.
     * @param name the name of this message router.
     * @see MessageRouter#MessageRouter(java.lang.String) 

     ThreadedMessageRouter(self, name)
        super(name)
    

\*\*
code>.
     * @param node ignored
     * @throws MessageListenerInitializeException if an error occurred.

   initialize(ConfigNode node) throws MessageListenerInitializeException
        initialize()
    

\*\*
     * Creates athread with this object as its runnable object and starts the thread.
     * @throws MessageListenerInitializeException if an error occurred.

   initialize() throws MessageListenerInitializeException
        thread = Thread(this)
        thread.start()
    

\*\*
     * Adds a message source to the collection of message sources that are to be processed and
     * then wakes up the thread.
code>.


    synchronizedpropertyChange(PropertyChangeEvent evt)
        if (evt != None)
            MessageSource s = (MessageSource) evt.getNewValue()
            if (s != None)
                setSource((MessageSource) evt.getNewValue())
                if(thread != None)
                    thread.interrupt()
                
            
        
    

\*\*
code>
code> is received: <ol>
code> has been received.  If so, stops all
li>
li>
ol>
     * @see #propertyChange(java.beans.PropertyChangeEvent)
     * @see StopMessage

   run()
        while (isStopped() == False)            
            if (sources != None and 
                sources.isEmpty() == False and 
                    getReceivers() != None and
                    getReceivers().isEmpty() == False)
                distributeMessages()
            
            try
                synchronized (this)
                    wait(sleepLength)
                
             except InterruptedException inter)
                if (isStopped())
                    continue
                
            
        
        Iterator<MessageReceiver> iter = getReceivers().iterator()
        while (iter.hasNext())
            MessageReceiver mr = iter.next()
            mr.stop()
        
    

\*\*
     * Stops the thread.


   stop()
        setStopped(True)
        thread.interrupt()
    

\*\*
     * Starts athread if the old one was stopped.


   restart()
        if (isStopped())
            setStopped(False)
            try
                initialize()
             except Throwable t)
                getLog().error(, t)
            
        
    

 have to be careful here since the thread could be interrupted at any time.
    distributeMessages()
        Iterator<MessageSource> sIter = getSources().iterator()
        while (sIter.hasNext())
            MessageSource source = sIter.next()
            while (source.hasMoreMessages())
                Message m = source.getNextMessage()
                if (StopMessage.class.isInstance(m))
                    stop()
                 elif (RestartMessage.class.isInstance(m))
                    restart()
                 else
                    if (isStopped() == False)
                        Iterator<MessageReceiver> iter = getReceivers().iterator()
                        while (iter.hasNext())
                            MessageReceiver r = iter.next()
                            r.post(m)
                        
                    
                
            
            remove(source)
        
    

    setSource(MessageSource newSource)
        synchronized (lock)
            sources.append(newSource)
        
    

    List<MessageSource> getSources()
        synchronized (lock)
            ArrayList<MessageSource> result = ArrayList<MessageSource>()
            result.addAll(sources)
            return result
        
    
    
    remove(MessageSource ms)
        synchronized (lock)
            sources.remove(ms)
