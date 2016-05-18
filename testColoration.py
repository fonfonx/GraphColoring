from graph_class import *
from math import *

# Parameters
# number of nodes
N = 10
# expected number of neighbors
c = 20
# number of colors
d = 5
# initial temperature
T0 = 40.0

# number of iterations
nbIter = 4000
# number of iterations for initial temperature
nbIterInit = 40

# plot curve or not
plot=True

# dat_file
dat_file="graph_adjacency_matrix.mat"


#### Decreasing functions ####
# Here are some decreasing functions that we can use
# Parameters: initial Temperature, actual Temperature, current number of iteration

# identity (no simulated annealing)
def identity(T):
    return T


# power decrease
def powerDecrease(T0, n, gamma):
    return T0 / (n ** gamma)


def logDecrease(T0, n):
    return T0 / log(n + 1)


def linearDecrease(T, alpha, n, modulo):
    if n % modulo == 0 and T > alpha:
        T -= alpha
    return T


def expoDecrease(T, alpha, n, modulo, Tmin):
    if n % modulo == 0 and T > Tmin:
        T *= alpha
    return T
    

# decreasingFunction
def decreasingFunction(T0, T, n):
    # return identity(T)
    # if n%10>=0 and n<=100:
    #     return powerDecrease(T0, n, 1.0)
    # if n>=100 and T>0.1 and n%10>=0:
    #     return powerDecrease(T0,n,0.6)
    # return T
    return expoDecrease(T,0.95,n,10,0.1)



G = Graph(N, d)
#G.erdosRenyi(c)
G.initFromFile(dat_file)
G.randomColoration()
T0 = G.initialTemperature(nbIterInit)
print "Initial Temperature:",T0
# G.vizualisation()
G.metropolisAlgo(nbIter, T0, decreasingFunction, plot)