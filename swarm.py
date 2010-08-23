#!/usr/bin/env python2.6

import random
from math import sqrt

# number of swarms
Fishes = 100
Sharks = 2
Planktii = 100
VIEWPORT = 100

class Vector():
    def __init__(self,x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z

    def dist(self,other=None):
        if not other:
            other=Vector()
        return sqrt(pow(self.x-other.x, 2)+pow(self.y-other.y, 2)+pow(self.z-other.z, 2))

    def normalize(self, d,c):
        if not d==0:
            self.x=(self.x*c)/d
            self.y=(self.y*c)/d
            self.z=(self.z*c)/d
        return self

    def gravity(self, other, d, c):
        g=c/pow(d, 2)
        return Vector((self.x-other.x)*g/d, (self.y-other.y)*g/d, (self.z-other.z)*g/d)

    def add(self,other):
        self.x+=other.x
        self.y+=other.y
        self.z+=other.z

    def __str__(self):
        return '%f %f %f' % (self.x/VIEWPORT, self.y/VIEWPORT, self.z/VIEWPORT)

class Agent:
    def __str__(self):
        #return "%s" % (self.vitality)
        if self.vitality>0:
            return "%s %s" % (str(self.pos), self.race)
        else:
            return ''

    def move(self,swarm):
        v=Vector()
        p=self.pos
        for agent in swarm:
            d=self.pos.dist(agent.pos)
            for zone in self.zones[agent.race]:
                if zone['min'] < d <= zone['max']:
                    v.add(p.gravity(agent.pos,d,zone['c']))
            # handle health
            if agent.race != self.race:
                if d<5:
                    # do damage/nutrition
                    self.vitality+=self.nutrition[agent.race]
            elif d<self.matingZone and self.vitality>1:
                # give birth
                Nursery.append(self.birth())
                self.vitality=0.7
        self.pos.add(v.normalize(v.dist(),self.vitality*self.speed))

class Fish(Agent):
    def __init__(self):
        self.pos        = Vector((random.random()-0.5)*1000,(random.random()-0.5)*1000,(random.random()-0.5)*1000)
        self.zones      = [[{'min': 0, 'max': 20, 'c': 100 }, {'min': 50, 'max': 300, 'c': -1000 }],
                           [{'min': 0, 'max': 700, 'c': 1000 }],
                           [{'min': 0, 'max': 1000, 'c': -1000 }]]
        self.matingZone = 30
        self.speed      = 1
        self.race       = 0
        self.vitality   = 0.999999999999
        self.nutrition  = {1: -0.7,
                           2: 0.4}

    def birth(self):
        return Fish()

class Shark(Agent):
    def __init__(self):
        self.pos        = Vector((random.random()-0.5)*1000,(random.random()-0.5)*1000,(random.random()-0.5)*1000)
        self.zones      = [[{'min': 0, 'max': 600, 'c': -1200 }],
                           [{'min': 0, 'max': 100, 'c': 10 }, {'min': 200, 'max': 800, 'c': -1000 }],
                           [{'min': 0, 'max': 20, 'c': 1 }]]
        self.matingZone = 0.0000001
        self.speed      = 2
        self.race       = 1
        self.vitality   = 0.8
        self.nutrition  = {0: 0.1,
                           2: -0.3}
    def birth(self):
        return Shark()

class Plankton(Agent):
    def __init__(self):
        self.pos        = Vector((random.random()-0.5)*1000,(random.random()-0.5)*1000,(random.random()-0.5)*1000)
        self.zones      = [[{'min': 0, 'max': 5, 'c': 10 }],
                           [{'min': 0, 'max': 1000, 'c': -1000 }],
                           []]
        self.matingZone = 1000000000000000
        self.speed      = 0.1
        self.race       = 2
        self.vitality   = 1
        self.nutrition  = {0: -1, 1: 0.8}

    def birth(self):
        return Plankton()

Nursery=[]

if __name__ == '__main__':
    import platform
    if platform.machine() in ['i386', 'i686']:
        import psyco
        psyco.full()
    swarm = [Fish() for x in range(Fishes)]+[Shark() for x in range(Sharks)]+[Plankton() for x in range(Planktii)]
    print '\n'.join(map(str, swarm))+'\ndone'
    while True:
        for a in swarm: a.move(swarm)
        # handle life and death
        swarm=filter(lambda x: x.vitality>0,swarm)
        swarm+=Nursery
        Nursery=[]
        print '\n'.join(map(str, swarm))+'\ndone'
