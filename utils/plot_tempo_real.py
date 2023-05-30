import matplotlib.pyplot as plt
import numpy as np

plt.axis([0, 10, 0, 1])

x = np.arange(0, 1000, np.pi / 10)
y = np.sin(x)

for i in range(90):
    # plt.ylim((-1, 1))
    plt.scatter(x[i: i+10], y[i: i+10])
    plt.pause(0.00001)
    plt.clf()

plt.show()