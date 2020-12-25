#! /usr/bin/env python3
import sys

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# the sea monster..
mnst={
    0:'                  # ',
    1:'#    ##    ##    ###',
    2:' #  #  #  #  #  #   '
}

# A tile re-assembly challenge, done by lining
# up the edges of all tiles, in any orientation
# and direction.. however for part1 we only
# actually need to know the corners, which are
# identified by having an edge pattern on two
# sides that does not align with any other tile =)
tiles={}
tile=None
tsiz=0
for v in vals:
    v = v.strip()
    o = v.find(':')
    if o>0:
        # tile name
        tile = v[:o].split()[1]
        tiles[tile]={}
        tiles[tile]['data']=[]
    elif len(v)>0:
        # tile row
        tiles[tile]['data'].append(v)
        tsiz=len(v)

# parse each tile and build a list of edges
# (top,bottom,left,right)
edges={}
for tile in tiles:
    edges[tile]=[]
    left=''
    right=''
    rnum=0
    for row in tiles[tile]['data']:
        if 0==rnum:              # top
            edges[tile].append(row)
        if len(row)-1==rnum:     # bottom
            edges[tile].append(row)
        left += row[0]
        right+= row[-1]
        rnum += 1
    edges[tile].append(left)
    edges[tile].append(right)

for tile in edges:
    print(tile,edges[tile])
print(len(edges))

# convolve edges with itself, count unmatched edges
# per tile.. remember edges can go both ways (flipped)
# enrich tile storage with adjacent tile information
mul = 1
cnr = []
for tile in edges:
    cnt = 0
    tiles[tile]['joins']={}
    enum = 0
    for edge in edges[tile]:
        fnd = False
        for scan in edges:
            if scan==tile:
                continue        # do not scan ourselves
            for sege in edges[scan]:
                if edge==sege:
                    #print('found',tile,edge,scan,sege)
                    fnd = True
                    break
                rev = sege[::-1]
                if edge==rev:
                    #print('found(rev)',tile,edge,scan,rev)
                    fnd = True
                    break
            if fnd:
                tiles[tile]['joins'][enum] = scan
                break
        if not fnd:
            cnt += 1
        enum += 1
    if cnt>1:
        cnr.append(tile)
        mul *= int(tile)
for tile in tiles:
    print(tile,tiles[tile]['joins'])
print('part1, corners and multiplicand',cnr,mul)

# part2: assemble the image from the tiles, now that we have
# lists of tile joins.. we start with the first corner as
# 'top left', then work across to top right following the
# joins, then down a row and repeat...
# pruning the boundaries as we assemble...
image={}

def insert(image,tile,x,y):
    # trim off boundary of tile while copying
    for dy in range(1,tsiz-1):
        for dx in range(1,tsiz-1):
            if y+dy not in image:
                image[y+dy]={}
            # should be empty cell..
            if x+dx in image[y+dy]:
                print('cell collision',y+dy,x+dx)
                sys.exit(1)
            image[y+dy][x+dx] = tile['data'][dy][dx]

def rotate90(tile):
    # rotate tile cells, including boundary +90 (ccw)
    ndata=[]
    for x in range(tsiz-1,-1,-1):
        nrow=''
        for y in range(0,tsiz):
            nrow+=tile['data'][y][x]
        ndata.append(nrow)
    njoins={}
    # rotate joins if any
    if 0 in tile['joins']:
        njoins[2] = tile['joins'][0]
    if 1 in tile['joins']:
        njoins[3] = tile['joins'][1]
    if 2 in tile['joins']:
        njoins[1] = tile['joins'][2]
    if 3 in tile['joins']:
        njoins[0] = tile['joins'][3]
    return {'data':ndata, 'joins':njoins}

def flip(tile,vert):
    # flip vertically (top/bottom) or horizontally
    ndata=[]
    njoins={}
    if vert:
        for y in range(tsiz-1,-1,-1):
            ndata.append(tile['data'][y])
        if 0 in tile['joins']:
            njoins[1] = tile['joins'][0]
        if 1 in tile['joins']:
            njoins[0] = tile['joins'][1]
        if 2 in tile['joins']:
            njoins[2] = tile['joins'][2]
        if 3 in tile['joins']:
            njoins[3] = tile['joins'][3]
    else:
        for r in tile['data']:
            ndata.append(r[::-1])
        if 0 in tile['joins']:
            njoins[0] = tile['joins'][0]
        if 1 in tile['joins']:
            njoins[1] = tile['joins'][1]
        if 2 in tile['joins']:
            njoins[3] = tile['joins'][2]
        if 3 in tile['joins']:
            njoins[2] = tile['joins'][3]
    return {'data':ndata, 'joins':njoins}

