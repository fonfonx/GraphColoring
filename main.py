from graph_class import *
from math import *
import matplotlib.pyplot as plt

# Parameters
# number of nodes
N = 100
# expected number of neighbors
c = 20
# number of colors
q = 5
# initial temperature
T0 = 10.0

# number of iterations
nbIter = 4000
# number of iterations for initial temperature
nbIterInit = 40

# plot curve or not
plot=True

# save coloration or not
save=False

# mat_file
mat_file="graph_adjacency_matrix.mat"

# mat file output (without extension)
out_file="coloration"


#### Decreasing functions ####
# Here are some decreasing functions that we can use
# Parameters: initial Temperature, actual Temperature, current number of iteration

# identity (no simulated annealing)
def identity(T):
    return T

# power decrease
def powerDecrease(T0,T,n):
    if (T>T0/2.0 and n%5==0) or (T>T0/10.0 and n%10==0) or (T>T0/100.0 and n%20==0):
        return T0/sqrt(n)
    return T

# linear decrease
def linearDecrease(T0,T,n):
    if (T > T0 / 2.0 and n % 5 == 0) or (T > T0 / 10.0 and n % 10 == 0) or (T > T0 / 100.0 and n % 20 == 0) and T>0.25:
        return T-0.25
    return T

# exponential decrease
def expoDecrease(T0,T,n):
    if T>T0/2.0 and n%5==0:
        return 0.85*T
    if T>T0/10.0 and n%10==0:
        return 0.85*T
    if T>T0/100.0 and n%20==0:
        return 0.85*T
    return T

# chosen decreasingFunction
def decreasingFunction(T0, T, n):
    return powerDecrease(T0,T,n)

# main function that we run
def test():
    G = Graph(N, q)
    G.erdosRenyi(c)
    #G.initFromFile(mat_file)
    G.randomColoration()
    T0 = G.initialTemperature(nbIterInit)
    print "Initial Temperature:",T0
    # G.vizualisation()
    G.metropolisAlgo(nbIter, T0, decreasingFunction, plot,save,out_file)

test()