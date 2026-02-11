''' A spaceship travels from Earth in a straight line 
at relativistic speed v to another planet x light 
years away. Write a program to ask the user for the 
value of x and the speed v as a fraction of the speed 
of light c, then print out the time in years that the 
spaceship takes to reach its destination (a) in the 
rest frame of an observer on Earth and (b) as 
perceived by a passenger on board the ship. 
Use your program to calculate the answers for a 
planet 10 light years away with v = 0.99c. '''

import sys
import numpy as np 

# special reletivaty
def spec_rel_sysargv():
    x = float(sys.argv[1]) # light years 
    v = float(sys.argv[2]) # %speed of light (m/s)

    def gamma(v):
        # Lorentz factor
        gamma_lf = 1 / np.sqrt(1 - v**2)
        return gamma_lf

    time = x / v # on earth
    tau = time / gamma(v) # on space ship

    print(time, " years Earth time.")
    print(tau, " years on the Ship.")

if __name__ == "__main__" : 
    spec_rel_sysargv()

