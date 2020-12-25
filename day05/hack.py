with open('input') as f:
 v = f.readlines()
h=0
m={}
for l in v:
 l=l.translate(str.maketrans("FBRL","0110"))
 r=int(l[:7],2)
 c=int(l[7:-1],2)
 s=r*8+c
 if s>h:
     h=s
 m[s]=1
print(h)
for i in range(1,h):
 if i not in m:
  if (i-1) in m and (i+1) in m:
   print(i)
   break
