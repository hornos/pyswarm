#!/usr/bin/env python2.6

import sys
from math import sqrt
from species import *

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
        return "%s %s" % (str(self.pos), self.species)

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
                self.vitality+=self.nutrition[agent.species]
                agent.vitality+=agent.nutrition[self.species]
            elif agent.species == self.species and self.vitality>=1 and d<self.matingZone:
                # breed
                world.swarm[self.species].append(self.breed())
                self.vitality=0.7
            if self.vitality>2:
                # glutony results in emptying everything
                self.vitality=0.5
            else:
                self.vitality+=self.hunger
        self.pos.add(v.normalize(v.dist(),self.vitality*self.speed))

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
