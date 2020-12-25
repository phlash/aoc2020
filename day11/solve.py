#! /usr/bin/env python3
import sys

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# let's play the game of life with seating..
def traceray(board,h,w,y,x,d,r):
    # walk array, find first non-floor, return occupancy
    y += d
    x += r
    while y>=0 and y<h and x>=0 and x<w:
        cell = board[y][x]
        if '.'==cell:
            y += d
            x += r
        elif '#'==cell:
            return 1
        else:
            break
    return 0

def traceall(board,h,w,y,x):
    o = 0
    o += traceray(board,h,w,y,x,-1,-1)          # up-left
    o += traceray(board,h,w,y,x,-1,0)           # up
    o += traceray(board,h,w,y,x,-1,1)           # up-right
    o += traceray(board,h,w,y,x,0,-1)           # left
    o += traceray(board,h,w,y,x,0,1)            # right
    o += traceray(board,h,w,y,x,1,-1)           # down-left
    o += traceray(board,h,w,y,x,1,0)            # down
    o += traceray(board,h,w,y,x,1,1)            # down-right
    return o

def adjacent(board,h,w,y,x):
    # measure occupancy of adjancent cells
    o = 0
    if y>0 and x>0 and '#'==board[y-1][x-1]:    # above-left
        o += 1
    if y>0 and '#'==board[y-1][x]:              # above
        o += 1
    if y>0 and x<w-1 and '#'==board[y-1][x+1]:  # above-right
        o += 1
    if x>0 and '#'==board[y][x-1]:              # left
        o += 1
    if x<w-1 and '#'==board[y][x+1]:            # right
        o += 1
    if y<h-1 and x>0 and '#'==board[y+1][x-1]:  # below-left
        o += 1
    if y<h-1 and '#'==board[y+1][x]:            # below
        o += 1
    if y<h-1 and x<w-1 and '#'==board[y+1][x+1]:# below-right
        o += 1
    return o

def iteration(board,trc):
    # calculate a new board state by applying
    # the simple rules:
    # empty seat with no occupied adjacents => occupy
    # occupied seat with 4+ occupied adjacents => empty
    nb = []
    h = len(board)
    for y in range(0,h):
        w = len(board[y])
        nb.append([])
        for x in range(0,w):
            cell = board[y][x]
            nb[y].append(cell)
            lim=4
            if trc:
                o = traceall(board,h,w,y,x)
                lim = 5
            else:
                o = adjacent(board,h,w,y,x)
            # apply rules
            if 'L'==cell and 0==o:
                nb[y][x] = '#'
            if '#'==cell and lim<=o:
                nb[y][x] = 'L'
    return nb

def compare(b1, b2):
    h1 = len(b1)
    h2 = len(b2)
    if h1!=h2:
        print('board height changed?')
        sys.exit(1)
    for y in range(0,h1):
        w1 = len(b1[y])
        w2 = len(b2[y])
        if w1!=w2:
            print('board width changed?')
            sys.exit(1)
        for x in range(0,w1):
            if b1[y][x]!=b2[y][x]:
                return False
    return True

# apply iterations to the loaded board until it's invariant
board=vals
nb=iteration(board,False)
cnt=0
while not compare(board,nb):
    board = nb
    nb = iteration(board,False)
    print('\r',cnt,end='')
    cnt+=1

# count occupied seats
cnt=0
for y in range(0,len(nb)):
    for x in range(0,len(nb[y])):
        if '#'==nb[y][x]:
            cnt += 1
print('\n',cnt)

# part #2 use ray tracing!
board=vals
nb=iteration(board,True)
while not compare(board,nb):
    board = nb
    nb = iteration(board,True)
    print('\r',cnt,end='')
    cnt+=1

# count occupied seats
cnt=0
for y in range(0,len(nb)):
    for x in range(0,len(nb[y])):
        if '#'==nb[y][x]:
            cnt += 1
print('\n',cnt)
