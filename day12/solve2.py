#! /usr/bin/env python3
import sys

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# ooh look, a LOGO / turtle graphics simulator
# we choose E=>positive, N=>positive, L=>positive rotation
# we start at 0,0, heading East (zero degrees)

# rotation matricies for 0, 90, 180, 270
# in the form (cos(t), sin(t)), used to rotate input vector
rots = [(1,0), (0,1), (-1,0), (0,-1)]
def rotate(vec,num):
    # check only multiples of 90 (right angles)
    if num%90!=0:
        print('non-right angle:',num)
        sys.exit(1)
    # how many right angles?
    num = int(num/90)%4
    # correct for negative rotation
    if num<0:
        num += 4
    # apply to input vector (matrix multiplication - yay!)
    # https://en.wikipedia.org/wiki/Rotation_matrix
    # (x',y') = (x.cos(t)-y.sin(t), x.sin(t)+y.cos(t))
    x = vec[0]*rots[num][0]-vec[1]*rots[num][1]
    y = vec[0]*rots[num][1]+vec[1]*rots[num][0]
    return (int(x),int(y))

# ship absolute position
x = y = 0
# waypoint relative vector from ship
wx = 10
wy = 1
for cmd in vals:
    # debug time!
    # parse as <code><number>
    code = cmd[0:1].upper()
    num  = int(cmd[1:])
    # interpret code
    if 'N'==code:
        wy += num
    elif 'S'==code:
        wy -= num
    elif 'E'==code:
        wx += num
    elif 'W'==code:
        wx -= num
    elif 'F'==code:
        x += wx*num
        y += wy*num
    elif 'L'==code:
        r = rotate((wx,wy), num)
        wx = r[0]
        wy = r[1]
    elif 'R'==code:
        r = rotate((wx,wy), -num)
        wx = r[0]
        wy = r[1]
    else:
        print('invalid:',cmd)
        sys.exit(1)

# Manhattan distance please :)
print(abs(x)+abs(y))
