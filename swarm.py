#!/usr/bin/env python2.6

import random
from math import sqrt

# number of swarms
SN = 200
REPEL_FORCE = 10
ATTRACT_FORCE = -1000
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

    def normalize(self, d):
        if not d==0:
            self.x/=d
            self.y/=d
            self.z/=d
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
    def __init__(self, avoid=(0, 20), attract=(50,300)):
        self.pos        = Vector((random.random()-0.5)*800,(random.random()-0.5)*800,(random.random()-0.5)*800)
        self.avoid      = avoid
        self.attract    = attract

    def __str__(self):
        return str(self.pos)

    def move(self,swarm):
        v=Vector()
        p=self.pos
        for agent in swarm:
            d=self.pos.dist(agent.pos)
            if self.avoid[0] < d <=self.avoid[1]:
                v.add(p.gravity(agent.pos,d,REPEL_FORCE))
            elif self.attract[0] < d <=self.attract[1]:
                v.add(p.gravity(agent.pos,d,ATTRACT_FORCE))
        self.pos.add(v.normalize(v.dist()))

def nextframe(swarm):
    return [a.move(swarm) for a in swarm]

if __name__ == '__main__':
    import platform
    if platform.machine() in ['i386', 'i686']:
        import psyco
        psyco.full()
    swarm = [Agent() for x in range(SN)]
    print '\n'.join(map(str, swarm))+'\ndone'
    while True:
        nextframe(swarm)
        print '\n'.join(map(str, swarm))+'\ndone'
