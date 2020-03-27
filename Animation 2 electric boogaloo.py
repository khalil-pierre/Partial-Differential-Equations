# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 20:43:22 2019

@author: user
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig=plt.figure()
#Creates a empty canvas in which we 
ax1=plt.axes(xlim=(-2,2),ylim=(-2,2))
#creates the axis that the data will be plotted against.
line,=ax1.plot([],[])
#initialise the line element that we want to animate
#Line object will be added to each itteration

def init():
    line.set_data([],[])
    return line,

#This function either sets all the data in the line to zero or creates a new list 
#at the end of the line object which data is added too.
#The line object is then returned and the next funtion animate will then take the 
#either empty line object or line with an empty end and fill it and then update the 
#plot.

def animate(i):
    x=np.linspace(-2,2,2000)
    y=np.sin(2 * np.pi * (x - 0.01 * i))
    #this is a traveling wave 
    line.set_data(x,y)
    return line,
#Animation function takes 1 argument frame number.
#Each frame it calculates a new sine wave that is shifted by 0.01 from the previous frame.


anim=animation.FuncAnimation(fig,animate,init_func=init,frames=100,interval=20,blit=True)
    
plt.show()

#
#x=np.linspace(0,2*np.pi,1000)
#y=np.sin(x)
#plt.figure(1)
#
#for t in range(0,100):
#    plt.clf()
#    Time=t/100
#    y=np.sin(2*np.pi*(x-Time))
#
#    plt.plot(x,y)
#    plt.axis([0,2*np.pi,-2,2])
#    plt.show()
#    plt.pause(0.000001)
# 