# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 14:08:47 2019

@author: user
"""

import random
import numpy as np
import matplotlib.pyplot as plt
import copy 
'''-------------------------------Task 1------------------------------------'''
#The functions I have defined bellow will be used in task 1 to solve the
#laplace equation using the finite difference method.
 
def AdjacentPoints(V,i,j,Periodic=False):
    #This function averages over the adjacent 4 point in the grid 
    #If periodic is true at the edge of the grid it will take the value of the 
    #grid at the opposite side.
    n=V.shape
    if Periodic==False:
        #There is a subtelty that I had to keep in mind when progrmaing this
        #When i or j is equal to 0, i-1 or j-1 will be -1 which will return the 
        #opposite bouandry point without any additional if statments.
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

def Grid(n,m,Grounded=True):
    #This function simply returns a grid where non-edge points are a random integer
    #between -10 and 10 and the edge points are set to 0 if grounded equals True.
    grid=np.zeros((n,m))
    if Grounded==True:    
        for i in range(1,n-1):
            for j in range(1,m-1):
                grid[i,j]=random.randint(-10,10)
        return grid
    elif Grounded==False:
        for i in range(n):
            for j in range(m):
                grid[i,j]=random.randint(-10,10)
        return grid

def ParallelPlate(n,m,V,sep,width,Grounded=False):
    #This function creates a grid with two parallel plates. Each plate has an 
    #opposite potential. The width and seperation of your grid are defined by 
    #input width and sep respectivly.
    if Grounded==True:
        ParaGrid=Grid(n,m)
    elif Grounded==False:
        ParaGrid=Grid(n,m,Grounded=False)
    
    TopPlatePos=int((m+sep)/2)
    BottomPlatePos=int((m-sep)/2)
    RightEdge=int((n+width)/2)
    LeftEdge=int((n-width)/2)
    
    ParaGrid[TopPlatePos,LeftEdge:RightEdge]=V
    ParaGrid[BottomPlatePos,LeftEdge:RightEdge]=-V
    
    return ParaGrid

def GaussSidel(grid,Tol,V,Capacitor=False):
    n=grid.shape
    VOld=(1/n[0])*np.sum(grid)
    VNew=0
    count=0
    while abs((VNew-VOld))>Tol:
        count+=1
        VOld=(1/n[0])*np.sum(grid)
        for i in range(n[0]):
            for j in range(n[1]):        
                grid[i,j]=AdjacentPoints(grid,i,j)
        VNew=(1/n[0])*np.sum(grid)
        
    return grid,count
    
def jacobi(grid,Tol):
    n=grid.shape
    VOld=(1/n[0])*np.sum(grid)
    VNew=0
    count=0
    gridOld=copy.deepcopy(grid)
    while abs((VNew-VOld))>Tol:
        count+=1
        VOld=(1/n[0])*np.sum(grid)
        for i in range(n[0]):
            for j in range(n[1]):
                grid[i,j]=AdjacentPoints(gridOld,i,j)
        gridOld=copy.deepcopy(grid)
        VNew=(1/n[0])*np.sum(grid)     
    
    return grid,count

N=25
GroundedBox=Grid(N,N)
GroundedBox,count=GaussSidel(GroundedBox,1e-5,0)

#For the first task we were asked to use either the gauss sidel or Jacobi method
#to solve the laplace equation. To test that the methods work I am going to use a 
#Grounded square box. The potential within the box should converge to ground
#as our numerical soultion becomes more accurate (i.e after each itteration).
print(count)
x=np.linspace(-2,2,N)
y=np.linspace(-2,2,N)
xv,yv=np.meshgrid(x,y)

plt.contourf(x,y,GroundedBox)
plt.colorbar()
plt.xlabel('x position (m)')
plt.ylabel('y position (m)')
plt.show()
plt.clf()
    
    




'''

count=0
VOld=np.sum(Potential)
VNew=0

while abs((1/N)*(VNew-VOld))>1e-67:
    count+=1
    VOld=np.sum(Potential)
    for i in range(N):
        for j in range(N):
            Potential[i,j]=AdjacentPoints(Potential,i,j)
    
    VNew=np.sum(Potential)
                

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
'''