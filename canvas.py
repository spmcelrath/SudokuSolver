from Tkinter import *
import ttk
import copy
import time
import random

def killnonos():
  global w
  global rects
  for i in rects:
    w.delete(i)

def nono():
  global w
  global rects
  global edges
  global m
  global n
  global s
  s=n*m
  bins = []
  nonos = []
  for i in range(s*s):
    nonos.append(-1)
    if i<s:
      bins.append([])

  for i in range(len(svlist)):
    if svlist[i].get() in number.keys():
      nonos[i] = number[svlist[i].get()]
      bins[number[svlist[i].get()]].append(i)

  flag = True
  for i in bins:
    if len(i)!=s:
      print "INVALID ARRANGEMENT"
      flag = False
  
  if flag:
    edges = {}

    for i in range(s*s):
      x = i%s
      y = i/s
      edges[str(i)] = []
      for j in range(s):
        if (j*s+x!=i):
          edges[str(i)].append(str(j*s+x))
        if (y*s+j!=i):
          edges[str(i)].append(str(y*s+j))
      for j in bins[nonos[i]]:
        if str(j) not in edges[str(i)] and i!=j:
          edges[str(i)].append(str(j))
      rects.append(w.create_rectangle(15+(h-20)*x/s,15+(h-20)*y/s,5+(h-20)*(x+1)/s,(h-20)*(y+1)/s,fill=color[nonos[i]]))

def genboard1():
  genboard(1)

def genboard2():
  genboard(s/2)

def genboard3():
  genboard(2*s)

def genboard(limit):
  global board
  global final
  global sols
  global answers
  global s

  t = time.time()
  reset()

  sols.append([copy.deepcopy(board),copy.deepcopy(final)])

  keep = []
  while len(answers)==0 and len(sols)>0:
    #print len(sols), ", ", len(sols[0][0])
    pick(sols)
  keep = copy.deepcopy(answers[0])
  
  while limit>0:
    sols = []
    board = []
    for i in range(len(final)):
      board.append([i,range(s)])
    answers = []
    final = copy.deepcopy(keep)
    flag = True
    while flag:
      rc = random.randint(0,len(final)-1)
      if final[rc]!=-1:
        final[rc]=-1
        flag = False
    sols.append([copy.deepcopy(board),copy.deepcopy(final)])
    while len(sols)>0:
      #print len(sols), ", ", len(sols[0][0])
      pick(sols)
    if len(answers)==1:
      keep = copy.deepcopy(final)
    if len(answers)!=1:
      limit-=1
  writeto(keep)

def genedge():
  global edges
  global m
  global n
  global s
  s=n*m
  edges = {}
  if m==3 and n==3:
    for i in edge0[:-1]:
      pair = i.split()
      edges[pair[0]] = pair[1].split(",")
  if m!=3 or n!=3:
    for i in range(s*s):
      x = i%s
      y = i/s
      bx = x/n
      by = y/m
      edges[str(i)] = []
      for j in range(s):
        if (j/m != by):
          edges[str(i)].append(str(j*s+x))
        if (j/n != bx):
          edges[str(i)].append(str(y*s+j))
      for j in range(n):
        for k in range(m):
          if (i != bx*n + by*m*s + j + k*s):
            edges[str(i)].append(str(bx*n+by*m*s+j+k*s))


def drawlines():
  global m
  global n
  global s
  s = n*m

  global lines
  for line in lines:
    w.delete(line)
  lines = []

  global elist
  global svlist
  elist = []
  svlist = []
  for i in range(s*s):
    svlist.append(StringVar())
    svlist[i].set(i)
    elist.append(Entry(master,textvariable=svlist[i],width=2))
    lines.append(w.create_window(10+(h-20)/s*(i%s+.5),10+(h-20)/s*(int(i/s)+.5),window=elist[i]))

  for i in range(s+1):
    for j in range(s+1):
      b=1
      if i%n==0:
        b=3
      lines.append(w.create_line(10+(h-20)*i/s,10,10+(h-20)*i/s,h-10,fill="#000000",width=b))
      b=1
      if j%m==0:
        b=3
      lines.append(w.create_line(10,10+(h-20)*j/s,h-10,10+(h-20)*j/s,fill="#000000",width=b))

