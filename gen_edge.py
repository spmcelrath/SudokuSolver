n = 3
m = 3
s = m*n

for i in range(s*s):
  x = i%9
  y = i/9
  bx = x/n
  by = y/m
  edges = ""
  for j in range(s):
    if (j/m != by):
      #print i, j*s+x
      edges = edges + "," + str(j*s+x)
    if (j/n != bx):
      #print i, y*s+j
      edges = edges + "," + str(y*s+j)
  for j in range(n):
    for k in range(m):
      if (i != bx*n + by*m*s + j + k*s):
        #print i, bx*n + by*m*s + j + k*s
        edges = edges + "," + str(bx*n+by*m*s+j+k*s)
  print i, edges[1:]
