import argparse
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Monte Carlo Random Walk Animation",
        description="Simulates a 2D random walk within a bounded grid and animates the particle motion."
    )
    parser.add_argument(
        "--steps", type=int, default=1000,
        help="Number of steps in the random walk (default: 1000)"
    )
    parser.add_argument(
        "--bounds", type=int, default=10,
        help="Half-width of the square boundary [-L, L] (default: 10)"
    )
    parser.add_argument(
        "--fps", type=int, default=30,
        help="Frames per second for the animation (default: 30)"
    )
    args = parser.parse_args()

    N = args.steps
    L = args.bounds

    p = [0,0]
    pointsxy = []

    for i in range(N):
        xory = np.random.choice(['x', 'y'])
        if (xory == 'x'):
            rx = int(np.random.choice([1,-1]))
            if (abs(p[0] + rx) >= L):
                rx = -rx
                p[0] += rx
            else:
                p[0] = p[0] + rx
            pointsxy.append(p.copy())
        if (xory == 'y'):
            ry = int(np.random.choice([1,-1]))
            if (abs(p[1] + ry) >= L):
                ry = -ry
                p[1] += ry
                pointsxy.append(p.copy())
            else:
                p[1] = p[1] + ry
                pointsxy.append(p.copy())

    print(pointsxy[i])

    fig = plt.figure(figsize=(L,L))
    ax = plt.axes(xlim=(-L, L), ylim=(-L, L))
    dust = plt.Circle((0,0),radius=0.3,facecolor='gray')
    ax.add_patch(dust)

    def init():
        dust.center = (0, 0)
        ax.add_patch(dust)
        return (dust,)

    def animate(i):
        anipxy = pointsxy[i]
        dust.center = anipxy
        return (dust,)

    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(pointsxy), interval=20, blit=True)
    writergif = animation.PillowWriter(fps=args.fps)
    ani.save('dust.gif', writer=writergif)

    # --- Exercise 10.8: Importance Sampling Integral ---
    # I = integral from 0 to 1 of x^(-1/2) / (e^x + 1) dx
    # w(x) = x^(-1/2), p(x) = 1/(2*sqrt(x)), transformation x = z^2

    N_samples = 1000000
    z = np.random.uniform(0, 1, N_samples)  # uniform samples
    x = z**2                                # transform: samples from p(x) = 1/(2*sqrt(x))
    I = 2 * np.mean(1.0 / (np.exp(x) + 1)) # factor of 2 from jacobian dx = 2z dz

    print("Exercise 10.8 - Importance Sampling Integral")
    print("I =", round(I, 5), "(expected ~0.84)")