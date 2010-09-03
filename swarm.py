#!/usr/bin/env python2.6

import sys
from math import sqrt
from species import *
from random import gauss, random

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
        g=c/pow(d, 4)
        return Vector((self.x-other.x)*g, (self.y-other.y)*g, (self.z-other.z)*g)

    def add(self,other):
        self.x+=other.x
        self.y+=other.y
        self.z+=other.z

    def __str__(self):
        return '%f %f %f' % (self.x/VIEWPORT, self.y/VIEWPORT, self.z/VIEWPORT)

class Agent:
    def __str__(self):
        return "%s %s" % (str(self.pos), self.species)

    def __init__(self,parent=None):
        self.default() # set species defaults
        if parent:
            # handle mutations
            self.speed      = parent.speed*gauss(1, 0.05)
            self.matingZone = parent.matingZone * gauss(1, 0.05)
            self.eatingZone = parent.eatingZone * gauss(1, 0.05)
            self.hunger     = parent.hunger*self.speed*gauss(1,0.05)
            self.nutrition  = dict([(key,value*gauss(1,0.05)) for (key,value) in parent.nutrition.items()])

    def move(self,swarm,world):
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
                c=(1-(d/self.eatingZone)) # how much we bite?
                self.vitality+=self.nutrition[agent.species]*c
                agent.vitality+=agent.nutrition[self.species]*c
            elif agent.species == self.species and self.vitality>=1 and d<self.matingZone:
                # try to breed
                c=(1-(d/self.matingZone)) # how much we the chance we breed?
                if(random()<c*(self.vitality**2)):
                    world.swarm[self.species].append(self.breed())
                    self.vitality=0.7
            if self.vitality>2:
                # glutony results in emptying everything
                self.vitality=0.5
            else:
                self.vitality+=self.hunger
        max_move=v.normalize(v.dist(),(0.5+self.vitality/2)*self.speed)
        if v.dist()>max_move.dist():
            self.pos.add(max_move)
        else:
            self.pos.add(v)

class World():
    def __init__(self):
        self.swarm=[[specie() for i in range(pop)] for specie, pop in Swarm]

    def __str__(self):
        return '\n'.join(map(str, self.living()))+'\ndone'

    def living(self):
        return (agent for species in self.swarm for agent in species if agent.vitality>0)

    def nextFrame(self):
        for a in self.living():
            a.move(self.living(),self)

    def run(self):
        i=0
        while True:
            print self
            if i % 50 ==0:
                counts=[len([1 for agent in species if agent.vitality > 0]) for species in self.swarm]
                sys.stderr.write("%d %s\n" % (i,counts))
                if 1 in counts:
                    sys.exit(0)
            i+=1
            self.nextFrame()

if __name__ == '__main__':
    import platform
    if platform.machine() in ['i386', 'i686']:
        import psyco
        psyco.full()

    World().run()
