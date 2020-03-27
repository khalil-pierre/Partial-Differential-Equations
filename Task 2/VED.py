# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 11:26:45 2019

@author: user
"""
import numpy as np
import matplotlib.pyplot as plt
import random 

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

E=[]
Width=[]
for i in range(0,11):
    xs=np.linspace(-30,30,60)
    Para=ParallelPlate(60,60,1000,5+5*i,20,Grounded=True)
    Para=GaussSidel(Para,1e-5,V=1000,Capacitor=True)[0]
    ElectricFieldSlice=np.gradient(Para)[0][30]
    E+=[np.amax(ElectricFieldSlice)]
    Width+=[5+5*i]
    plt.plot(xs,ElectricFieldSlice,label='Seperation='+str(5+5*i))
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xlabel('Y position')
    plt.ylabel('Electric field Strength')
    
    
plt.show()
plt.clf()

TheoriticalE_Strength=[]
for j in Width:
    TheoriticalE_Strength+=[2000/j]

plt.plot(Width,E,label='E field strength')
plt.plot(Width,TheoriticalE_Strength,linestyle='--',label='Theoretical E field')
plt.xlabel('Plate width')
plt.ylabel('Electric Field')
plt.legend()
plt.show()
plt.clf()
