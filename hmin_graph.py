import matplotlib.pyplot as plt
import numpy as np

tabx=[1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49]
taby3=[0.0, 2.75, 19.75, 44.75, 82.5, 118.75, 153.5, 195.5, 236.5, 267.5, 319.0, 361.25, 411.0, 440.0, 503.25, 539.5, 573.75]
taby5= [0.0, 0.0, 0.0, 1.5, 9.75, 24.25, 42.0, 57.25, 77.25, 95.5, 123.0, 138.75, 164.0, 197.75, 213.0, 240.5, 272.75]
taby7=[0.0, 0.0, 0.0, 0.0, 0.25, 4.75, 9.75, 13.25, 27.75, 40.75, 53.5, 66.5, 77.0, 89.25, 106.75, 128.25, 145.5]


plt.plot(tabx,taby3)
plt.plot(tabx,taby5)
plt.plot(tabx,taby7)
plt.show()


