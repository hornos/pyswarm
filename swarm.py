#!/usr/bin/env python2.6

import random, sys
from math import sqrt

# number of swarms
Fishes = 50
Sharks = 4
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
        #return "%s %s" % (self.species, self.vitality)
        if self.vitality>0:
            return "%s %s" % (str(self.pos), self.species)
        else:
            return ''

    def move(self,swarm):
        if self.vitality<=0: return
        v=Vector()
        p=self.pos
        for agent in swarm:
            d=self.pos.dist(agent.pos)
            # calculate vector of next move
            for zone in self.zones[agent.species]:
                if zone['min']/self.vitality < d <= zone['max']/self.vitality:
                    v.add(p.gravity(agent.pos,d,zone['c']))
            # handle health
            if agent.species == self.prey and d<self.eatingZone and agent.vitality>0:
                # do damage/nutrition
                self.vitality+=self.nutrition[agent.species]
                agent.vitality+=agent.nutrition[self.species]
            elif agent.species == self.species and self.vitality>=1 and d<self.matingZone:
                # give birth
                Nursery.append(self.birth())
                self.vitality=0.7
            if self.vitality>2:
                # glutony results in emptying everything
                self.vitality=0.5
            else:
                self.vitality+=self.hunger
        self.pos.add(v.normalize(v.dist(),self.vitality*self.speed))

class Fish(Agent):
    def __init__(self):
        self.species    = 0
        self.speed      = 3
        self.vitality   = 0.7
        self.pos        = Vector((random.random()-0.5)*1000,(random.random()-0.5)*1000,(random.random()-0.5)*1000)
        self.zones      = [[{'min': 0, 'max': 20, 'c': 100 }, {'min': 50, 'max': 200, 'c': -1000 }],
                           [{'min': 0, 'max': 700, 'c': 5000 }],
                           [{'min': 0, 'max': 1000, 'c': -15000 }]]
        self.matingZone = 30
        self.eatingZone = 40
        self.prey       = 2
        self.nutrition  = {1: -0.7,
                           2: 0.10}
        self.hunger     = -0.000001

    def birth(self):
        return Fish()

class Shark(Agent):
    def __init__(self):
        self.species    = 1
        self.speed      = 6
        self.vitality   = 0.8
        self.pos        = Vector((random.random()-0.5)*1000,(random.random()-0.5)*1000,(random.random()-0.5)*1000)
        self.zones      = [[{'min': 0, 'max': 600, 'c': -1200 }],
                           [{'min': 0, 'max': 100, 'c': 10 }, {'min': 200, 'max': 800, 'c': -1000 }],
                           [{'min': 0, 'max': 140, 'c': 800 }]]
        self.matingZone = 40
        self.eatingZone = 20
        self.prey       = 0
        self.nutrition  = {0: 0.08,
                           2: -0.008}
        self.hunger     = -0.000001

    def birth(self):
        return Shark()

class Plankton(Agent):
    def __init__(self):
        self.species    = 2
        self.speed      = 0.1
        self.vitality   = 0.5
        self.pos        = Vector((random.random()-0.5)*1000,(random.random()-0.5)*1000,(random.random()-0.5)*1000)
        self.zones      = [[{'min': 0, 'max': 5, 'c': 10 }],
                           [{'min': 0, 'max': 1000, 'c': -1000 }],
                           []]
        self.matingZone = 700
        self.eatingZone = 100
        self.prey       = 1
        self.nutrition  = {0: -0.2, 1: 0.12}
        self.hunger     = -0.000001

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
    i=0
    while True:
        for a in swarm: a.move(swarm)
        # handle life and death
        swarm=filter(lambda x: x.vitality>0,swarm)
        swarm+=Nursery
        Nursery=[]
        print '\n'.join(map(str, swarm))+'\ndone'
        if i % 50 ==0:
            counts=[0,0,0]
            for agent in swarm:
                counts[agent.species]+=1
            sys.stderr.write("%d %s\n" % (i,counts))
            if counts == [0,0,0]:
                sys.exit(0)
        i+=1
