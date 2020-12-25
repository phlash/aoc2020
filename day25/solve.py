#! /usr/bin/env python3
import sys

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# cracking DH public-key encryption (ish)
def transform(sub,val):
    return (val*sub)%20201227

def findloop(sub,pub):
    # apply the algorithm as described
    loop=1
    res=sub
    while res!=pub:
        res = transform(sub,res)
        loop += 1
    return loop

# test values
cpub = 5764801
dpub = 17807724
# real values
cpub = int(vals[0])
dpub = int(vals[1])
card = findloop(7,cpub)
door = findloop(7,dpub)
print('card',card,'door',door)
key = cpub
for i in range(1,door):
    key = transform(cpub,key)
    print(i,'ckey',key)
key = dpub
for i in range(1,card):
    key = transform(dpub,key)
    print(i,'dkey',key)
