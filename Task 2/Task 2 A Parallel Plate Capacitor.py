# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 15:32:24 2019

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

N=61
Potential=np.zeros((N,N))

for i in range(N):
    for j in range(N):
        if j>15 and j<45:
            if i==20:
                Potential[i,j]=1000
            elif i==40:
                Potential[i,j]=-1000
            
            else:
                Potential[i,j]=random.randint(-10,10)
        else:
            Potential[i,j]=random.randint(-10,10)
        
count=0
VOld=np.sum(Potential)
VNew=0

while abs(VOld-VNew)>1e-5:
    count+=1
    VOld=(1/N)*np.sum(Potential)
    for i in range(N):
        for j in range(N):
            if i==20 or i==40:
                if j>15 and j<45:
                    pass
                else:
                    Potential[i,j]=AdjacentPoints(Potential,i,j,Periodic=True)
            else:
                 Potential[i,j]=AdjacentPoints(Potential,i,j,Periodic=True)
    
    VNew=(1/N)*np.sum(Potential)
    
print(count)

x=np.linspace(-2,2,N)
y=np.linspace(-2,2,N)
xv,yv=np.meshgrid(x,y)
yg,xg=np.gradient(Potential)

plt.imshow(Potential)
plt.colorbar()
plt.show()
plt.clf()

plt.contourf(x,y,Potential)
plt.colorbar()
plt.xlabel('x position (m)')
plt.ylabel('y position (m)')
plt.quiver(xv[::4,::4],yv[::4,::4],-xg[::4,::4],-yg[::4,::4])
plt.show()
plt.clf()       
        
        
        
        
        
        
