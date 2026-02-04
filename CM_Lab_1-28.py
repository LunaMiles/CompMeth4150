import sys
def time_sysargv():
    g = 9.81 # m/s
    h = float(sys.argv[2]) # enter 100 meters # everything in sys argv is a string
    t = ((2*h)/g)**0.5

    print(t)

if __name__ == "__main__" : 
    time_sysargv()