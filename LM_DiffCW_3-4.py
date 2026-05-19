# Status: Completed, not submitted
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

ep_z = 8.85e-12 # epsilon

# taking the difference of the two values of phi and dividing by the distance between them gives us the derivative
def efx(phi, j, i, n):
    partialx = (phi[j,i] - phi[j, i+1]) / (1/n)
    return partialx

def efy(phi, j, i, n):
    partialy = (phi[j,i] - phi[j+1, i]) / (1/n)
    return partialy

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate and visualize the electric potential and field of two point charges."
    )
    parser.add_argument(
        "--n", type=int, default=100,
        help="Number of grid points along each axis (default: 100)"
    )
    parser.add_argument(
        "--q1", type=float, default=1.0,
        help="Magnitude of the positive charge in Coulombs (default: 1.0)"
    )
    parser.add_argument(
        "--q2", type=float, default=-1.0,
        help="Magnitude of the negative charge in Coulombs (default: -1.0)"
    )
    args = parser.parse_args()

    n = args.n
    q1 = args.q1
    q2 = args.q2

    phi = np.zeros((n,n)) # an array of n x n number of points in the grid

    phi_px = np.zeros((n-1,n-1))
    phi_py = np.zeros((n-1,n-1))

    x_list = np.zeros((n-1,n-1))
    y_list = np.zeros((n-1,n-1))

    # x values gen
    for i in range(0, n-1):
        x = -0.5 + 1/n * i

        # y values gen
        for j in range(0, n-1):
            y = -0.5 + 1/n * j

            # each charge will have its own radius (distance) from each surrounding charge
            r1 = np.sqrt((x - xq1)**2 + (y - yq1)**2)
            r2 = np.sqrt((x - xq2)**2 + (y - yq2)**2)

            # calculate the electric potential phi
            phi1 = q1 / (4*np.pi*ep_z*r1)
            phi2 = q2 / (4*np.pi*ep_z*r2)

            phi[j,i] = phi1 + phi2

            phi_px[j,i] = efx(phi, j, i, n)
            phi_py[j,i] = efy(phi, j, i, n)

            x_list[j,i] = x
            y_list[j,i] = y

    # density plot of electric potential 
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    im = ax1.imshow(phi, extent=[-0.5, 0.5, -0.5, 0.5], origin='lower', vmin=-1e11, vmax=1e11, cmap='RdBu')
    fig.colorbar(im, ax=ax1)
    ax1.scatter(xq1, yq1, c='red', zorder=5)   # positive charge
    ax1.scatter(xq2, yq2, c='blue', zorder=5)  # negative charge
    ax1.set_title("Electric Potential")
    ax1.set_xlabel("x (m)")
    ax1.set_ylabel("y (m)")

    # quiver plot of electric field 
    step = 5 # plot every 5th arrow to avoid clutter
    ax2.quiver(x_list[::step, ::step], y_list[::step, ::step], phi_px[::step, ::step], phi_py[::step, ::step])
    ax2.scatter(xq1, yq1, c='red', zorder=5)   # positive charge
    ax2.scatter(xq2, yq2, c='blue', zorder=5)  # negative charge
    ax2.set_title("Electric Field")
    ax2.set_xlabel("x (m)")
    ax2.set_ylabel("y (m)")

    plt.tight_layout()
    plt.show()