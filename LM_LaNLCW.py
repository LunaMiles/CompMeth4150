# Status: Completed, not submitted
import argparse
import numpy as np
import matplotlib.pyplot as plt

m = 9.1094e-31 # electron mass in kg
hbar = 1.0546e-34 # reduced Planck's constant in J*s
eV = 1.6022e-19 # 1 electron volt in Joules

def y1(E, w):
    return np.tan(np.sqrt(w**2 * m * E / (2 * hbar**2)))

def y2(E, V):
    return np.sqrt((V - E) / E) # even states

def y3(E, V):
    return -np.sqrt(E / (V - E)) # odd states

def binary_search(f, a, b, tol=0.001*eV):
    while (b - a) > tol:
        mid = (a + b) / 2
        if f(a) * f(mid) < 0:
            b = mid
        else:
            a = mid
    return (a + b) / 2

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find energy levels of a quantum particle in a square potential well."
    )
    parser.add_argument(
        "--V", type=float, default=20.0,
        help="Wall height in eV (default: 20.0)"
    )
    parser.add_argument(
        "--w", type=float, default=1e-9,
        help="Well width in meters (default: 1e-9)"
    )
    parser.add_argument(
        "--n_points", type=int, default=1000,
        help="Number of plot points (default: 1000)"
    )
    args = parser.parse_args()

    V = args.V * eV
    w = args.w

    ################################################################################

    E_vals = np.linspace(1e-3 * eV, V - 1e-3 * eV, args.n_points)

    Y1 = np.where(np.abs(y1(E_vals, w)) > 10, np.nan, y1(E_vals, w))   # clip tan discontinuities
    Y2 = y2(E_vals, V)
    Y3 = y3(E_vals, V)

    plt.plot(E_vals / eV, Y1, label="y1")
    plt.plot(E_vals / eV, Y2, label="y2 (even)")
    plt.plot(E_vals / eV, Y3, label="y3 (odd)")
    plt.ylim(-10, 10)
    plt.xlabel("E (eV)")
    plt.legend()
    plt.grid(True)
    plt.show()

    ###############################################################################

    E_scan = np.linspace(1e-3 * eV, V - 1e-3 * eV, 10000)
    energies = []

    for func in [lambda E: y1(E, w) - y2(E, V),
                 lambda E: y1(E, w) - y3(E, V)]:
        for k in range(len(E_scan) - 1):
            a, b = E_scan[k], E_scan[k+1]
            fa, fb = func(a), func(b)
            if np.isfinite(fa) and np.isfinite(fb) and fa * fb < 0:
                energies.append(binary_search(func, a, b) / eV)

    energies = sorted(set(round(e, 3) for e in energies))[:6]

    print("First six energy levels (eV):")
    for i, e in enumerate(energies):
        print("State", i, ":", e, "eV")