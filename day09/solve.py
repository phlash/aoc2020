#! /usr/bin/env python3
import sys

# load the values
vals=[]
with open('input') as f:
    vals = [int(x) for x in f.readlines()]

# starting at offset 25, check each number can be the sum
# of two previous numbers in a 25-number window beforehand
idx=25
vsum=True
while vsum:
    vsum = False
    for n1 in range(idx-25,idx):
        for n2 in range(idx-25,idx):
            if n1!=n2 and vals[n1]+vals[n2]==vals[idx]:
                # found valid sum, next!
                idx += 1
                if idx>=len(vals):
                    # oops, no more input
                    print('out of input!')
                else:
                    vsum = True
                break
        # early exit for efficiancy ;)
        if vsum:
            break

# we stop when vsum is false and idx points to failing value
print(idx, vals[idx])

# now search contiguous ranges up to idx, to find a range that
# sums to vals[idx], print first and last values & their sum
for n1 in range(0,idx):
    for n2 in range(n1+1,idx):
        s = sum(vals[n1:n2])
        if s==vals[idx]:
            # find largest/smallest values in range
            sv = vals[n1]
            lv = vals[n1]
            for v in vals[n1:n2]:
                sv = v if v<sv else sv
                lv = v if v>lv else lv
            print(n1,n2-1,sv,lv,sv+lv)
            sys.exit(0)
print('no solution :(')
