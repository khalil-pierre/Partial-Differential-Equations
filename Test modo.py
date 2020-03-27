# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 03:05:02 2019

@author: user
"""
import numpy as np

def GaussSeidel(n,m,conditions,voltage,capacitor='0'):
    count = 0
    sumbefore = []    
    sumafter = [] 
    grid = conditions
    percentage = 10
    while percentage > 1e-15:      #convergence condition
        sumbefore = np.copy(grid) 
        for i in range(1,n-1):       #between 1 and n-1/m-1 to cover all the points in the grid except the edges
            for j in range(1,m-1):
                if capacitor =='yes':
                    if grid[i][j] != abs(voltage):     #condition to ensure that the capacitor is not changed while the Gauss Seidel method is used
                        grid[i][j] = 0.25 * (grid[i-1][j] + grid[i+1][j] + grid[i][j-1] + grid[i][j+1])    
                else:
                    grid[i][j] = 0.25 * (grid[i-1][j] + grid[i+1][j] + grid[i][j-1] + grid[i][j+1])
        sumafter = np.copy(grid)
        difference = abs(sumafter - sumbefore)
        percentage = abs(np.amax(difference)/np.amax(sumafter))      #defines a percentage difference of the matrix before and after iteration 
        count += 1     #determines the number of iterations completed until the convergence condition is satisfied
    print('Number of iterations = ', count)
    return grid