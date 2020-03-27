# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 14:09:11 2019

@author: user
"""

import random
import numpy as np
import matplotlib.pyplot as plt


def AdjacentPoints(V,i,j,Periodic=False):
    n=V.shape
    if Periodic==False:
        if i==0 or j==0 or i==n[0]-1 or j==n[1]-1:
            return V[i,j]
        else:
            return (1/4)*(V[i-1,j]+V[i+1,j]+V[i,j-1]+V[i,j+1])
    
    elif Periodic==True:
    
        if i==n[0]-1 and j!=n[1]-1:
            return (1/4)*(V[i-1,j]+V[0,j]+V[i,j-1]+V[i,j+1])
        
        elif j==n[1]-1 and i!=n[0]-1:
            return  (1/4)*(V[i-1,j]+V[i+1,j]+V[i,j-1]+V[i,0])
        
        elif i==n[0]-1 and j==n[1]-1:
            return (1/4)*(V[i-1,j]+V[0,j]+V[i,j-1]+V[i,0])
        
        else:
            return (1/4)*(V[i-1,j]+V[i+1,j]+V[i,j-1]+V[i,j+1])

def Grid(n,m):
    grid=np.zeros((n,m))
    for i in range(1,n-1):
        for j in range(1,m-1):
            grid[i,j]=random.randint(-10,10)
    return grid


N=25
Potential=Grid(N,N)
count=0
VOld=np.sum(Potential)
VNew=0

while abs((VNew-VOld))>1e-5:
    count+=1
    VOld=(1/N)*np.sum(Potential)
    
    for i in range(1,N-1):
        for j in range(1,N-1):
            Potential[i,j]=AdjacentPoints(Potential,i,j)
            
    VNew=(1/N)*np.sum(Potential)
                
plt.figure()
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
  

                
                
                
        

  