#! /usr/bin/env python3
import sys

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# sort input into players hands of cards
hands={}
pids=[]
for v in vals:
    v = v.strip()
    if len(v)<1:
        continue
    elif v.startswith('Player '):
        pids.append(int(v.split()[1][:-1]))
        hands[pids[-1]]=[]
    else:
        hands[pids[-1]].append(int(v))

# let's play [Recursive] Combat (tm)!
def copyhands(hands):
    cpy={}
    for pid in hands:
        cpy[pid]=[]
        cpy[pid]=hands[pid].copy()
    return cpy

def checkhands(prev,hands):
    for (idx,hand) in enumerate(prev):
        diff = False
        for pid in hand:
            h1 = hand[pid]
            h2 = hands[pid]
            if len(h1)!=len(h2):
                diff = True
            for (v1,v2) in zip(h1,h2):
                if v1!=v2:
                    diff = True
        if not diff:
            return (idx,hand)
    return (-1,None)

tot = 0
mem = 0
oldhnds=[]
oldwins=[]
def combat(rec,pids,hands):
    #print(rec,':',hands)
    global tot, mem
    win = -1
    rnd = 0
    # detect round loop by retaining previous hands
    prev=[]
    while True:
        # 'before any card is dealt, check for matching previous round.
        # If found, immediately award the game to player 1'
        (idx,mtch) = checkhands(prev,hands)
        if mtch:
            #print(rec,'! win/rnd=',pids[0],'/',rnd,mtch,'=',hands)
            return pids[0]
        prev.append(copyhands(hands))
        rnd += 1
        # draw a card from each player (in order)
        played = [hands[pid].pop(0) for pid in pids]
        # check for recursion (if playing Recursive Combat)
        # both players have as many card in hand as the value
        # of the card just drawn
        dorec = True
        idx = -1
        for i in range(0,len(played)):
            if played[i]>len(hands[pids[i]]):
                dorec = False
        if rec!=None and dorec:
            # copy (value of card just drawn) cards into new hand, recurse game
            subhnds={}
            for i in range(0,len(played)):
                subhnds[pids[i]]=((hands[pids[i]])[:played[i]]).copy()
            # memoization check, have we played this hand before?
            (idx,mtch) = checkhands(oldhnds,subhnds)
            if mtch:
                subwin = oldwins[idx]
                mem += 1
            else:
                temp = copyhands(subhnds)
                subwin = combat(rec+[rnd],pids,subhnds)
                oldhnds.append(temp)
                oldwins.append(subwin)
            for i in range(0,len(played)):
                if pids[i]==subwin:
                    idx = i
        else:
            # find highest card (equal should be impossible!)
            high = -1
            for i in range(0,len(played)):
                if played[i]>high:
                    high = played[i]
                    idx = i
        # winner picks up all cards, theirs first
        hands[pids[idx]].append(played.pop(idx))
        hands[pids[idx]].extend(played)
        # stop if any player has all the cards
        cnt = 0
        for pid in hands:
            if len(hands[pid])>0:
                cnt += 1
                win = pid
        if 1==cnt:
            break
        tot += 1
        if (tot%1000)==0:
            print('\rtotal:',tot,'mem:',mem)
    #print(rec,':','win/rnd=',win,'/',rnd)
    return win

# Part1: play a non-recursive game
part1 = copyhands(hands)
win = combat(None,pids,part1)

# print the winning hand and sum score
print('Part1:',win,'=',part1[win])
score = 0
mul = 1
while len(part1[win])>0:
    score += mul*part1[win].pop()
    mul += 1
print(score)

# Part2: play recursive games..
part2 = copyhands(hands)
win = combat([],pids,part2)
print('Part2:',win,'=',part2[win])
score = 0
mul = 1
while len(part2[win])>0:
    score += mul*part2[win].pop()
    mul += 1
print(score)
