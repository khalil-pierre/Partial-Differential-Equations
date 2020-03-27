# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:56:28 2019

@author: user
"""
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.animation as animation

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
    CoefficentMatrix=np.zeros((Nx,Nx))
    for i in range(1,Nx-1):
            CoefficentMatrix[i,i]=1+2*gamma 
            CoefficentMatrix[i,i+1]=CoefficentMatrix[i,i-1]=-gamma 
        
    CoefficentMatrix[0,0]=1+3*gamma
    CoefficentMatrix[0,1]=CoefficentMatrix[-1,-2]=-gamma
    
    if Neumann==True:    
        CoefficentMatrix[-1,-1]=1+gamma
    
    elif Neumann==False:
        CoefficentMatrix[-1,-1]=1+3*gamma
        
    for t in range(Nt):
        Temp[0]+=2*gamma*TH
        
        if Neumann==False:
            Temp[-1]+=2*gamma*TC
            
        Temp=np.linalg.solve(CoefficentMatrix,Temp)
        
    return Temp,Rod



T=np.linspace(100,10000,100)

for i in T:
    plt.clf()
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
    plt.pause(0.1)





#
#Time=[]
#Z=[]
#for i in T:
#    Z.append(TempDiffusion(50,100,i,100,1000)[0])
#    x=np.linspace(0,50,100)
#    Time.append(i)
#
#plt.imshow(Z)
#plt.show()

'''
fig=plt.figure()
ax=fig.add_subplot(1,1,1,projection='3d')
ax.plot_surface(x, Time, Z)
plt.show()
'''