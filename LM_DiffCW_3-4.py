'''
Suppose we have a distribution of charges and we want to calculate the resulting electric field.
One way to do this is to first calculate the electric potential φ and then take its gradient.

You have two charges, of ±1 C, 10 cm apart. Calculate the resulting electric potential on 
a 1 m × 1 m square plane surrounding the charges and passing through them.
'''
import argparse
import numpy as np
import matplotlib.pyplot as plt
import astropy.constants as con
import astropy.units as u

# epsilon = 8.85e-12

# each charge
q1 = 1
q2 = -1
# both charges are 10 cm or 0.1 m apart
q_dist = 0.1 # m

# positions of the charges on the plane
xq1 = -0.05 #half the cm
yq1 = 0
xq2 = 0.05 #other half the cm
yq2 = 0

 # epsilon
ep_z = 8.85e-12 

n = 100 # number of points i want in this grid plot
phi = np.zeros((n,n)) # an array of n x n number of points in the grid
# to plot the points, we need to generate x and y values like so:

''' 
Now calculate the partial derivatives of the potential with respect to x and y and 
hence find the electric field in the xy plane. Make a visualization of the field also.
'''
phi_px = np.zeros((n-1,n-1))
phi_py = np.zeros((n-1,n-1))

x_list = np.zeros((n-1,n-1))
y_list = np.zeros((n-1,n-1))

# taking the difference of the two values of phi and dividing by the distance between them gives us the derivative
# electric field
def efx(phi, j, i):
    partialx = (phi[j,i] - phi[j , i+1]) / (1/n)
    return partialx

def efy(phi, j, i):
    partialy = (phi[j,i] - phi[j+1, i]) / (1/n)
    return partialy
    

# x values gen
for i in range (0, n-1):
    x = -0.5 + 1/n * i

    # y values gen
    for j in range (0, n-1):
        y = -0.5 + 1/n * j
    
        # each charge will have its own radius (distance) from each surrounding charge
        # if r = sqrt(x^2 + y^2)
        r1 = np.sqrt((x - xq1)**2 + (y - yq1)**2)
        r2 = np.sqrt((x - xq2)**2 + (y - yq2)**2)

        # calculate the electric potential phi
        phi1 = q1 / (4*np.pi*ep_z*r1)
        phi2 = q2 / (4*np.pi*ep_z*r2)

        phi[j,i] = phi1 + phi2

        phi_px[j,i] = efx(phi, j, i)
        phi_py[j,i] = efy(phi, j, i)

        x_list[j,i] = x
        y_list[j,i] = y

print(phi.size)
print(phi_px.size)
print(phi_py.size)
print(x_list.size)
print(y_list.size)

# plots the two charges for reference
plt.scatter(xq2 , yq2, c = 'blue')
plt.scatter(xq1 , yq1, c = 'red')

# ef
# !!! Fix slice to get only i or j 
plt.quiver(x_list[0:n:3], y_list[0:n:3], phi_px[0:n:3], phi_py[0:n:3])

# actually plots the potential as a gradient
#plt.imshow(phi, extent = [-1.25, 1.25, -1.25, 1.25], vmin=-1e11, vmax=1e11)
plt.colorbar()
plt.show()
    
###############################################################################

# plt.axline((0, 50), (100, 50), linestyle='--', color='w')

