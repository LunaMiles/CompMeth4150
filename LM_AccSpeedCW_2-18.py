import argparse 
import numpy as np 
import matplotlib.pyplot as plt 

def f(x):
    eff = x*(x-1)
    return eff

x = 1 # log scale
delta = 10e-2
g = (f(x + delta) - f(x)) / delta 
print("g: " , g) # 1.100000000000001
# analytically = 1.01
a = 1.01
print("a: " , a)

# plot error as a function of delta or plot result of calculation as a function of delta?

'''
loop to plot each calculation for delta values using
the range to update delta
''' 
plt.figure()
delta_vals = []
derivs = []
for N in range (-2, -14, -2):
    delta = 10**N
    g = (f(x + delta) - f(x)) / delta 

    delta_vals.append(delta)
    derivs.append(g)

plt.scatter(np.log(derivs) , delta_vals)
plt.xscale("log")
plt.yscale("log")
plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Deltoid Curve")
    parser.add_argument("f", 
                        type = function, # error, but isn't it technically a type?
                        help = "Defines the function f(x) for this assignment")
    parser.add_argument("g", 
                        type = float,
                        help = "Calculates the derivative of f(x)")
    parser.add_argument("delta", 
                        type = float,
                        help = "Defines delta")
    parser.add_argument("a",
                        type = float,
                        help = "Is the analytic calculation of f(x)")
    parser.add_argument("delta_vals", 
                        type = list,
                        help = "Lists all values of delta as per assignment")
    parser.add_argument("derivs", 
                        type = list,
                        help = "Lists all derivatives of g using delta_vals")

    args = parser.parse()
    


    
    




