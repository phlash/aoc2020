#! /usr/bin/env python3
import sys, os

# debug
verb = (True if os.getenv("SOLVE_DBG") else False)
def dbg(*args,**kwargs):
    global verb
    if verb:
        print(*args,**kwargs)

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# let's play the game of life in 4D with Conway Cubes!
def put(spc,x,y,z,w,v):
    # insert a cube into the 4D space (see below for structure!)
    if w not in spc:
        spc[w]={}
    if z not in spc[w]:
        spc[w][z]={}
    if y not in spc[w][z]:
        spc[w][z][y]={}
    if x not in spc[w][z][y]:
        spc[w][z][y][x]={}
    spc[w][z][y][x]=v

def get(spc,x,y,z,w):
    # find a cube in the 4D space, no such space == inactive (False)
    if w in spc:
        if z in spc[w]:
            if y in spc[w][z]:
                if x in spc[w][z][y]:
                    return spc[w][z][y][x]
    return False

def count(spc,x,y,z,w):
    n = 0
    dbg('(',end='')
    for dw in range(-1,2):
        for dz in range(-1,2):
            for dy in range(-1,2):
                for dx in range(-1,2):
                    if dx==0 and dy==0 and dz==0 and dw==0:
                        continue
                    n += (1 if get(spc,x+dx,y+dy,z+dz,w+dw) else 0)
                    dbg(dx,dy,dz,dw,end='/')
    dbg(')=',end='')
    return n

# rules:
# 1. active cube, remain so if neighbours in (2,3) otherwise inactive
# 2. inactive cube, activates if neighbours == 3, otherwise remain
def rules(b,n):
    r = b
    if b and (n<2 or n>3):
        r = False
    if not b and n==3:
        r = True
    dbg(n,b,'-',r,']',end=',')
    return r

# operate one game cycle, generating a new output space
def cycle(spc):
    nsp = {}
    # walk existing space, expanded by one in each dimension,
    # calculate new space
    lw = min(spc)
    mw = max(spc)
    lz = min(spc[0])
    mz = max(spc[0])
    ly = min(spc[0][0])
    my = max(spc[0][0])
    lx = min(spc[0][0][0])
    mx = max(spc[0][0][0])
    for w in range(lw-1,mw+2):
        for z in range(lz-1,mz+2):
            for y in range(ly-1,my+2):
                for x in range(lx-1,mx+2):
                    dbg('[',x,y,z,w,'=>',end='')
                    # count neighbours
                    n = count(spc,x,y,z,w)
                    # apply rules
                    put(nsp,x,y,z,w,rules(get(spc,x,y,z,w),n))
                    dbg()
    return nsp

def debug(spc):
    global verb
    act = 0
    ov = verb
    verb = True
    for w in sorted(spc):
        for z in sorted(spc[w]):
            dbg('\nz=',z,'w=',w)
            for y in sorted(spc[w][z]):
                for x in sorted(spc[w][z][y]):
                    act += (1 if spc[w][z][y][x] else 0)
                    dbg(('#' if spc[w][z][y][x] else '.'),end='')
                dbg()
    verb = ov
    return act

# initial 4D space, a map of outer co-ordinate space (w), with
# nested maps for each axes (z,y,x) finally holding cube activation
# state (True/False)
spc = {}
y = 0
for v in vals:
    # we treat lines as y-coord, columns as x-coord
    for x in range(0,len(v)):
        put(spc,x,y,0,0,'#'==v[x:x+1])
    y += 1

# operate 6 cycles of the game..
debug(spc)
for c in range(0,6):
    spc = cycle(spc)
    #debug(spc)

# count all the active cubes
print(debug(spc))
