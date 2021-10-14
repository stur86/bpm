# File: ./examples1D/Lennard_Jones_1D.py
# A double Lennard-Jones potential, such as one could find along a hydrogen bond
# The initial condition is a Gaussian wavepacket

import numpy as np

Nx = 600                        # Grid points
Ny = Nx
dt = 0.001                  # Evolution step
tmax = 30                   # End of propagation 
xmax = 5                    # x-window size
ymax = xmax                 # y-window size
images = 300                # number of .png images  
absorb_coeff = 20       # 0 = periodic boundary
output_choice = 3         # If 1, it plots on the screen but does not save the images
                            # If 2, it saves the images but does not plot on the screen
                            # If 3, it saves the images and plots on the screen
fixmaximum= 1.25              # Fixes a maximum scale of |psi|**2 for the plots. If 0, it does not fix it.


r0 = xmax/2

def psi_0(x, y):

    f = 0.j+np.exp(-(x-xmax+r0)**2*4)

    return f

def V(x,y,t,psi):       # A Lennard-Jones potential

    sl = (x+xmax+1e-12)/(r0/2**(1/6)) # Fix the infinity
    sr = (xmax-x+1e-12)/(r0/2**(1/6)) # Fix the infinity
    V = 4*(1/sl**12-1/sl**6+1/sr**12-1/sr**6)

    V -= np.amin(V)

    return V