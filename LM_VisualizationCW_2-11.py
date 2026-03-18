import argparse 
import numpy as np 
import matplotlib.pyplot as plt 

def deltoid(n=2000):
    # 0 <= theta < 2pi
    theta = np.linspace(0, 2*np.pi, n)
    x = 2*np.cos(theta) + np.cos(2*theta)
    y = 2*np.sin(theta) - np.sin(2*theta)
    return x, y

def galilean_spiral(n=4000):
    # r = theta^2, 0 <= theta <= 10pi
    theta = np.linspace(0, 10*np.pi, n)
    r = theta**2
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def feys_function(n=12000):
    # r = e^{cosθ} - 2cos(4θ) + sin^5(θ/12), 0 <= θ <= 24pi
    theta = np.linspace(0, 24*np.pi, n)
    r = np.exp(np.cos(theta)) - 2*np.cos(4*theta) + (np.sin(theta/12))**5
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def plot_xy(x, y, title, color=None):
    plt.figure()
    plt.plot(x, y, color=color)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(title)
    plt.axis("equal")  # makes the curves not look squished
    plt.grid(True, alpha=0.3)

# deltoid
x, y = deltoid()
plot_xy(x, y, "Deltoid Curve", color="red")
plt.show()

# galilean spiral
x, y = galilean_spiral()
plot_xy(x, y, "Galilean Spiral", color="blue")
plt.show()

# fey's function
x, y = feys_function()
plot_xy(x, y, "Fey's Function", color="green")
plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Visualization Classwork: Luna Miles',
                    description='Created functions to plot the Deltoid, Galilean Spiral, and Feys, and a function to plot each graph.'
    )

    args = parser.parse_args()


