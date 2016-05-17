from graph_class import *
from math import *

# Parameters
# number of nodes
N = 100
# expected number of neighbors
c = 20
# number of colors
d = 5
# initial temperature
T0 = 40.0

# number of iterations
nbIter = 3000
# number of iterations for initial temperature
nbIterInit = 40

# plot curve
plot=False


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


def expoDecrease(T, alpha, n, modulo, Tmin):
    if n % modulo == 0 and T > Tmin:
        T *= alpha


# decreasingFunction
def decreasingFunction(T0, T, n):
    # return identity(T)
    return powerDecrease(T0, n, 0.5)


G = Graph(N, d)
G.erdosRenyi(c)
G.randomColoration()
T0 = G.initialTemperature(nbIterInit)
print "Initial Temperature:",T0
# G.vizualisation()
G.metropolisAlgo(nbIter, T0, decreasingFunction, plot)
