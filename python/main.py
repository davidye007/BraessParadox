from city import City
from simulator import Simulator
from simulated_annealing import optimize
from simulated_annealing import energy
import os, pygame, sys

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 640
COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
ASSET_PATH = "assets"
def load_asset(path):
  return pygame.image.load(os.path.join(ASSET_PATH, path))


#  The number of minutes that will elapse in the simulator per second of real running time.
VISUAL_MODE_MIN_PER_SEC = 10
#TODO: The default lane matrix to use. Feel free to edit this to test out different configurations manually.
# DEFAULT_LANE_MATRIX = [
#     [0,2,5,0],
#     [2,0,5,5],
#     [5,5,0,2],
#     [0,5,2,0],
# ]
# DEFAULT_LANE_MATRIX = [
#     [0,2,2,0],
#     [2,0,0,2],
#     [2,0,0,2],
#     [0,2,2,0],
# ]
# DEFAULT_LANE_MATRIX = [
#     [0,2,5,0],
#     [2,0,0,2],
#     [5,0,0,2],
#     [0,2,2,0],
# ]
DEFAULT_LANE_MATRIX = [
    [0,2,5,0],
    [2,0,0,5],
    [5,0,0,2],
    [0,5,2,0],
]
# DEFAULT_LANE_MATRIX = [
#     [0,0,5,0],
#     [0,0,5,5],
#     [5,5,0,0],
#     [0,5,0,0],
# ]
# simulated annealing iteration
SA_ITERATIONS = 20
# use simulated annealing
USE_SA = True

POPULATIONS = [2000, 500, 500, 2000]
DISTANCES = [
    [0,2,4,0],
    [2,0,1,4],
    [4,1,0,2],
    [0,4,2,0],
]
MAX_LANES = [
    [0,2,5,0],
    [2,0,5,5],
    [5,5,0,2],
    [0,5,2,0],
]
# MAX_LANES = [
#     [0,2,5,0],
#     [2,0,1,5],
#     [5,1,0,2],
#     [0,5,2,0],
# ]

time = 0.0

city = City(POPULATIONS)
for i in range(len(POPULATIONS)):
    for j in range(len(POPULATIONS)):
        if DISTANCES[i][j] != 0:
            city.roadDistances[i][j] = DISTANCES[i][j]
            city.maxRoadLanes[i][j] = MAX_LANES[i][j]

simulator = Simulator(city)
if USE_SA:
    laneMatrix = optimize(city, SA_ITERATIONS)
else:
    laneMatrix = DEFAULT_LANE_MATRIX

city.setRoads(laneMatrix)
iters = 5
total_energy = 0
for i in range(iters):
    total_energy += energy(simulator, laneMatrix)
print('average lane matrix energy:', total_energy/iters)

simulator.reset()

pygame.init()
font = pygame.font.SysFont(None, 20)
cityTexture = load_asset("city.png")
roadTextures = {i: {} for i in range(len(POPULATIONS))}
for i in range(len(POPULATIONS)):
    for j in range(len(POPULATIONS)):
        if DISTANCES[i][j] != 0:
            roadTextures[i][j] = load_asset(f"road_{i+1}_{j+1}.png")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((255,255,255))
    screen.blit(cityTexture, cityTexture.get_rect())
    for i in range(city.numberLocations):
        for j in city.roads[i]:
            road = city.roads[i][j]
            t = min(0.5*road.cars / road.capacity, 1)
            texture = roadTextures[i][j].copy()
            texture.fill((255*0.8*t, 255*0.8*(1-t), 0), special_flags=pygame.BLEND_MULT)
            screen.blit(texture, texture.get_rect())

    # Hardcoded rendering for population sizes + road usage
    screen.blit(font.render(f"Population {simulator.populations[0]}", True, COLOR_BLACK), (60,50))
    screen.blit(font.render(f"Population {simulator.populations[1]}", True, COLOR_BLACK), (300,200))
    screen.blit(font.render(f"Population {simulator.populations[2]}", True, COLOR_BLACK), (300,370))
    screen.blit(font.render(f"Population {simulator.populations[3]}", True, COLOR_BLACK), (560,480))
    roads = city.roads
    if 1 in roads[0]:
        screen.blit(font.render(f"{round(roads[0][1].cars/roads[0][1].capacity*10)/10}x", True, COLOR_BLACK), (200, 210))
    if 0 in roads[1]:
        screen.blit(font.render(f"{round(roads[1][0].cars/roads[1][0].capacity*10)/10}x", True, COLOR_BLACK), (220, 180))
    if 2 in roads[1]:
        screen.blit(font.render(f"{round(roads[1][2].cars/roads[1][2].capacity*10)/10}x", True, COLOR_BLACK), (300, 340))
    if 0 in roads[2]:
        screen.blit(font.render(f"{round(roads[2][0].cars/roads[2][0].capacity*10)/10}x", True, COLOR_BLACK), (60, 410))
    if 1 in roads[2]:
        screen.blit(font.render(f"{round(roads[2][1].cars/roads[2][1].capacity*10)/10}x", True, COLOR_BLACK), (360, 340))
    if 2 in roads[0]:
        screen.blit(font.render(f"{round(roads[0][2].cars/roads[0][2].capacity*10)/10}x", True, COLOR_BLACK), (20, 410))
    if 3 in roads[1]:
        screen.blit(font.render(f"{round(roads[1][3].cars/roads[1][3].capacity*10)/10}x", True, COLOR_BLACK), (640, 260))
    if 1 in roads[3]:
        screen.blit(font.render(f"{round(roads[3][1].cars/roads[3][1].capacity*10)/10}x", True, COLOR_BLACK), (675, 260))
    if 3 in roads[2]:
        screen.blit(font.render(f"{round(roads[3][2].cars/roads[3][2].capacity*10)/10}x", True, COLOR_BLACK), (460, 475))
    if 2 in roads[3]:
        screen.blit(font.render(f"{round(roads[2][3].cars/roads[2][3].capacity*10)/10}x", True, COLOR_BLACK), (440, 525))

    # print("on the way arriving at destination" +str(time))
    while simulator.time < time:
        simulator.nextEvent()
    time += VISUAL_MODE_MIN_PER_SEC / 3600


    pygame.display.flip()
    clock.tick(60)
