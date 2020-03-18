import random
import math
import geometry as geo

worldWidth  = 800
worldHeight = 600

incubationTime = 21 #threeweeks
population = 1000
nbOfInfectionsAtStart=5
polutionRadius = 5
deathRate = 100
ticksPerDay = 10

class Human():
    def __init__(self, age=30, infectedDays=0):
        self.pos = geo.randPos(polutionRadius, worldWidth, polutionRadius, worldHeight)
        self.age = age
        self.isAlive = True
        self.infectedDays = infectedDays
        self.hasRecovered = False
        self.speed = 1
        self.deadIndays = 0
        self.way = []
    
    def move(self):
        if self.isAlive:
            if len(self.way) > 0:
                self.pos = self.way[0]
                self.way = self.way[1:]
            else:
                newPos = geo.randPos(0, worldWidth, 0, worldHeight)
                self.way = geo.calcLine(self.pos, newPos, self.speed)
                
class SmartHuman(Human):
    def move(self):
        pass

class World():
    def __init__(self, smartPopulationPercent=0):
        self.citicens = []
        infections = nbOfInfectionsAtStart
        smartHumans = population * smartPopulationPercent / 100
        self.nextDead = deathRate
        self.ticks = 0
        self.days = 0
        self.statInfected = []
        self.statRecovered = []
        self.statDied = []
        self.dataPopulation = None
        self.dataInfected = None
        self.dataDied = None
        self.dataRecovered = None
        for i in range(0, population):
            if(infections > 0):
                self.citicens.append(Human(random.randrange(1, 90), incubationTime))
            else:
                if (smartHumans > 0):
                    self.citicens.append(SmartHuman(random.randrange(1, 90)))
                    smartHumans = smartHumans - 1
                else:
                    self.citicens.append(Human(random.randrange(1, 90)))
            infections = infections - 1
    
    def updateData(self):
        aliveHumans = list(filter(lambda h: h.isAlive, self.citicens))
        recoveredHumans = list(filter(lambda h: h.hasRecovered, self.citicens))
        infectedHumans = list(filter(lambda h : h.infectedDays > 0, aliveHumans))
        self.dataPopulation = len(self.citicens)
        self.dataInfected = len(infectedHumans)
        self.dataDied = len(self.citicens)-len(aliveHumans)
        self.dataRecovered = len(recoveredHumans)
    def tick(self):
        self.ticks = self.ticks + 1
        aliveHumans = list(filter(lambda h: h.isAlive, self.citicens))
        infectedHumans = list(filter(lambda h : h.infectedDays > 0, aliveHumans))
        n = 0
        if self.ticks % ticksPerDay == 0:
            self.days = self.days + 1
        for human in aliveHumans:
            if not((human.infectedDays > 0) or human.hasRecovered): #ignore already infected and recovered citicens
                for infected in infectedHumans:
                    d = geo.getDistance(geo.getRectangele(human.pos, infected.pos))
                    if d <= polutionRadius:
                        human.infectedDays = incubationTime #got infected.
            if human.infectedDays > 0 and self.ticks % ticksPerDay == 0:
                human.infectedDays = human.infectedDays -1
                if human.infectedDays == 0:
                    human.hasRecovered = True
            human.move()
            n = n + 1
        self.updateData()
        if self.ticks % ticksPerDay == 0:
            self.statInfected.append(self.dataInfected)
            self.statRecovered.append(self.dataRecovered)

import pygame
import sys
import matplotlib.pyplot as plt

pygame.init()
screen = pygame.display.set_mode((worldWidth+polutionRadius*2, worldHeight+polutionRadius*2))
paused = False
fps = pygame.time.Clock()

fontConsolas = pygame.font.SysFont("consolas", 21)

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255, 255, 0)
GRAY  = (20,20,20)
WHITE = (255, 255, 255)

for smartPeople in range(0, 95, 5):
    world = World(smartPeople)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    paused = not paused
        if not paused:
            screen.fill(BLACK)
            for human in world.citicens:
                color = YELLOW
                if not(human.isAlive):
                    color = GRAY
                elif human.hasRecovered:
                    color = GREEN
                elif human.infectedDays > 0:
                    color = RED
                x, y = human.pos
                if len(human.way) > 0:
                    xt, yt = human.way[-1]
                    pygame.draw.line(screen, GRAY, [x+polutionRadius, y+polutionRadius], [xt+polutionRadius, yt+polutionRadius], 1)
                pygame.draw.circle(screen, color, [x+polutionRadius, y+polutionRadius], polutionRadius, 0)
            world.tick()
            text = fontConsolas.render("Day:%d Population:%d Infected:%d Recovered:%d" % (world.days, world.dataPopulation, world.dataInfected, world.dataRecovered), True, WHITE)
            screen.blit(text, (0, 0))
            text = fontConsolas.render("SmartPeople: %d%%" % (smartPeople), True, WHITE)
            screen.blit(text, (0, 25))
            pygame.display.update()
            fps.tick(60)
            if(world.dataInfected == 0):
                paused = True
        else:
            plt.clf()
            plt.title('People Staying at home: %03d%%' % (smartPeople))
            plt.plot(world.statInfected, label='infected')
            plt.plot(world.statRecovered, label='recovered')
            plt.ylabel('people')
            plt.xlabel('days')
            plt.xlim(0,200)
            plt.ylim(0, population)
            plt.legend(framealpha=1, frameon=True);
            plt.savefig('%03dPercent.png' % (smartPeople))
            paused = False
            break