import heapq, random
from person import Person
import time

# DEPARTURE_RATE = 25.0 #100.0
# DEPARTURE_RATE = 100.0 #100.0
# DEPARTURE_RATE = 150.0 #100.0
DEPARTURE_RATE = 200.0 #100.0
# DEPARTURE_RATE = 300.0 #100.0
# DEPARTURE_RATE = 400.0 #100.0
# DEPARTURE_RATE = 500.0 #100.0
# DEPARTURE_RATE = 600.0 #100.0
# DEPARTURE_RATE = 700.0 #100.0
# DEPARTURE_RATE = 1000.0 #100.0
END_TIME_HOURS = 2.0
# END_TIME_HOURS = 10.0

class Simulator:
    def __init__(self, city):
        self.city = city

    def reset(self):
        self.timeSpentInTraffic = 0
        self.timeSpentOnRoads = 0
        self.totalTripsMade = 0
        self.time = 0
        self.events = []
        self.people = []
        self.populations = []

        for i in range(self.city.numberLocations):
            self.populations.append(self.city.populations[i])
            for j in range(self.populations[i]):
                self.people.append(Person(i, self.city))

        for s in self.city.roads:
            for t in self.city.roads[s]:
                self.city.roads[s][t].cars = 0

        for person in self.people:
            person.destination = random.randint(0, self.city.numberLocations-1)
            while (person.destination == person.home):
                person.destination = random.randint(0, self.city.numberLocations-1)
            nextLocation = computeNextLocation(person, self.city)
            departureTime = random.expovariate(DEPARTURE_RATE)
            # why false? what is the point is isArrival?
            heapq.heappush(self.events, person.getEvent(departureTime, nextLocation, False))

    def nextEvent(self):
        # TODO: Process the next event and add a new event for the given person.
        # You will update the time variable based on the event time.
        event = heapq.heappop(self.events) # pop off event
        person = event.person # get person
        self.time = event.time
        if event.isArrival is True:
            self.totalTripsMade += 1
            self.city.roads[person.currentLocation][event.destination].cars -=1 # remove car from road just travelled
            person.currentLocation = event.destination
            if (person.currentLocation is person.home) or (person.currentLocation is person.destination): # arriving at person's destination
                if person.currentLocation is person.home:
                    # print('arrived home')
                    person.destination = random.randint(0, self.city.numberLocations-1)
                    while (person.destination == person.home):
                        person.destination = random.randint(0, self.city.numberLocations-1)
                else:
                    # print('arrived at destination')
                    person.destination = person.home
                event.destination = computeNextLocation(person, self.city)
                waitTime = random.expovariate(DEPARTURE_RATE)
                departureTime = event.time + waitTime
                event.time = departureTime
                event.isArrival = False
                heapq.heappush(self.events, event) # waiting (not travelling)
                self.populations[person.currentLocation] += 1 # add one population of current location
            else: # arriving at intermediate location
                # print('intermediate travelling')
                event.destination = computeNextLocation(person, self.city)
                r = self.city.roads[person.currentLocation][event.destination]
                arrivalTime = event.time + r.travelTimeHours()
                event.time = arrivalTime
                event.isArrival = True
                heapq.heappush(self.events, event) # travelling (no time spent at intermediate location)
                # self.city.roads[person.currentLocation][event.destination].cars +=1 # add car to new road
                r.cars+=1 # add car to new road
                self.timeSpentInTraffic =  self.timeSpentInTraffic + (r.travelTimeHours() - r.baseTimeHours) # time spent in traffic
                self.timeSpentOnRoads =  self.timeSpentOnRoads + r.travelTimeHours() # time spent on road
        else:
            # print('start travelling')
            event.destination = computeNextLocation(person, self.city)
            r = self.city.roads[person.currentLocation][event.destination]
            arrivalTime = event.time + r.travelTimeHours()
            event.time = arrivalTime
            event.isArrival = True
            heapq.heappush(self.events, event) # travelling
            self.city.roads[person.currentLocation][event.destination].cars +=1 # add car to road
            self.timeSpentInTraffic =  self.timeSpentInTraffic + (r.travelTimeHours() - r.baseTimeHours) # time spent in traffic
            self.timeSpentOnRoads =  self.timeSpentOnRoads + r.travelTimeHours() # time spent on road
            self.populations[person.currentLocation] -= 1 # remove one person from population of leaving location


    def simulate(self):
        self.reset()
        startTime = time.time()

        while self.time < END_TIME_HOURS:
            self.nextEvent()

        trafficRatio = self.timeSpentInTraffic / self.timeSpentOnRoads

        print(f"Total trips made: {self.totalTripsMade}")
        print(f"Time spent on roads: {self.timeSpentOnRoads}")
        print(f"Time spent in traffic: {self.timeSpentInTraffic}")
        print(f"Energy in system: {trafficRatio}")
        print(f"System time elapsed (sec): {time.time() - startTime}")
        print(f"Departure Rate: {DEPARTURE_RATE}")

        return trafficRatio

# Essentially run Dijkstra's algorithm to simulate their GPS giving them the fastest route.
MAX_VERTICES = 10
done = [False for i in range(MAX_VERTICES)]
ret = [[0,0] for i in range(MAX_VERTICES)]
priorityQueue = []
def computeNextLocation(person, city):
    n = city.numberLocations
    source = person.currentLocation
    target = person.destination

    for i in range(n):
        ret[i][0] = ret[i][1] = -1
        done[i] = False
    priorityQueue.clear()

    ret[source][0] = 0
    done[source] = True

    for v in city.roads[source]:
        r = city.roads[source][v]
        ret[v][0] = r.travelTimeHours()
        ret[v][1] = source
        heapq.heappush(priorityQueue, (r.travelTimeHours(), v))

    while not done[target]:
        minimumCost, minimumCostVertex = heapq.heappop(priorityQueue)
        while done[minimumCostVertex]:
            minimumCost, minimumCostVertex = heapq.heappop(priorityQueue)

        done[minimumCostVertex] = True

        for v in city.roads[minimumCostVertex]:
            if done[v]:
                continue
            r = city.roads[minimumCostVertex][v]
            newCost = minimumCost + r.travelTimeHours()
            if ret[v][0] == -1 or ret[v][0] > newCost:
                ret[v][0] = newCost
                ret[v][1] = minimumCostVertex
                heapq.heappush(priorityQueue, (newCost, v))


    v = target
    while int(ret[v][1]) != source:
        v = int(ret[v][1])
    return v