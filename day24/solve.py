#! /usr/bin/env python3
import sys

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# navigating a hexagonally tiled floor!
# we keep the floor in a 2D map, using 2x scaled
# co-ordinates for the x-axis with x-axis rows
# alternating between odd/even (we can use the
# y-axis oddness to discover which)
# Here's our reference tile in the middle...
floor={
    0: { 0: 0 }
}

# parse a line of tile steps, build out the
# floor as we walk it, placing white (0) tiles
# if none present, otherwise no change. Once
# full path walked, we flip last tile
def placetile(floor,path):
    # path steps are a series of:
    # e - east, w - west
    # ne - northeast, nw - northwest
    # se - southeast, sw - southwest
    # from the same reference tile (0,0)
    x = y = 0
    while len(path)>0:
        if path[0]=='e':
            x += 2
            path=path[1:]
        elif path[0]=='w':
            x -= 2
            path=path[1:]
        elif path[0:2]=='ne':
            x += 1
            y += 1
            path=path[2:]
        elif path[0:2]=='nw':
            x -= 1
            y += 1
            path=path[2:]
        elif path[0:2]=='se':
            x += 1
            y -= 1
            path=path[2:]
        elif path[0:2]=='sw':
            x -= 1
            y -= 1
            path=path[2:]
        else:
            print('invalid path:',path)
            sys.exit(1)
        #print(x,y,end='/')
        if y not in floor:
            floor[y]={}
        if x not in floor[y]:
            floor[y][x]=0
            #print('[P],',end='')
    v = floor[y][x]
    #print(v,'=>',(v+1))
    floor[y][x]=(v+1)
    return (x,y)

# place those tiles... measure extent of floor
minx=maxx=0
miny=maxy=0
for v in vals:
    v = v.strip()
    (x,y)=placetile(floor,v)
    minx=(x if x<minx else minx)
    maxx=(x if x>maxx else maxx)
    miny=(y if y<miny else miny)
    maxy=(y if y>maxy else maxy)
# ensure x range values are even
minx=(minx-1 if minx%2==1 else minx)
maxx=(maxx+1 if maxx%2==1 else maxx)
print(minx,miny,'=>',maxx,maxy)

# now we play the game of life (again!) in hex =)
def adjacency(x,y,floor):
    # count black (odd value) tiles surrounding x,y
    cnt = 0
    for (dy,dx) in [(0,-2),(0,2),(1,-1),(1,1),(-1,-1),(-1,1)]:
        if (y+dy) in floor:
            if (x+dx) in floor[(y+dy)]:
                if (floor[y+dy][x+dx]%2)==1:
                    cnt += 1
    return cnt

def lifecycle(floor):
    global minx,miny,maxx,maxy
    nfl={}
    miny-=1
    maxy+=1
    minx-=2
    maxx+=2
    for y in range(miny,maxy+1):
        nfl[y]={}
        xoff=(0 if (y%2)==0 else 1)
        for x in range(xoff+minx,xoff+maxx+1,2):
            cnt = adjacency(x,y,floor)
            # copy existing tile (if any)
            if y in floor and x in floor[y]:
                nfl[y][x]=floor[y][x]
            else:
                nfl[y][x]=0
            # the rules:
            # current tile black..
            if (nfl[y][x]%2)==1:
                # zero or more than two adjacent black, flip
                if cnt==0 or cnt>2:
                    nfl[y][x] += 1
            # otherwise white
            else:
                # exactly two adjacent black, flip
                if cnt==2:
                    nfl[y][x] += 1
    return nfl

# count black (odd flip count) tiles
def count(floor):
    cnt = 0
    for y in floor:
        for x in floor[y]:
            if (floor[y][x]%2)==1:
                cnt += 1
    return cnt

print('Day 0 :',count(floor))
for d in range(1,101):
    floor = lifecycle(floor)
    print('Day',d,':',count(floor))
