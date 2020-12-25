#! /usr/bin/env python3
import re

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# the required set of passport fields & value regex or ranges
reqs={
    'byr': range(1920,2003),
    'iyr': range(2010,2021),
    'eyr': range(2020,2031),
    'hgt': r'(\d+)(cm|in)',  # also needs range checking - see below
    'hcl': r'#[0-9a-f]{6}',
    'ecl': r'amb|blu|brn|gry|grn|hzl|oth',
    'pid': r'\d{9}'
}
hgts={
    'cm': range(150,194),
    'in': range(59,77)
}
def check(flds):
    p1val=True
    p2val=True
    inf='chk('
    for r in reqs:
        if r in flds:
            v = flds[r]
            t = reqs[r]
            # are we checking regex or range?
            if isinstance(t, str):
                m = re.fullmatch(t, v)
                if not m:
                    p2val=False
                    inf+=r+'/M'
                elif r=='hgt':
                    # special range check
                    try:
                        v=int(m[1])
                        h=hgts[m[2]]
                        if v not in h:
                            p2val=False
                            inf+=r+'/'+str(v)+'/H'
                    except:
                        p2val=False
                        inf+=r+'/'+str(m.groups())+'/n'
            else:
                try:
                    v=int(v)
                    if v not in t:
                        p2val=False
                        inf+=r+'/'+str(v)+'/R'
                except:
                    p2val=False
                    inf+=r+'/'+str(v)+'/N'
        else:
            p1val=False
            p2val=False
            inf+=r+'/-'
    inf = inf+')'
    #print(inf, flds, valid)
    return (p1val,p2val)

# parse passport entries (separated by blank lines)
# check fields (see above)
cnt1=0
cnt2=0
flds={}
for line in vals:
    line = line.strip()
    if len(line)==0:
        # end of record, check fields
        (p1,p2) = check(flds)
        if p1:
            cnt1 = cnt1+1
        if p2:
            cnt2 = cnt2+1
        # clear fields for next record
        flds={}
        continue
    # split into fields & key/val pairs and store
    for f in line.split(' '):
        kv = f.split(':', 2)
        if len(kv)<2:
            print('erk: ',line,kv)
        flds[kv[0]]=kv[1]
# check last fieldset
(p1,p2) = check(flds)
if p1:
    cnt1 = cnt1+1
if p2:
    cnt2 = cnt2+1
print(cnt1, cnt2)
