from road import Road

class City:
    roads = {}
    maxRoadLanes = {}
    roadDistances = {}

    def __init__(self, populations):
        self.numberLocations = len(populations)
        self.populations = populations
        for i in range(self.numberLocations):
            self.roads[i] = {}
            self.maxRoadLanes[i] = {}
            self.roadDistances[i] = {}
            for j in range(self.numberLocations):
                self.maxRoadLanes[i][j] = 0
                self.roadDistances[i][j] = 0

    def setRoads(self, laneMatrix):
        for i in range(self.numberLocations):
            self.roads[i].clear()
            for j in range(self.numberLocations):
                if j == i:
                    continue

                lanes = laneMatrix[i][j]
                maxLanes = self.maxRoadLanes[i][j]

                if lanes < 0:
                    print(f"ERROR: Cannot set a negative number of lanes from location {i} to {j}")
                    return
                if lanes > maxLanes:
                    print(f"ERROR: Cannot set more than {maxLanes} lanes from location {i} to {j}")

                if lanes > 0:
                    self.roads[i][j] = Road(lanes, self.roadDistances[i][j])

    def isConnected(self):
        connected = [False for i in range(self.numberLocations)]
        todo = []
        todo.append(0)
        connected[0] = True

        while len(todo) > 0:
            i = todo.pop()
            for j in self.roads[i]:
                if not connected[j]:
                    connected[j] = True
                    todo.append(j)

        if not all(connected):
            return False

        # Check reverse connectivity.
        connected = [False for i in range(self.numberLocations)]
        todo = []
        todo.append(0)
        connected[0] = True

        while len(todo) > 0:
            i = todo.pop()
            for j in range(self.numberLocations):
                if i in self.roads[j]:
                    if not connected[j]:
                        connected[j] = True
                        todo.append(j)

        if not all(connected):
            return False

        return True