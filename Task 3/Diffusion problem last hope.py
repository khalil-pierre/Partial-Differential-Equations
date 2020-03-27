# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 14:02:49 2019

@author: user
"""

import numpy as np
import matplotlib.pyplot as plt


N=50
dx=50/N
dt=1000
alpha=59/(450*7900)#Collective diffusion coefficent 
gamma=alpha*dt/((dx)**2)
T0=1000 #Teampreture of heat resivour (Furnace)

Rod=np.linspace(0,50,N)
Temp=20*np.ones(N)
CoefficentMatrix=np.zeros((N,N))

for i in range(1,N-1):
    for j in range(1,N-1):
        CoefficentMatrix[i,i]=1+2*gamma 
        CoefficentMatrix[i,i+1]=CoefficentMatrix[i,i-1]=-gamma      

CoefficentMatrix[0,0]=1+3*gamma
CoefficentMatrix[-1,-1]=1+gamma
CoefficentMatrix[0,1]=-gamma
CoefficentMatrix[-1,-2]=-gamma

time=0
count=0
plt.figure(1)
for t in range(50z):
    plt.clf()
    count+=1
    time+=dt
    Temp[0]+=2*gamma*T0
    Temp=np.linalg.solve(CoefficentMatrix,Temp)
    plt.plot(Rod,Temp)
    plt.axis([0,50,0,1100])
    plt.show()
    plt.pause(1e-30)
    
plt.show()    
plt.clf()


    
    