def reset():
  global n
  global m
  flag = False
  if nval.get()!="" and int(nval.get())!=n:
    n = int(nval.get())
    flag = True
  if mval.get()!="" and int(mval.get())!=m:
    m = int(mval.get())
    flag = True
  if flag:
    genedge()
    drawlines()
    killnonos()
  reseth()
  writeto(final)  

def reseth():
  global n
  global m
  global s
  s=n*m
  global board
  global final
  global sols
  global answers
  board = []
  final = []
  sols  = []
  answers = []

  for i in range(s*s):
    final.append(-1)
    board.append([i,range(s)[:]])

def finalcheck(brd):
  for i in range(len(brd)):
    for j in edges[str(i)]:
      if brd[int(j)]==brd[i]:
        return False
  return True
      

def printboard(final):
  for i in range(s):
    temp = ""
    for j in range(s):
      if (final[s*i+j]!=-1):
        temp = temp + letter[final[s*i+j]]
        temp = temp + "\t"
      elif (final[s*i+j]==-1):
        temp += "?"
        temp += "\t"
    print temp

def pick(sols):
  if len(sols)==0:
    print "NO (more) SOLUTIONS"
    return 
  b = sols[0][0]
  if len(b)==0:
    if finalcheck(sols[0][1]):
      answers.append(copy.deepcopy(sols[0][1]))
    sols.pop(0)
    return
  
  b.sort(key=lambda x: len(x[1]))
  if (len(b[0][1]) == 0):				#guess failed
    sols.pop(0)
    return
  if (len(b[0][1]) == 1):				#number determined
    sols[0][1][b[0][0]] = b[0][1][0]
    b.pop(0)
    deduce(sols[0])
    return
  if (len(b[0][1]) > 1):
    s0 = sols.pop(0)
    for guess in s0[0][0][1]:
      btemp = copy.deepcopy(s0[0])
      ftemp = copy.deepcopy(s0[1])
      ftemp[b[0][0]] = guess
      btemp.pop(0)
      deduce([btemp,ftemp])
      #sols.append(copy.deepcopy([btemp,ftemp]))
      
      sols.insert(0,copy.deepcopy([btemp,ftemp]))


def deduce(duo):
  bnew = duo[0]
  fnew = duo[1]
  for cell in bnew:
    for k in edges[str(cell[0])]:
      if fnew[int(k)] in cell[1]:
        cell[1].remove(fnew[int(k)])
        #print "removing", fnew[int(k)], "from", cell[0]

def readfrom():
  board = []
  final = []
  for i in range(s*s):
    final.append(-1)
    board.append([i,range(s)[:]])

  for i in range(len(svlist)):
    if svlist[i].get() in number.keys():
      board[i][1] = [number[svlist[i].get()]]
  return board

def writeto(brd):
  for i in range(len(brd)):
    if brd[i]!=-1:
      svlist[i].set(letter[brd[i]])
    if brd[i]==-1:
      svlist[i].set("")

def show():
  if solnum.get()!="":
    if int(solnum.get()) in range(len(answers)):
      writeto(answers[int(solnum.get())])

def solve():
  t = time.time()
  
  reseth()
  board = copy.deepcopy(readfrom())
  sols.append([copy.deepcopy(board),copy.deepcopy(final)])

  while len(sols)>0:
    #print len(sols), ", ", len(sols[0][0])
    pick(sols)

  for yeet in answers:
    printboard(yeet)
    writeto(yeet)
    print " "
  print "TOTAL SOLUTIONS: ", len(answers)
  print "TIME OF CODE: ", time.time()-t
  butt.set("TIME (s): " + str(time.time()-t))
  numsols.set("SOLUTIONS: " + str(len(answers)))

########################################################
  
board0 = open("s3.txt","r").read().split()
n = int(board0[0])
m = int(board0[1])
s = n*m


edge0 = open("edge.txt","r").read().split("\n")
edges = {}
if m==3 and n==3:
  for i in edge0[:-1]:
    pair = i.split()
    edges[pair[0]] = pair[1].split(",")
