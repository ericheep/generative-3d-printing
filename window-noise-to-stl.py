"""
window-noise-to-stl.py

Creates a 2D matrix made of windowed noise, and then
creates an STL or STLs suitable for slicing.
"""

from scipy import signal
from stl_chunker import stl_chunker

import numpy as np

# 210mm, so let's do 240 (24 * 10mm)
width = 24
# 332mm, so let's do 360 (36 * 10mm)
height = 36

piecesWide = 3
piecesHigh = 3

depth = 50
maxNoise = 6

maxValue = 1.00
minValue = 0.05
rangeValue = maxValue - minValue

maxRandom = 0.80
minRandom = 0.50
rangeRandom = maxRandom - minRandom

R = np.random.rand(width, height)
R = R * rangeRandom + minRandom

W = np.empty((width, height))

for row in range(height):
    noise = np.abs(np.random.normal(0, maxNoise, width))
    window = signal.blackman(width) * depth
    W[:, row] = window + noise

for col in range(width):
    noise = np.abs(np.random.normal(0, maxNoise, height))
    window = signal.blackman(height) * depth
    W[col, :] *= window + noise

# standardize
W = (W - np.mean(W)) / np.std(W)

# normalize
W = W - np.min(W)
W = W/np.max(W)

W = W * rangeValue + minValue

X = np.empty((width, height, 2))
X[:, :, 0] = W
X[:, :, 1] = R

# chunk it
stls, coords = stl_chunker(X,
                           stl_length=int(height/piecesWide),
                           stl_width=int(width/piecesHigh),
                           cube_size=10,
                           inner_wall_scale=0.95,
                           inner_wall_minimum=1,
                           height_scale=depth,
                           invert_thickness=True)


# save our stls according to it's coordinate
for idx, stl in enumerate(stls):
    stl_filename = "windowed-noise" + "-" + str(coords[idx]) + ".stl"
    stl.save(stl_filename)
