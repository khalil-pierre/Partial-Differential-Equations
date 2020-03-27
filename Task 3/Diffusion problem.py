# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 17:36:22 2019

@author: user
"""
import numpy as np
import matplotlib.pyplot as plt


N=100
XStep=50/N
TStep=0.05
Rod=np.linspace(0,50,N)
Temperature=np.zeros(N)
#Want the bounadry node to be constant
for i in range(N):
    if i==0:
        Temperature[i]=1000
    elif i==N+1:
        Temperature[i]=0
    else:
        Temperature[i]=20

alpha=59/(450*7900)
gamma=alpha*TStep/((XStep)**2)

CoefficentMatrix=np.zeros((N,N))

for i in range(1,N+1):
    CoefficentMatrix[i,i]=1+2*gamma
    CoefficentMatrix[i,i+1]=-gamma
    CoefficentMatrix[i,i-1]=-gamma
    
CoefficentMatrix[0,0]=CoefficentMatrix[N,N]=1  

print(CoefficentMatrix) 
plt.imshow(CoefficentMatrix)
plt.show()

Time=0
#plt.figure(1)
for t in range(0,100):
    #plt.clf()
    Time+=TStep
    Tempreture=np.linalg.solve(CoefficentMatrix,Temperature)
    plt.plot(Rod,Temperature)
    #plt.axis([0,50,20,23])
    #plt.show()
    #plt.pause(0.01)
    
plt.show()
plt.clf()


