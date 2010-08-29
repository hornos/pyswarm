from swarm import Agent, Vector
import random

# number of swarms
Fishes = 50
Sharks = 4
Planktii = 100

class Fish(Agent):
    def __init__(self):
        self.species    = 0
        self.speed      = 3
        self.vitality   = 0.7
        self.pos        = Vector((random.random()-0.5)*2000,(random.random()-0.5)*2000,(random.random()-0.5)*2000)
        self.zones      = [[{'min': 0, 'max': 20, 'c': 100 }, {'min': 50, 'max': 200, 'c': -1000 }],
                           [{'min': 0, 'max': 700, 'c': 5000 }],
                           [{'min': 0, 'max': 1000, 'c': -15000 }]]
        self.matingZone = 30
        self.eatingZone = 40
        self.prey       = 2
        self.nutrition  = {1: -0.1,
                           2: 0.033}
        self.hunger     = -0.000001

    def breed(self):
        return Fish()

class Shark(Agent):
    def __init__(self):
        self.species    = 1
        self.speed      = 6
        self.vitality   = 0.8
        self.pos        = Vector((random.random()-0.5)*2000,(random.random()-0.5)*2000,(random.random()-0.5)*2000)
        self.zones      = [[{'min': 0, 'max': 600, 'c': -1200 }],
                           [{'min': 0, 'max': 100, 'c': 10 }, {'min': 200, 'max': 800, 'c': -1000 }],
                           [{'min': 0, 'max': 140, 'c': 800 }]]
        self.matingZone = 40
        self.eatingZone = 20
        self.prey       = 0
        self.nutrition  = {0: 0.005,
                           2: -0.0045}
        self.hunger     = -0.0000001

    def breed(self):
        return Shark()

class Plankton(Agent):
    def __init__(self):
        self.species    = 2
        self.speed      = 0.1
        self.vitality   = 0.5
        self.pos        = Vector((random.random()-0.5)*2000,(random.random()-0.5)*2000,(random.random()-0.5)*2000)
        self.zones      = [[{'min': 0, 'max': 5, 'c': 1000 }],
                           [{'min': 0, 'max': 1000, 'c': -10000 }],
                           [{'min': 0, 'max': 380, 'c': 50000 }]]
        self.matingZone = 400
        self.eatingZone = 100
        self.prey       = 1
        self.nutrition  = {0: -0.12,
                           1: 0.33}
        self.hunger     = -0.000001

    def breed(self):
        return Plankton()

