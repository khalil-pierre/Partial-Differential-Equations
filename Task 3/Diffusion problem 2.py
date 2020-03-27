# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 17:36:56 2019

@author: user
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as sp

def LU_lin_solver(A,b):
    '''Calculates the soultion to a linear equation using LU decomposition.'''
    lu,piv=sp.lu_factor(A)
    return sp.lu_solve((lu,piv),b)

N=100
dx=50/N
dt=0.5

Rod=np.linspace(0,50,N)
Temperature=np.zeros(N+2)
alpha=59/(450*7900)
gamma=alpha*dt/(dx**2)

for j  in range(N+2):
    if j==0:
        Temperature[j]=1000
    elif j==N+1:
        Temperature[j]=0
    else:
        Temperature[j]=20

CoefficentMatrix=np.zeros((N+2,N+2))

for i in range(1,N+1):
    CoefficentMatrix[i,i]=1+2*gamma
    CoefficentMatrix[i,i+1]=-gamma
    CoefficentMatrix[i,i-1]=-gamma

CoefficentMatrix[0,0]=1+2*gamma
CoefficentMatrix[0,1]=-gamma
CoefficentMatrix[N+1,N+1]=1

plt.imshow(CoefficentMatrix)
plt.show()
plt.clf()

time=0
for t in range(50):
    time+=dt
    Temperature=LU_lin_solver(CoefficentMatrix,Temperature)
    plt.plot(Rod,Temperature[1:-1])
    








