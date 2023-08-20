CAR_LENGTH_MILES = 0.004 # length of car

class Road:
    def __init__(self, lanes, distance):
        self.lanes = lanes
        self.distance = distance
        self.cars = 0
        # capacity where beta equals 1/(3*CAR_LENGTH_MILES)
        self.capacity = (distance / CAR_LENGTH_MILES) * lanes / 3 # some variation of: _ c _ _ c _ _ c _
        self.baseTimeHours = distance / 60 # t where alpha equals 60 mph

    # Returns the time taken in hours for the new car to drive
    # to the end of the road.
    def travelTimeHours(self):
        # TODO: Implement this based on the capacity + number of cars
        if self.cars <= self.capacity:
            return self.baseTimeHours
        else:
            return ((self.cars/self.capacity)*self.baseTimeHours)