def ptile(lab,tile):
    print(lab)
    if 0 in tile['joins']:
        print('  ',tile['joins'][0])
    else:
        print('   -')
    if 2 in tile['joins']:
        print(tile['joins'][2],'<',end='')
    else:
        print(' - <',end='')
    if 3 in tile['joins']:
        print('>',tile['joins'][3],end='')
    else:
        print('> -',end='')
    print()
    if 1 in tile['joins']:
        print('  ',tile['joins'][1])
    else:
        print('   -')
    for r in tile['data']:
        print(r)

def orient(tile,edge,vert):
    # check top or left edge of the tile (vert=top)
    # flip and check again, then rotate and repeat
    chk = tile
    while True:
        if vert:
            ed=chk['data'][0]
        else:
            ed=''.join([r[0] for r in chk['data']])
        if ed==edge:
            return chk
        flp = flip(chk,not vert)
        if vert:
            ed=flp['data'][0]
        else:
            ed=''.join([r[0] for r in flp['data']])
        if ed==edge:
            return flp
        chk = rotate90(chk)

# starting tile - first corner, flip to ensure matched
# edges are right/down
fst = cnr[0]
til = tiles[fst]
if 0 in til['joins']:       # joined at the top, flip
    til = flip(til,True)
if 2 in til['joins']:       # joined to the left, flip
    til = flip(til,False)

# special starting value to ensure no re-orienting on loop entry below
be = til['data'][0]

# iterate top-bottom, left-right orienting and inserting tiles to image
ypos= -1
while fst:
    til = orient(tiles[fst],be,True)
    xpos = -1
    insert(image,til,xpos,ypos)
    xpos += tsiz-2
    print(fst,end=':')
    re = ''.join([r[-1] for r in til['data']])
    be = til['data'][-1]
    nxt = (til['joins'][3] if 3 in til['joins'] else None)
    # next row start.. do this now before til gets reused
    fst = (til['joins'][1] if 1 in til['joins'] else None)
    while nxt:
        til = orient(tiles[nxt],re,False)
        insert(image,til,xpos,ypos)
        print(nxt,end=',')
        xpos += tsiz-2
        re = ''.join([r[-1] for r in til['data']])
        nxt = (til['joins'][3] if 3 in til['joins'] else None)
    print()
    ypos += tsiz-2

# we have an assembled image (phew!), dump it (and count hashes)
ypos = 0
nhsh = 0
while ypos in image:
    xpos = 0
    while xpos in image[ypos]:
        print(image[ypos][xpos],end='')
        if '#'==image[ypos][xpos]:
            nhsh += 1
        xpos += 1
    print()
    ypos += 1
print(ypos,nhsh)

# sea monster hunt!
def ismonster(img,mnst,x,y):
    # match each '#' in the monster to the image
    for dy in mnst:
        for dx in range(0,len(mnst[dy])):
            if '#'==mnst[dy][dx] and '#'!=img[y+dy][x+dx]:
                return False
    return True

def flipimg(img):
    nimg={}
    for y in range(0,len(img)):
        nimg[y]={}
        for x in range(0,len(img[y])):
            nimg[y][x] = img[y][len(img[y])-x-1]
    return nimg

def rotimg(img):
    nimg={}
    for y in range(0,len(img)):
        nimg[y]={}
        for x in range(0,len(img[y])):
            nimg[y][x] = img[x][len(img)-y-1]
    return nimg

# convolve the monster across the image, then flip and
# try again, then rotate and repeat, until we find them
img = image
for i in range(0,4):
    for y in range(0,len(img)-3):
        for x in range(0,len(img[y])-20):
            if ismonster(img,mnst,x,y):
                print(i,'monster!',x,y)
                nhsh -= 15
    flp = flipimg(img)
    for y in range(0,len(flp)-3):
        for x in range(0,len(flp[y])-20):
            if ismonster(flp,mnst,x,y):
                print(i,'flp monster!',x,y)
                nhsh -= 15
    img = rotimg(img)

print(nhsh)
