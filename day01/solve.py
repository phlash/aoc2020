#! /usr/bin/env python3

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# search for solutions, both two-valued and three-valued
for a in vals:
    x = int(a)
    for b in vals:
        y = int(b)
        # two-valued
        if x+y == 2020:
            print(x, y, x*y)
        for c in vals:
            z = int(c)
            # three-valued
            if x+y+z == 2020:
                print(x, y, z, x*y*z)