if m!=3 or n!=3:
  for i in range(s*s):
    x = i%s
    y = i/s
    bx = x/n
    by = y/m
    edges[str(i)] = []
    for j in range(s):
      if (j/m != by):
        edges[str(i)].append(str(j*s+x))
      if (j/n != bx):
        edges[str(i)].append(str(y*s+j))
    for j in range(n):
      for k in range(m):
        if (i != bx*n + by*m*s + j + k*s):
          edges[str(i)].append(str(bx*n+by*m*s+j+k*s))

if len(edges)!=s*s:
  print "INVALID"

colors0 = open("colors.txt","r").read().split("\n")
color = {}
for i in colors0[:-1]:
  pair = i.split()
  color[int(pair[0])] = pair[1]

dict0 = open("dict.txt","r").read().split("\n")
letter = {}
number = {}
for i in dict0[:-1]:
  pair = i.split()
  letter[int(pair[0])] = pair[1]
  number[pair[1]] = int(pair[0])

letter2 = {}
number2 = {}
left = range(s)
while len(left)>0:
  rc = random.randint(0,len(left)-1)
  letter2[left[rc]] = str(s-len(left)+1)
  number2[str(s-len(left)+1)] = left[rc]
  left.pop(rc)
  
###########################################################

board = []
final = []
sols  = []
answers = []

for i in range(s*s):
  final.append(-1)
  board.append([i,range(s)[:]])

count = 0
for i in board0[2:]:
  for j in i.split(","):
    if (j != '?'):
      board[count][1] = [number[j]]
      final[count] = number[j]
    count+=1

board.sort(key=lambda x: len(x[1]))

#######################################################

master = Tk()
h=500
w = Canvas(master,width=2*h,height=h)
w.pack()

rects = []

lines = []
for i in range(s+1):
  for j in range(s+1):
    b=1
    if i%n==0:
      b=3
    lines.append(w.create_line(10+(h-20)*i/s,10,10+(h-20)*i/s,h-10,fill="#000000",width=b))
    b=1
    if j%m==0:
      b=3
    lines.append(w.create_line(10,10+(h-20)*j/s,h-10,10+(h-20)*j/s,fill="#000000",width=b))

elist = []
svlist = []
rectlist = []
for i in range(s*s):
  svlist.append(StringVar())
  svlist[i].set(i)
  elist.append(Entry(master,textvariable=svlist[i],width=2))
  lines.append(w.create_window(10+(h-20)/s*(i%s+.5),10+(h-20)/s*(int(i/s)+.5),window=elist[i]))

butt = StringVar()
numsols = StringVar()
solnum = StringVar()
e = Label(master,textvariable=butt)
w.create_window(600,100,window=e)
fritz = Button(master,text="SOLVE",command=solve)
w.create_window(600,50,window=fritz)
dylan = Button(master,text="RESET",command=reset)
w.create_window(800,50,window=dylan)
gerard = Button(master,text="SEE SOLUTION:",command=show)
w.create_window(600,150,window=gerard)
boris = Label(master,textvariable=numsols)
w.create_window(800,100,window=boris)
gook = Entry(master,textvariable=solnum)
w.create_window(800,150,window=gook)
cookout = Label(master,text="GENERATE:")
w.create_window(600,300,window=cookout)
gen1 = Button(master,text="EASY",command=genboard1)
w.create_window(700,300,window=gen1)
gen2 = Button(master,text="MEDIUM",command=genboard2)
w.create_window(775,300,window=gen2)
gen3 = Button(master,text="HARD",command=genboard3)
w.create_window(850,300,window=gen3)
conan = Button(master,text="SET NONOMINOS",command=nono)
w.create_window(600,400,window=conan)


mval = StringVar()
nval = StringVar()
mval.set(m)
nval.set(n)

mtext = Label(master,text="m=")
w.create_window(600,200,window=mtext)
ntext = Label(master,text="n=")
w.create_window(600,250,window=ntext)
mtext2 = Entry(master,text=mval)
w.create_window(800,200,window=mtext2)
ntext2 = Entry(master,text=nval)
w.create_window(800,250,window=ntext2)


writeto(final)
mainloop()
