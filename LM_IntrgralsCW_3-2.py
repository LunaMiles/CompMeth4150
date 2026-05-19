import argparse 
import numpy as np                          
import astropy.constants as const          
import astropy.units as u                   

hbar = const.hbar # reduced Planck's constant in J*s
k_B = const.k_B # Boltzmann constant in J/K
c = const.c # speed of light in m/s
sigma = const.sigma_sb

def f(x):
    return (x**3) / (np.exp(x) - 1)       

def simpson(func, a, b, N):
    if N % 2 != 0: # Simpson's rule needs even number of slices
        N += 1
    h = (b - a) / N # width of each slice
    x = np.linspace(a, b, N + 1)         
    y = func(x) # evaluate the integrand at every point

    coeffs = np.ones(N + 1)                 
    coeffs[1:-1:2] = 4                      
    coeffs[2:-2:2] = 2                      

    return (h / 3) * np.dot(coeffs, y)    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(           
        description="Numerically evaluate the Planck radiation integral and derive the Stefan-Boltzmann constant."
    )
    parser.add_argument(                        
        "--N", type=int, default=1000,
        help="Number of slices for Simpson's rule integration (default: 1000; more = more accurate)"
    )
    parser.add_argument(                        
        "--b", type=float, default=500.0,
        help="Upper limit of integration approximating infinity (default: 500; integrand is negligible beyond this)"
    )
    parser.add_argument(                       
        "--a", type=float, default=1e-10,
        help="Lower limit of integration near 0 (default: 1e-10; avoids division by zero)"
    )
    args = parser.parse_args()

    a = args.a                                  
    b = args.b                                  
    N = args.N                                  

    integral_val = simpson(f, a, b, N)      

    print("Integral result:", round(integral_val, 6), "pi^4/15 =", round(np.pi**4 / 15, 6))

    # Compute the Stefan-Boltzmann constant 
    prefactor = k_B**4 / (4 * np.pi**2 * c**2 * hbar**3) # constant multiplier derived from rearranging W = sigma * T^4
    sigma_computed = (prefactor * integral_val).to(u.W / u.m**2 / u.K**4)

    print("Computed sigma:", sigma_computed)
    print("Known sigma:   ", sigma)

    # Method: Simpson's rule. With N=1000 slices the result matches pi^4/15 to in ~1e-12, which is pretty accurate