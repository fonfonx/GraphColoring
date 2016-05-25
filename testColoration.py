from graph_class import *
from math import *
import matplotlib.pyplot as plt

# Parameters
# number of nodes
N = 100
# expected number of neighbors
c = 20
# number of colors
d = 7
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
inputXav="mygraph.mat"

# mat file output (without extension)
out_file="coloration"


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

def mydecrease(T0,T,n):
    if n<=10:
        return T0
    if n>10:
        if n%(10+n/100)==0:
            #return 0.95*T
            return T0/sqrt(n)
    return T


# decreasingFunction
def decreasingFunction(T0, T, n):
    #return identity(T)
    #return expoDecrease(T,0.85,n,5,0.1)
    #return powerDecrease(T0,n,0.5)
    #return mydecrease(T0,T,n)
    return expDecrease3(T0,T,n)

def linDecrease(T0,T,n):
    return linearDecrease(T,0.25,n,5)

def expDecrease(T0,T,n):
    return expoDecrease(T,0.85,n,5,0.1)

def expDecrease2(T0,T,n):
    return expoDecrease(T,0.85,n,10,0.1)

def expDecrease3(T0,T,n):
    if T>T0/2.0 and n%5==0:
        return 0.85*T
    if T>T0/10.0 and n%10==0:
        return 0.85*T
    if T>T0/100.0 and n%20==0:
        return 0.85*T
    return T

def powDecrease(T0,T,n):
    return powerDecrease(T0,n,0.5)

def powDecrease2(T0,T,n):
    if (T>T0/2.0 and n%5==0) or (T>T0/10.0 and n%10==0) or (T>T0/100.0 and n%20==0):
        return T0/sqrt(n)
    return T

def linDecrease2(T0,T,n):
    if (T > T0 / 2.0 and n % 5 == 0) or (T > T0 / 10.0 and n % 10 == 0) or (T > T0 / 100.0 and n % 20 == 0) and T>0.25:
        return T-0.25
    return T

def test():
    G = Graph(N, d)
    #G.erdosRenyi(c)
    G.initFromFile("G4.mat")
    G.randomColoration()
    #G.setColorationFromMat("coloration_50.mat")
    T0 = G.initialTemperature(nbIterInit)
    print "Initial Temperature:",T0
    # G.vizualisation()
    G.metropolisAlgo(nbIter, T0, decreasingFunction, plot,save,out_file)

def test_moy(graph,N,d):
    G=Graph(N,d)
    G.initFromFile(graph)
    G.randomColoration()
    initColFile=G.writeMat("initcol")
    print G.coloration
    print "lol"
    T0=G.initialTemperature(nbIterInit)
    print T0
    tabmin=np.zeros(3)
    dec=[linDecrease2, expDecrease3,powDecrease2]
    for method in range(3):
        tab=np.zeros(nbIter+1)
        minmoy=0.0
        for k in range(10):
            G.setColorationFromMat(initColFile)
            minH,tabH=G.metropolisAlgo(nbIter,T0,dec[method],False,False,out_file)
            tab+=tabH
            minmoy+=minH
        tab=tab/10.0
        minmoy=minmoy/10.0
        tabmin[method]=minmoy
        print "method,min",method,minmoy
        #plt.plot(np.linspace(0,nbIter,nbIter+1),tab)
    print tabmin
    #plt.show()


def competition(input, nbNodes, nbColors):
    G=Graph(nbNodes,nbColors)
    G.initFromFile(input)
    H=1000
    while H>0:
        G.randomColoration()
        T0=G.initialTemperature(nbIterInit)
        G.metropolisAlgo(nbIter, T0, decreasingFunction, False, False,out_file)
        actH=G.hamiltonian()
        if actH<H:
            H=actH
            print H
            G.writeMat(out_file)
        print "actual best:",H

def valeurs_moy():
    G=Graph(N,d)
    G.initFromFile(inputXav)
    rep=0
    for k in range(10):
        G.randomColoration()
        minH,tabH=G.metropolisAlgo(nbIter,T0,decreasingFunction,False,False,out_file)
        rep+=minH
    print "average min H:",rep/(10.0)

def Hmin(q):
    taby=[]
    tabx=[]
    for c in range(1,N,3):
        print c
        val=0
        for k in range(4):
            G = Graph(N, q)
            G.erdosRenyi(c)
            G.randomColoration()
            T0=G.initialTemperature(nbIterInit)
            val+=G.metropolisAlgo(nbIter,T0,decreasingFunction,False,False,out_file)[0]
        taby.append(val/4.0)
        tabx.append(c)
    print tabx,taby
    plt.plot(tabx,taby)
    plt.show()


#competition(mat_file,100,3)
#test()
#valeurs_moy()

#Hmin(5)

test_moy("G4.mat",100,7)
