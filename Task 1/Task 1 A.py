# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 14:09:11 2019

@author: user
"""

import random
import numpy as np
import matplotlib.pyplot as plt

N=100

Potential=np.zeros((N,N))
print(Potential)    

for i in range(N):
    for j in range(N):
        if j==0 or i==0 or i==N-1 or j==N-1:
            pass
        else:
            Potential[i,j]=random.randint(-10,10)


count=0
VOld=np.sum(Potential)*(1/N)
VNew=0

while round(VNew/VOld,5)!=1:
    count+=1
    print(count)
    print(VNew/VOld)
    VOld=np.sum(Potential)*(1/N)
    for i in range(N):
        for j in range(N):
            if j==0 or i==0 or i==N-1 or j==N-1:
                pass
            else:
                Lpoint=Potential[i-1,j]
                Rpoint=Potential[i+1,j]
                Apoint=Potential[i,j-1]
                Bpoint=Potential[i,j+1]
                
                Potential[i,j]=0.25*(Lpoint+Rpoint+Apoint+Bpoint)
                
                
    VNew=np.sum(Potential)*(1/N)

plt.imshow(Potential)
plt.colorbar()
plt.show()
plt.clf()

x=np.linspace(-2,2,N)
y=np.linspace(-2,2,N)
xv,yv=np.meshgrid(x,y)

plt.contourf(x,y,Potential)
plt.colorbar()
plt.xlabel('x position (m)')
plt.ylabel('y position (m)')
plt.show()
plt.clf()        
              
print(count)
  

                
                
                
        

  