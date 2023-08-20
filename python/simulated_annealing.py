import math, random
import copy

from simulator import Simulator

memoization = {}
def energy(simulator, laneMatrix):
    memoKey = ((x for x in row) for row in laneMatrix)
    if memoKey not in memoization:
        simulator.city.setRoads(laneMatrix)
        memoization[memoKey] = simulator.simulate()
    return memoization[memoKey]

def probability(energyCurrent, energyNext, temperature):
    return math.exp((energyCurrent - energyNext) / temperature)

def getTemperature(t):
    return 0.001*(1-t)

def optimize(city, iterations):
    simulator = Simulator(city)
    laneMatrix = []
    bestMatrix = []
    bestEnergy = math.inf

    for i in range(city.numberLocations):
        laneMatrix.append([])
        for j in range(city.numberLocations):
            if i == j:
                laneMatrix[i].append(0)
            else:
                laneMatrix[i].append(city.maxRoadLanes[i][j])
    # laneMatrix = [
    # [0,0,5,0],
    # [0,0,5,5],
    # [5,5,0,0],
    # [0,5,0,0],
    # ]
    curr_energy = energy(simulator,laneMatrix)
    bestMatrix = copy.deepcopy(laneMatrix)
    bestEnergy = curr_energy
    print('original matrix:', laneMatrix)
    print('original energy: ',bestEnergy)
    for iter in range(iterations):
        print('iter: '+str(iter/iterations))
        temperature = getTemperature(iter / iterations)
        # TODO: Choose a valid neighbor for the nextLaneMatrix and decide whether or not
        # to accept the neighbor based on probability().
        # print(laneMatrix)
        nextLaneMatrix = copy.deepcopy(laneMatrix)
        i = random.randint(0, city.numberLocations-1)
        j = random.randint(0, city.numberLocations-1)
        while city.maxRoadLanes[i][j] == 0: # if max road lanes is zero choose another location
            i = random.randint(0, city.numberLocations-1)
            j = random.randint(0, city.numberLocations-1)
        # rand_lanes = random.randint(0, city.maxRoadLanes[i][j])
        # nextLaneMatrix[i][j] = rand_lanes
        # nextLaneMatrix[j][i] = rand_lanes
        # r = random.uniform(0, 1)
        # if (r <= 0.5 and nextLaneMatrix[i][j] > 0) or nextLaneMatrix[i][j] == city.maxRoadLanes[i][j]:
        #     nextLaneMatrix[i][j] -= 1
        # else:
        #     nextLaneMatrix[i][j] += 1
        while nextLaneMatrix == laneMatrix: #keep going if no change
            r = random.uniform(0, 1)
            if r < 0.5:
                nextLaneMatrix[i][j] = 0
                nextLaneMatrix[j][i] = 0
            else:
                # rand_lanes = random.randint(1, city.maxRoadLanes[i][j])
                # nextLaneMatrix[i][j] = rand_lanes
                nextLaneMatrix[i][j] = city.maxRoadLanes[i][j]
                nextLaneMatrix[j][i] = city.maxRoadLanes[j][i]
        simulator.city.setRoads(nextLaneMatrix)
        # while city.isConnected() is False: # if city is not connected
        #     nextLaneMatrix = copy.deepcopy(laneMatrix)
        #     rand_lanes = random.randint(0, city.maxRoadLanes[i][j])
        #     nextLaneMatrix[i][j] = rand_lanes
        #     simulator.city.setRoads(nextLaneMatrix)
        while city.isConnected() is False: # if city is not connected
            nextLaneMatrix = copy.deepcopy(laneMatrix)
            i = random.randint(0, city.numberLocations-1)
            j = random.randint(0, city.numberLocations-1)
            while city.maxRoadLanes[i][j] == 0: # if max road lanes is zero choose another location
                i = random.randint(0, city.numberLocations-1)
                j = random.randint(0, city.numberLocations-1)
            # rand_lanes = random.randint(0, city.maxRoadLanes[i][j])
            # nextLaneMatrix[i][j] = rand_lanes
            # nextLaneMatrix[j][i] = rand_lanes
            # r = random.uniform(0, 1)
            # if (r <= 0.5 and nextLaneMatrix[i][j] > 0) or nextLaneMatrix[i][j] == city.maxRoadLanes[i][j]:
            #     nextLaneMatrix[i][j] -= 1
            # else:
            #     nextLaneMatrix[i][j] += 1
            while nextLaneMatrix == laneMatrix: #keep going if no change
                r = random.uniform(0, 1)
                if r < 0.5:
                    nextLaneMatrix[i][j] = 0
                    nextLaneMatrix[j][i] = 0
                else:
                    # rand_lanes = random.randint(1, city.maxRoadLanes[i][j])
                    # nextLaneMatrix[i][j] = rand_lanes
                    nextLaneMatrix[i][j] = city.maxRoadLanes[i][j]
                    nextLaneMatrix[j][i] = city.maxRoadLanes[j][i]
            simulator.city.setRoads(nextLaneMatrix)
        r = random.uniform(0, 1)
        energyNext = energy(simulator, nextLaneMatrix)
        print('new matrix',nextLaneMatrix)
        if r < probability(curr_energy, energyNext,temperature):
            laneMatrix = copy.deepcopy(nextLaneMatrix) # nextLaneMatrix
            curr_energy = energyNext
        if curr_energy < bestEnergy:
            bestEnergy = curr_energy
            bestMatrix = copy.deepcopy(laneMatrix)
        print('current best matrix: ', bestMatrix)
    print('best energy: ',bestEnergy)
    print('return lane matrix: ',bestMatrix)
    print('retun matrix energy:', energy(simulator, bestMatrix))
    return bestMatrix