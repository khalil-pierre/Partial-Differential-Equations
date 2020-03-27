# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 11:52:58 2019

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
                grid[i,j]=1
        return grid
    elif Grounded==False:
        for i in range(n):
            for j in range(m):
                grid[i,j]=1
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
    #Takes a slice at our capacitor positions and sets the grid values as 
    #+ or - V.
    
    return ParaGrid

def GaussSidel(grid,Tol,V=0,Capacitor=False):
    #This function uses the gauss sidel method to approximate a soultion to laplaces 
    #equation. It takes in the grid with the bouandyry conditions that you want to evaluate
    #and itterates unitil the convergance condition is meet. The Tolerance is decided by the user.
    #When the grid of interest has a capacitor in it we have to avoid the nodes
    #that contain plates. This is done by checking if the grid value is equal to
    #either plate potential, if it is then that point is skipped over.
    n=grid.shape
    VOld=(1/n[0])*np.sum(grid)
    VNew=0
    count=0
    while abs((VNew-VOld))>Tol:
        count+=1
        VOld=(1/n[0])*np.sum(grid)
        for i in range(n[0]):
            for j in range(n[1]):
                if Capacitor==True:
                    if abs(grid[i,j])!=V:
                        grid[i,j]=AdjacentPoints(grid,i,j)
                else:
                    grid[i,j]=AdjacentPoints(grid,i,j)
        VNew=(1/n[0])*np.sum(grid)
        
    return grid,count

def Jacobi(grid,Tol):
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

# xp = np.linspace(0,100,20)
# y = [114,467,1024,1766,2683,3764,5003,6392,7927,9601]
# x = [10,20,30,40,50,60,70,80,90,100]    
# z = np.polyfit(x,y,2)
# p = np.poly1d(z)
# plt.plot(x,y,'.',xp,p(xp),'--')
# plt.xlabel('N')
# plt.ylabel('Iterations')
# plt.legend(('No. Iterations','Polynomial Fit'))
# plt.show()

xp = [1e-3,1e-4,1e-5,1e-6,1e-7,1e-8,1e-9,1e-10,1e-11,1e-12,1e-13,1e-14,1e-15]
Itterations=[]
Itterations2=[]
N=[]

for i in xp:
    SQbox=Grid(20,20,Grounded=True)
    SQbox2=Grid(20,20,Grounded=True)
    Itterations+=[np.amax(GaussSidel(SQbox,i)[0])]
    Itterations2+=[np.amax(Jacobi(SQbox2,i)[0])]
    N+=[(i)]
    
z = np.polyfit(N,Itterations,1)
z2= np.polyfit(N,Itterations2,1)
p = np.poly1d(z)
p2=np.poly1d(z2)
plt.plot(N,Itterations,'.',label='Gauss sidel method')#xp,p(xp),'--',label='Gauss sidel method')
#plt.plot(xp,p(xp))
plt.plot(N,Itterations2,'.',label='Jacobi method')#xp,p2(xp),'--',label='Jacobi method')
#plt.plot(xp,p2(xp))
#plt.xscale('log')
#plt.yscale('log')
plt.xlabel('Tolerance')
plt.ylabel('Error')
plt.legend()
plt.show()

    
    