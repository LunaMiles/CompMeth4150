# Status: Completed, not submitted
import argparse
import numpy as np
import matplotlib.pyplot as plt
from numpy import zeros

def dft(y):
    N = len(y)
    c = zeros(N//2+1, complex)
    for k in range(N//2+1):
        for n in range(N):
            c[k] += y[n] * np.exp(-2j*np.pi*k*n/N)
    return c

def square_wave(N):
    y = np.zeros(N)
    y[:N//2] = 1.0 # first half is 1, second half is 0
    return y

def sawtooth(N):
    return np.arange(N, dtype=float) # y_n = n

def modulated_sine(N):
    n = np.arange(N)
    return np.sin(np.pi * n / N) * np.sin(20 * np.pi * n / N)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Discrete Fourier transforms of simple periodic functions."
    )
    parser.add_argument(
        "--N", type=int, default=200,
        help="Number of sample points (default: 200)"
    )
    parser.add_argument(
        "--wave", type=str, default="all", choices=["square", "sawtooth", "modulated", "all"],
        help="Which wave to plot (default: all)"
    )
    args = parser.parse_args()

    N = args.N

    waves = {
        "square":    square_wave(N),
        "sawtooth":  sawtooth(N),
        "modulated": modulated_sine(N),
    }

    to_plot = waves.keys() if args.wave == "all" else [args.wave]

    fig, axes = plt.subplots(len(list(to_plot)), 2, figsize=(12, 4 * len(list(to_plot))))
    if len(list(to_plot)) == 1:
        axes = [axes] # keep consistent indexing for single plot

    for ax_row, name in zip(axes, to_plot):
        y = waves[name]
        c = dft(y)                      
        amps = np.abs(c) # amplitude of each frequency component

        # to see the original function
        ax_row[0].plot(y)
        ax_row[0].set_title(name + " (time domain)")
        ax_row[0].set_xlabel("n")

        # to see the amplitude of the function
        ax_row[1].plot(amps)
        ax_row[1].set_title(name + " (frequency domain)")
        ax_row[1].set_xlabel("k")
        ax_row[1].set_ylabel("amplitude")

    plt.show()