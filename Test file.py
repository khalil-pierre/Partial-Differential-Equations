# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 13:38:18 2019

@author: user
"""
import numpy as np
import matplotlib.pyplot as plt

def I(x):
    return np.exp(-x**2)

Nx=100
L=50
N=10
T=5
TStep=T/N
XStep=L/Nx

alpha=59/(450*7900)
F=alpha*TStep/(XStep)**2

x = np.linspace(0, L, Nx+1)   # mesh points in space
dx = x[1] - x[0]
t = np.linspace(0, T, N+1)    # mesh points in time
u   = np.zeros(Nx+1)          # unknown u at new time level
u_n = np.zeros(Nx+1)          # u at the previous time level

# Data structures for the linear system
A = np.zeros((Nx+1, Nx+1))
b = np.zeros(Nx+1)

for i in range(1, Nx):
    A[i,i-1] = -F
    A[i,i+1] = -F
    A[i,i] = 1 + 2*F
A[0,0] = A[Nx,Nx] = 1

# Set initial condition u(x,0) = I(x)
for i in range(0, Nx+1):
    u_n[i] = I(x[i])

import scipy.linalg

for n in range(0, N):
    # Compute b and solve linear system
    for i in range(1, Nx):
        b[i] = -u_n[i]
    b[0] = b[Nx] = 0
    u[:] = scipy.linalg.solve(A, b)

    # Update u_n before next step
    u_n[:] = u
    
    plt.plot(x,u[:])
    
plt.show()