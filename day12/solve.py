#! /usr/bin/env python3
import sys

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# ooh look, a LOGO / turtle graphics simulator
# we choose E=>positive, N=>positive, L=>positive rotation
# we start at 0,0, heading East (zero degrees)
hds=[(1,0),(0,1),(-1,0),(0,-1)]
def rotate(h,num):
    # check only multiples of 90 (right angles)
    if num%90!=0:
        print('non-right angle:',num)
        sys.exit(1)
    # how many right angles?
    num = int(num/90)%4
    # correct for negative rotation
    if num<0:
        num += 4
    # apply to index, correct for overflow
    h = (h+num)%4
    return h

x = y = 0
h = 0
for cmd in vals:
    # parse as <code><number>
    code = cmd[0:1].upper()
    num  = int(cmd[1:])
    # interpret code
    if 'N'==code:
        y += num
    elif 'S'==code:
        y -= num
    elif 'E'==code:
        x += num
    elif 'W'==code:
        x -= num
    elif 'F'==code:
        x += hds[h][0]*num
        y += hds[h][1]*num
    elif 'L'==code:
        h = rotate(h, num)
    elif 'R'==code:
        h = rotate(h, -num)
    else:
        print('invalid:',cmd)
        sys.exit(1)

# Manhattan distance please :)
print(abs(x)+abs(y))
