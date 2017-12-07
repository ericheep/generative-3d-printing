"""
guassian-noise-to-stl.py

Creates a 2D matrix made of guassian noise, and then
creates an STL or STLs suitable for slicing.
"""

# import stl_chunker
import numpy as np
import matplotlib.pyplot as plt

mean = 15
cov = [1, 0]

X = np.random.multivariate_normal(mean, cov, (4))
print(X.shape)

plt.subplot(211)
plt.imshow(X[:, :, 0], interpolation="nearest", origin="lower", cmap="viridis")
plt.subplot(212)
plt.imshow(X[:, :, 1], interpolation="nearest", origin="lower", cmap="viridis")
plt.show()
