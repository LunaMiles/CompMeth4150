# Status: ready for submission
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def derivatives(r, m, R, rho, C, g):
    x, y, vx, vy = r # unpack position and velocity
    v = np.sqrt(vx**2 + vy**2) # magnitude of velocity
    k = np.pi * R**2 * rho * C / (2 * m) # drag constant from equations of motion
    ax = -k * vx * v # x acceleration from drag
    ay = -g - k * vy * v # y acceleration from gravity and drag
    return np.array([vx, vy, ax, ay])

def rk4_step(r, dt, m, R, rho, C, g):
    k1 = derivatives(r, m, R, rho, C, g)
    k2 = derivatives(r + 0.5*dt*k1, m, R, rho, C, g)
    k3 = derivatives(r + 0.5*dt*k2, m, R, rho, C, g)
    k4 = derivatives(r + dt*k3, m, R, rho, C, g)
    return r + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simulate cannonball trajectory with air resistance using RK4."
    )
    parser.add_argument(
        "--m", type=float, default=1.0,
        help="Mass of cannonball in kg (default: 1.0)"
    )
    parser.add_argument(
        "--R", type=float, default=0.08,
        help="Radius of cannonball in meters (default: 0.08)"
    )
    parser.add_argument(
        "--v0", type=float, default=100.0,
        help="Initial velocity in m/s (default: 100.0)"
    )
    parser.add_argument(
        "--angle", type=float, default=30.0,
        help="Launch angle in degrees (default: 30.0)"
    )
    parser.add_argument(
        "--dt", type=float, default=0.01,
        help="Time step in seconds (default: 0.01)"
    )
    args = parser.parse_args()

    # constants
    g   = 9.81 # gravity m/s^2
    rho = 1.22 # air density kg/m^3
    C   = 0.47 # drag coefficient for a sphere

    angle = np.radians(args.angle)
    vx0 = args.v0 * np.cos(angle) # initial x velocity
    vy0 = args.v0 * np.sin(angle) # initial y velocity

    r = np.array([0.0, 0.0, vx0, vy0]) # initial state [x, y, vx, vy]

    xs, ys = [r[0]], [r[1]] # store trajectory

    while r[1] >= 0: # simulate until cannonball hits ground
        r = rk4_step(r, args.dt, args.m, args.R, rho, C, g)
        xs.append(r[0])
        ys.append(r[1])

    print("Distance traveled:", round(xs[-1], 2), "m")

    masses = [0.5, 1.0, 5.0, 10.0, 50.0] # kg
    plt.figure()
    for m in masses:
        r = np.array([0.0, 0.0, vx0, vy0])
        xs_m, ys_m = [r[0]], [r[1]]
        while r[1] >= 0:
            r = rk4_step(r, args.dt, m, args.R, rho, C, g)
            xs_m.append(r[0])
            ys_m.append(r[1])
        plt.plot(xs_m, ys_m, label=str(m) + " kg")
        print("Mass", m, "kg - distance:", round(xs_m[-1], 2), "m")

    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Cannonball trajectories for different masses")
    plt.legend()
    plt.grid(True)
    plt.show()

###############################################################################################

def pendulum_derivs(r, l, g):
    theta, omega = r # unpack angle and angular velocity
    return np.array([omega, -(g/l) * np.sin(theta)])
 
def pendulum_rk4(r, dt, l, g):
    k1 = pendulum_derivs(r, l, g)
    k2 = pendulum_derivs(r + 0.5*dt*k1, l, g)
    k3 = pendulum_derivs(r + 0.5*dt*k2, l, g)
    k4 = pendulum_derivs(r + dt*k3, l, g)
    return r + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)
 
if __name__ == "__main__":
    parser2 = argparse.ArgumentParser(
        description="Nonlinear pendulum simulation with RK4 and animation."
    )
    parser2.add_argument(
        "--l", type=float, default=0.1,
        help="Pendulum arm length in meters (default: 0.1)"
    )
    parser2.add_argument(
        "--theta0", type=float, default=179.0,
        help="Initial angle in degrees (default: 179.0)"
    )
    parser2.add_argument(
        "--t_end", type=float, default=10.0,
        help="Simulation duration in seconds (default: 10.0)"
    )
    parser2.add_argument(
        "--dt", type=float, default=0.001,
        help="RK4 time step in seconds (default: 0.001)"
    )
    parser2.add_argument(
        "--fps", type=int, default=30,
        help="Animation frames per second (default: 30)"
    )
    args2 = parser2.parse_args()
 
    g   = 9.81
    l   = args2.l
    dt  = args2.dt
    theta0 = np.radians(args2.theta0)
 
    r = np.array([theta0, 0.0]) # start from omega = 0
    t = 0.0
    ts, thetas = [], []
 
    while t <= args2.t_end:
        ts.append(t)
        thetas.append(r[0])
        r = pendulum_rk4(r, dt, l, g)
        t += dt
 
   # plot theta(t)
    plt.figure()
    plt.plot(ts, np.degrees(thetas))
    plt.xlabel("t (s)")
    plt.ylabel("theta (degrees)")
    plt.title("Nonlinear Pendulum")
    plt.grid(True)
    plt.show()
 
    # animate
    steps_per_frame = max(1, int(1 / (args2.fps * dt))) # RK4 steps per animation frame
 
    r_anim = np.array([theta0, 0.0])
    frames = []
    t = 0.0
    while t <= args2.t_end:
        for _ in range(steps_per_frame): # several RK4 steps per frame
            r_anim = pendulum_rk4(r_anim, dt, l, g)
            t += dt
        frames.append(r_anim[0]) # store angle for this frame
 
    fig2, ax2 = plt.subplots(figsize=(4, 4))
    ax2.set_xlim(-l*1.5, l*1.5)
    ax2.set_ylim(-l*1.5, l*1.5)
    ax2.set_aspect('equal')
    ax2.grid(True)
 
    line, = ax2.plot([], [], 'k-', lw=2) # pendulum string
    bob,  = ax2.plot([], [], 'ko', ms=12) # pendulum bob
 
    def init_pend():
        line.set_data([], [])
        bob.set_data([], [])
        return line, bob
 
    def animate_pend(i):
        theta = frames[i]
        bx = l * np.sin(theta) # bob x position
        by = -l * np.cos(theta) # bob y position
        line.set_data([0, bx], [0, by])
        bob.set_data([bx], [by])
        return line, bob
 
    ani2 = animation.FuncAnimation(fig2, animate_pend, init_func=init_pend,
                                   frames=len(frames), interval=1000//args2.fps, blit=True)
    writergif2 = animation.PillowWriter(fps=args2.fps)
    ani2.save('pendulum.gif', writer=writergif2)
