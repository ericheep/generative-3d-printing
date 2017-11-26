"""
noise-cube.py
"""

import numpy as np
import matplotlib.pyplot as plt

mu, sigma = 0, 1


def gaussian(x, mu, sig):
        return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

plt.plot(gaussian(np.linspace(-3.5, 3.5, 100), mu, sigma))
plt.show()
