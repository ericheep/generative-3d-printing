"""
window-noise-to-stl.py

Creates a 2D matrix made of windowed noise, and then
creates an STL or STLs suitable for slicing.
"""

from scipy import signal
from stl_chunker import stl_chunker

import numpy as np

size = 50
height = 25
maxRandom = 6

X = np.empty((size, size))

for row in range(size):
    noise = np.abs(np.random.normal(0, maxRandom, size))
    window = signal.blackmanharris(size) * height
    X[:, row] = window + noise

for col in range(size):
    noise = np.abs(np.random.normal(0, maxRandom, size))
    window = signal.blackmanharris(size) * height
    X[col, :] *= window + noise

# standardize
X = (X - np.mean(X)) / np.std(X)

# normalize
X = X - np.min(X)
X = X/np.max(X)

# chunk it
stls, coords = stl_chunker(X,
                           stl_length=size,
                           stl_width=size,
                           cube_size=7,
                           inner_wall_scale=0.95,
                           inner_wall_minimum=1,
                           height_scale=30.0,
                           invert_thickness=True)


# save our stls according to it's coordinate
for idx, stl in enumerate(stls):
    stl_filename = "windowed-noise" + "-" + str(coords[idx]) + ".stl"
    stl.save(stl_filename)
