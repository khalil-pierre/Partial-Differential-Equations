# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 23:06:52 2019

@author: user
"""

"""
Created on Sat Mar  2 23:19:02 2019

@author: Christina
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la



alpha = 59/(450*7900)

N_x = 11
N_t = 100
time = 10000

dt = time/N_t

length = 0.5
dx = length/(N_x-1)
x = np.linspace(0, length, N_x)

T = np.zeros(N_x)
A = np.zeros((N_x,N_x))
B = np.zeros(N_x)

T[:] = 20

for k in range(N_t):
    for i in range(N_x):
        if i==0:
            A[i][i]=(2*dt*alpha/(dx*dx))+1
            A[i][i+1]=-dt*alpha/(dx*dx)
            B[i] = T[i]+1000*dt*alpha/(dx*dx)
        elif i==N_x-1:
            A[i][i]=(2*dt*alpha/(dx*dx))+1
            A[i][i-1]=-2*dt*alpha/(dx*dx)
            B[i]=T[i]
        else:
            A[i][i]=(2*dt*alpha/(dx*dx))+1
            A[i][i+1]=-dt*alpha/(dx*dx)
            A[i][i-1]=-dt*alpha/(dx*dx)
            B[i]=T[i]
    T_next = la.solve(A,B)
    T, T_next = T_next, T

plt.plot(x, T)
#-----------------------------------------------------------------------------
alpha = 59/(450*7900)

N_x = 11
N_t = 100
time = 10000

dt = time/N_t

length = 0.5
dx = length/(N_x-1)
x = np.linspace(0, length, N_x)

T = np.zeros(N_x)
A = np.zeros((N_x,N_x))
B = np.zeros(N_x)

T[:] = 20

for k in range(N_t):
    for i in range(N_x):
        if i==0:
            A[i][i]=(2*dt*alpha/(dx*dx))+1
            A[i][i+1]=-dt*alpha/(dx*dx)
            B[i] = T[i]+1000*dt*alpha/(dx*dx)
        elif i==N_x-1:
            A[i][i]=(2*dt*alpha/(dx*dx))+1
            A[i][i-1]=-dt*alpha/(dx*dx)
            B[i]=T[i]
        else:
            A[i][i]=(2*dt*alpha/(dx*dx))+1
            A[i][i+1]=-dt*alpha/(dx*dx)
            A[i][i-1]=-dt*alpha/(dx*dx)
            B[i]=T[i]
    T_next = la.solve(A,B)
    T, T_next = T_next, T
plt.grid()
plt.plot(x, T)