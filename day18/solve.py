#! /usr/bin/env python3
import sys

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# Expression parsing & evaluation, with modified operator
# precedence, yay (so we cannot just eval in python!)
# our given precedence is strict left-to-right unless there
# are parentheses, in which case we eval within those as
# a unit - this allows a recursive strategy to work..
def part1(res,rem):
    # parse expression remainder..
    tst = rem.strip()
    #print(tst,end=': ')
    # termination condition, close paren or end of line
    val=None
    opr=None
    while (len(tst) and tst[0]!=')'):
        if tst[0]=='(':
            # sub-expression, recurse!
            #print('(',end='')
            evl = part1(None,tst[1:])
            val = evl[0]
            tst = evl[1][1:]
            #print(')=',val,'[',tst,']',end='')
        elif tst[0].isdecimal():
            # number, parse
            end = 0
            while end<len(tst) and tst[end].isdecimal():
                end += 1
            val = int(tst[:end])
            tst = tst[end:]
        elif tst[0]!=' ':
            # operator, parse
            opr = tst[0]
            tst = tst[1:]
        else:
            # whitespace, go around..
            tst = tst[1:]
            continue
        # if we have a result , value and operator, apply them
        if res!=None and val!=None and opr!=None:
            if '+'==opr:
                res = res + val
            elif '*'==opr:
                res = res * val
            else:
                print('invalid opr:',opr)
                sys.exit(1)
            # reset state..
            val = None
            opr = None
        # otherwise, if we have no result and a value assign it
        elif res==None and val!=None:
            res = val
            val = None
    return (res, tst)

# part2 - now addition takes precedence over multiplication, so
# we use a different strategy - bracketing additions with extra
# parenthesis, then using eval() in python to do the hard work..
def part2(rem):
    # find every '+', then find left and right values, which may
    # include multiple parenthesised terms, so we count open/close
    # until we reach zero
    tst = rem.strip()
    off = tst.find('+')
    while off>0:
        # left search for numeral or close paren
        left = off
        pcnt = 0
        done = False
        while left>=0 and not done:
            left -= 1
            if not pcnt and tst[left].isdecimal():
                while left>=0 and tst[left].isdecimal():
                    left -= 1
                left += 1
                done = True
            elif tst[left]==')':
                pcnt += 1
            elif tst[left]=='(':
                pcnt -= 1
                if not pcnt:
                    done = True
        tst = tst[:left]+'('+tst[left:]
        rght = off
        pcnt = 0
        done = False
        while rght<len(tst) and not done:
            rght += 1
            if not pcnt and tst[rght].isdecimal():
                while rght<len(tst) and tst[rght].isdecimal():
                    rght += 1
                rght -= 1
                done = True
            elif tst[rght]=='(':
                pcnt += 1
            elif tst[rght]==')':
                pcnt -= 1
                if not pcnt:
                    done = True
        tst = tst[:rght+1]+')'+tst[rght+1:]
        off = tst.find('+',off+2)
    rv = eval(tst)
    print(rem.strip(),'=>',tst,'===',rv)
    return rv

# work through those expressions, sum all the answers
tot = 0
for v in vals:
    res = part1(None,v)
    tot += res[0]
    print(v.strip(),'=>',res[0])
print(tot)
tot = 0
for v in vals:
    res = part2(v)
    tot += res
print(tot)
