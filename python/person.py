class Person:
    def __init__(self, home, city):
        self.home = home
        self.currentLocation = home
        self.city = city
        self.event = Event()
    
    def getEvent(self, time, destination, isArrival):
        self.event.time = time
        self.event.person = self
        self.event.destination = destination
        self.event.isArrival = isArrival
        return self.event
    
class Event:
    def __lt__(self, other):
        return self.time < other.time
    
    def __gt__(self, other):
        return self.time > other.time
    
    def __eq__(self, other):
        return self.time == other.time