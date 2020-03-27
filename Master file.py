# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 14:08:47 2019

@author: user
"""

import random
import numpy as np
import matplotlib.pyplot as plt
import copy 
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')

'''-------------------------------Task 1------------------------------------'''
#The functions I have defined bellow will be used in task 1 to solve the
#laplace equation using the finite differenc    e method.
 
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

#For the first task we were asked to use either the gauss sidel or Jacobi method
#to solve the laplace equation. To test that the methods work I am going to use a 
#Grounded square box. The potential within the box should converge to ground
#as our numerical soultion becomes more accurate (i.e after each itteration).
    
N=30
GroundedBoxGauss=Grid(N,N)
GroundedBoxJacobi=Grid(N,N)
GroundedBoxGauss,CountGauss=GaussSidel(GroundedBoxGauss,1e-9,V=0,Capacitor=False)
GroundedBoxJacobi,CountJacobi=Jacobi(GroundedBoxJacobi,1e-9)

print('The Gauss Sidel method meets the convergance condition in '+ str(CountGauss)+' iterations')
x=np.linspace(-N/2,N/2,N)
y=np.linspace(-N/2,N/2,N)
xv,yv=np.meshgrid(x,y)
plt.contourf(x,y,GroundedBoxGauss)
plt.colorbar()
plt.title('Grounded Box Potential Gauss sidel method')
plt.xlabel('X position')
plt.ylabel('Y position')
plt.show()
plt.clf()

print('The Jacobi method meets the convergance condition in '+ str(CountJacobi)+' iterations')
plt.contourf(x,y,GroundedBoxJacobi)
plt.colorbar()
plt.title('Grounded Box Potential Jacobi method')
plt.xlabel('X position')
plt.ylabel('Y position')
plt.show()
plt.clf()

#We were then asked to evaluate the behaviour of a parallel plate capacitor.

N=60
ParallelPlatePotential=ParallelPlate(N,N,1000,20,50,Grounded=True)
ParallelPlatePotential=GaussSidel(ParallelPlatePotential,1e-5,V=1000,Capacitor=True)[0]

xp=np.linspace(-30,30,N)
yp=np.linspace(-30,30,N)
xp,yp=np.meshgrid(xp,yp)
yg,xg=np.gradient(ParallelPlatePotential)
plt.contourf(xp,yp,ParallelPlatePotential)
plt.colorbar()
plt.quiver(xp[::4,::4],yp[::4,::4],-xg[::4,::4],-yg[::4,::4])
plt.title('Potential field of parallel plate capacitors')
plt.xlabel('X position')
plt.ylabel('Y position')
plt.show()
plt.clf()

#we were asked to show that the as the dimensions of the capacitor got larger
#the numerical soultion approximated the infinite plate soultion. To show this
#I took a vertical slice of the electric field at the center of the capacitor 
#plates and plotted how it changed as a function of plate width.
#
#E=[]
#Width=[]
##if you want to see how the potential change with seperation you can swap the
##20 and 10+10*i around in the ParallelPlate function arguments.
#for i in range(0,5):
#    xs=np.linspace(-30,30,60)
#    Para=ParallelPlate(60,60,1000,20,10+10*i,Grounded=True)
#    Para=GaussSidel(Para,1e-5,V=1000,Capacitor=True)[0]
#    ElectricFieldSlice=np.gradient(Para)[0][30]
#    E+=[np.amax(ElectricFieldSlice)]
#    Width+=[10+10*i]
#    plt.plot(xs,ElectricFieldSlice,label='Width='+str(10+10*i))
#    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#    plt.xlabel('Y position')
#    plt.ylabel('Electric field Strength')
#    
#plt.show()
#plt.clf()
#
##Not only the the electric field distribution have to approximate a top hat but
##the strength of the electric field within the capacitorplates should be givin by 
##E=V/D. Using the max value from my distributions I was able to plot E field
##strength against plate width. 
#TheoriticalE_Strength=100*np.ones(5)
#plt.plot(Width,E,label='E field strength')
#plt.plot(Width,TheoriticalE_Strength,linestyle='--',label='Theoretical E field')
#plt.xlabel('Plate width')
#plt.ylabel('Electric Field')
#plt.legend()
#plt.show()
#plt.clf()

'''---------------------------------Task 2----------------------------------'''
#In this section I have used finite difference method to solve the Heat equation

def TempDiffusion(RodLength,Nx,Time,Nt,TH,TC=0,Neumann=True):
    #Nx is the number of gridpoints, Nx is the number of itterations 
    #Time is the time you want the simulation to run in seconds
    #Nt is the numer of itterations the progrmam will run for
    #TH is the hot reseviour 
    #TC is the cold reservoir
    #If Neumann is true there is no heat flux out of the back end of the rod.
    dx=RodLength/Nx #Seperation between grid point in space
    dt=Time/Nt #Seperation between grid points in time 
    alpha=59/(450*7900) #Collective diffusion coefficent
    gamma=alpha*dt/((dx)**2)
    
    Rod=np.linspace(0,RodLength,Nx)
    Temp=20*np.ones(Nx)
    #Need to set up a coefficentMatrix that will be used to solve our system of linear 
    #equations.
    CoefficentMatrix=np.zeros((Nx,Nx))
    for i in range(1,Nx-1):
            CoefficentMatrix[i,i]=1+2*gamma 
            CoefficentMatrix[i,i+1]=CoefficentMatrix[i,i-1]=-gamma 
        
    CoefficentMatrix[0,0]=1+3*gamma
    CoefficentMatrix[0,1]=CoefficentMatrix[-1,-2]=-gamma
    
    if Neumann==True:    
        CoefficentMatrix[-1,-1]=1+gamma
        #For the Neumann boundary conditions the gradient of the temp goes to
        #zero at the boundary. We use this to approx the value of the "ghost cell''
        #on the other side of the boundary.
    elif Neumann==False:
        CoefficentMatrix[-1,-1]=1+3*gamma
        #For the Dirichlet boundary condition we fix the teampreture at the bouandry.
        #By taking the aveage of the ghost cell and the bouandry cell to be equal to 
        #the fixed temp we can solve for our ghost cell.    
    for t in range(Nt):
        Temp[0]+=2*gamma*TH
        if Neumann==False:
            Temp[-1]+=2*gamma*TC    
        Temp=np.linalg.solve(CoefficentMatrix,Temp)
    return Temp,Rod

def diffplotter(StartTime,EndTime,N,Neu=True):
    #This function plots the teampreture against position for multiple total times
    for time in np.linspace(StartTime,EndTime,N):
        y,x=TempDiffusion(0.5,100,time,100,1000,Neumann=Neu)
        if Neu==True:
            Title='Temperature across iron rod with no heat loss'
        if Neu==False:
            Title='Temperature across iron rod with cold reservoir'
        plt.title(Title)
        plt.plot(x,y,label='Time='+str(time)+'s') 
        plt.xlabel('Position (m)')
        plt.ylabel('Temperature (Celsius)')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

diffplotter(25,4000,5,Neu=False)
diffplotter(25,10000,5,Neu=True)

plt.switch_backend('Qt5Agg')

T=np.linspace(100,100000,1000)
#This segmant runs my animation. It takes a value from the T array above and then
#finds the tempreature distribution 
for i in T:
    plt.clf()#Clears the plot after each frame is plotted
    y,x=TempDiffusion(0.5,100,i,100,1000)
    y1,x1=TempDiffusion(0.5,100,i,100,1000,Neumann=False)
    plt.plot(x,y,label='No heat loss')
    plt.plot(x1,y1,label='Fixed temperature')
    plt.axis([0,0.5,0,1100])
    plt.legend()
    plt.xlabel('Position (m)')
    plt.ylabel('Temperature(Degrees)')
    plt.title('Time='+str(i)+'s')
    plt.show()
    plt.pause(0.1)#Adds a delay between each frame.

get_ipython().run_line_magic('matplotlib', 'inline')  

#This was the segmant of code I used to plot the number of itterations against matrix size,
#Number of itterations against convergance conditions which just means I had to plot the log 
#of the tolerance and use a polynomial fit of 1.
#This code is not included in my program due to the long run times.

#xp = np.linspace(10,100,30)
#Itterations=[]
#N=[]
#for i in xp:
#    SQbox=Grid(int(i),int(i),Grounded=True)
#    Itterations+=[GaussSidel(SQbox,1e-5)[1]]
#    N+=[i]
#    
#z = np.polyfit(N,Itterations,2)
#p = np.poly1d(z)
#plt.plot(N,Itterations,'.',xp,p(xp),'--')
#plt.xlabel('N')
#plt.ylabel('Iterations')
#plt.legend(('No. Iterations','Polynomial Fit'))
#plt.show()



