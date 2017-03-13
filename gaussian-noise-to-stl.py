"""
guassian-noise-to-stl.py

Creates a 2D matrix made of guassian noise, and then
creates an STL or STLs suitable for slicing.
"""

# import stl_chunker
import numpy as np
import matplotlib.pyplot as plt

mean = (15, 15)
cov = [[1, 0], [0, 1]]

# X = np.random.multivariate_normal(mean, cov, (30,30))
X = np.random.randn(30)
print(X.shape)

plt.plot(X)
plt.subplot(211)
# plt.imshow(X[:, :], interpolation="nearest", origin="lower", cmap="viridis")
# plt.subplot(212)
# plt.imshow(X[:, :, 1], interpolation="nearest", origin="lower", cmap="viridis")
plt.show()
