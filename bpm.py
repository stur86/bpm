# Integrating a 1+1D or 1+2D NLSE with different initial conditions and for different potentials.
# To run this code type the command:
# python3 bpm.py example 1D    for a 1D example   (1D.py file needed)
# python3 bpm.py example 2D    for a 2D example   (2D.py file needed)
# where example.py contains the details for the particular example and should be placed in
# the directory ./examples1D   or   ./examples2D

import numpy as np
import sys
import os
import importlib
import glob
import argparse as ap

parser = ap.ArgumentParser(
    description='Solve the Schroedinger equation.')
parser.add_argument('system', type=str,
                    help='System to run the simulation on')
parser.add_argument('mode', type=str, default='1D',
                    help='Dimensionality of the problem')
parser.add_argument('--ground', '-g', action='store_true', default=False,
                    help='If true, converge to the ground state instead of '
                    'time evolution')
args = parser.parse_args()

# Preliminaries (handling directories and files)
# adds to path the directory with examples
sys.path.insert(0, './examples'+args.mode)
# directory for images and video output
output_folder = './examples'+args.mode+'/'+args.system
# creates folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Erase all image files (if exist) before starting computation and generating new output
try:
    for filename in glob.glob(output_folder+'/*.png'):
        os.remove(filename)
except:
    pass

# imports the file with the details for the computation
my = importlib.__import__(args.system)
build = importlib.__import__(args.mode)        # selects 1D or 2D


# Initialization of the computation

x, y = build.grid(my.Nx, my.Ny, my.xmax, my.ymax)      # builds spatial grid
psi = my.psi_0(x, y)                     # loads initial condition
psi0_norm = np.linalg.norm(psi)

L = build.L(my.Nx, my.Ny, my.xmax, my.ymax)        # Laplacian in Fourier space
# linear phase in Fourier space (including point swap)
linear_phase = np.fft.fftshift(np.exp((1.0 if args.ground else 1.0j)*L*my.dt/2))
# Absorbing shell at the border of the computational window
border = build.absorb(x, y, my.xmax, my.ymax, my.dt, my.absorb_coeff)

# Creates a vector to save the data of |psi|^2 for the final plot
savepsi = np.zeros((my.Nx, my.images+1))
# Number of computational steps between consecutive graphic outputs
steps_image = int(my.tmax/my.dt/my.images)


# Main computational loop
print("calculating", end="", flush=True)
for j in range(steps_image*my.images+1):        # propagation loop
    if j % steps_image == 0:  # Generates image output
        build.output(x, y, psi, int(j/steps_image), j*my.dt,
                     output_folder, my.output_choice, my.fixmaximum)
        savepsi[:, int(j/steps_image)] = build.savepsi(my.Ny, psi)
        print(".", end="", flush=True)

    V = my.V(x, y, j*my.dt, psi)           # potential operator
    psi *= np.exp(-1.j*my.dt*V)         # potential phase
    if sys.argv[2] == "1D":
        psi = np.fft.fft(psi)           # 1D Fourier transform
        psi *= linear_phase              # linear phase from the Laplacian term
        # inverse Fourier transform and damping by the absorbing shell
        psi = border*np.fft.ifft(psi)
    elif sys.argv[2] == "2D":
        psi = np.fft.fft2(psi)          # 2D Fourier transform
        psi *= linear_phase              # linear phase from the Laplacian term
        # inverse Fourier transform and damping by the absorbing shell
        psi = border*np.fft.ifft2(psi)
    else:
        print("Not implemented")

    psi *= psi0_norm/np.linalg.norm(psi)

# Final operations
# Generates some extra output after the computation is finished and save the final value of psi:

build.final_output(output_folder, x, steps_image*my.dt, psi,
                   savepsi, my.output_choice, my.images, my.fixmaximum)
print()
