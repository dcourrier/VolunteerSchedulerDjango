class ResourceAvailability():

    def __init__(self, resource=None,count=0):    
        self.resource = resource
        self.count = count

    def getResource(self):
        return self.resource
    
    def getCount(self):
        return self.count
    
    def setCount(self, count):
        self.count = count
    
    def __str__(self):
        return self.resource.getName() + " " + str(self.count)
    