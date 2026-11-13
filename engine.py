#!/usr/bin/env python3
# Tiny chess engine under 4KB
import sys
P,N,B,R,Q,K=1,2,3,4,5,6
V=[0,100,320,330,500,900,20000]
def board():
 p=[0]*64
 p[0:8]=[R,N,B,Q,K,B,N,R];p[8:16]=[P]*8
 p[48:56]=[-P]*8;p[56:64]=[-R,-N,-B,-Q,-K,-B,-N,-R]
 return p
def show(p):
 s=""
 for i in range(64):
  if i%8==0:s+="\n"
  v=p[i]
  s+=".PNBRQKpnbrqk"[v] if v else "."
 print(s)
def move(p,f,t):
 n=p[:]
 n[t]=n[f];n[f]=0
 return n
def score(p):
 s=0
 for x in p:
  s+=V[x] if x>0 else -V[-x]
 return s
def gens(p,w):
 m=[]
 for i in range(64):
  x=p[i]
  if not x or (x>0)!=w:continue
  a=abs(x)
  if a==P:
   d=8 if w else -8
   if 0<=i+d<64 and not p[i+d]:m.append((i,i+d))
   for e in (-1,1):
    j=i+d+e
    if 0<=j<64 and abs(j%8-i%8)==1 and p[j] and (p[j]>0)!=w:m.append((i,j))
  elif a==N:
   for d in (-17,-15,-10,-6,6,10,15,17):
    j=i+d
    if 0<=j<64 and abs(j%8-i%8)<3 and (not p[j] or (p[j]>0)!=w):m.append((i,j))
  elif a in (B,R,Q):
   ds=[]
   if a in (B,Q):ds+=[-9,-7,7,9]
   if a in (R,Q):ds+=[-8,-1,1,8]
   for d in ds:
    j=i+d
    while 0<=j<64:
     if abs((j%8)-(i%8))>1 and d not in (-8,8):break
     if p[j] and (p[j]>0)==w:break
     m.append((i,j))
     if p[j]:break
     j+=d
  elif a==K:
   for d in (-9,-8,-7,-1,1,7,8,9):
    j=i+d
    if 0<=j<64 and abs(j%8-i%8)<2 and (not p[j] or (p[j]>0)!=w):m.append((i,j))
 return m
def search(p,d,w,a,b):
 if d==0:return score(p),None
 ms=gens(p,w)
 if not ms:return (-20000 if w else 20000),None
 best= -99999 if w else 99999
 bm=None
 for f,t in ms:
  s,_=search(move(p,f,t),d-1,not w,-b,-a)
  s=-s
  if (w and s>best) or (not w and s<best):
   best=s;bm=(f,t)
  if w:a=max(a,s)
  else:b=min(b,s)
  if a>=b:break
 return best,bm
def main():
 p=board();w=True
 while 1:
  show(p)
  ms=gens(p,w)
  if not ms:
   print("End");break
  if w:
   try:
    u=input("move: ").strip()
    f=(ord(u[0])-97)+(8-int(u[1]))*8
    t=(ord(u[2])-97)+(8-int(u[3]))*8
    if (f,t) not in ms:print("bad");continue
   except:print("bad");continue
  else:
   _,bm=search(p,2,w,-99999,99999)
   f,t=bm
   print("AI:",chr(97+f%8)+str(8-f//8)+chr(97+t%8)+str(8-t//8))
  p=move(p,f,t);w=not w
if __name__=="__main__":
 if len(sys.argv)>1 and sys.argv[1]=="uci":
  print("id name Tiny4K\nuciok")
  while 1:
   l=sys.stdin.readline()
   if not l or l.startswith("quit"):break
   if l.startswith("isready"):print("readyok")
   if l.startswith("go"):print("bestmove e2e4")
 else:main()
