"""
stl_chunker.py

Accepts a 2D matrix and returns an STL or multiple STLs
as a matrix of cubes whose height and thickness is based
on the values of the the 2D matrix.
"""

import numpy as np

from stl import mesh


def left_vertices(x_origin, y_origin, size, width, value):
    """ Creates the left wall of the cube.
    """

    x_origin = x_origin * size
    y_origin = y_origin * size

    x1, y1, = x_origin,         y_origin
    x2, y2, = x_origin + width, y_origin
    x3, y3, = x_origin + width, y_origin + (size - width)
    x4, y4, = x_origin,         y_origin + (size - width)

    return np.array([[x1, y1, 0.0],     # bottom back left
                     [x2, y2, 0.0],     # bottom back right
                     [x3, y3, 0.0],     # bottom front right
                     [x4, y4, 0.0],     # bottom front left
                     [x1, y1, value],   # top back left
                     [x2, y2, value],   # top back right
                     [x3, y3, value],   # top front right
                     [x4, y4, value]])  # trop front left


def right_vertices(x_origin, y_origin, size, width, value):
    """ Creates the left wall of the cube.
    """

    x_origin = x_origin * size
    y_origin = y_origin * size

    x1, y1, = x_origin + (size - width),    y_origin + width
    x2, y2, = x_origin + size,              y_origin + width
    x3, y3, = x_origin + size,              y_origin + size
    x4, y4, = x_origin + (size - width),    y_origin + size

    return np.array([[x1, y1, 0.0],     # bottom back left
                     [x2, y2, 0.0],     # bottom back right
                     [x3, y3, 0.0],     # bottom front right
                     [x4, y4, 0.0],     # bottom front left
                     [x1, y1, value],   # top back left
                     [x2, y2, value],   # top back right
                     [x3, y3, value],   # top front right
                     [x4, y4, value]])  # trop front left


def bottom_vertices(x_origin, y_origin, size, width, value):
    """ Creates the bottom wall of the cube.
    """

    x_origin = x_origin * size
    y_origin = y_origin * size

    x1, y1, = x_origin + width, y_origin
    x2, y2, = x_origin + size,  y_origin
    x3, y3, = x_origin + size,  y_origin + width
    x4, y4, = x_origin + width, y_origin + width

    return np.array([[x1, y1, 0.0],     # bottom back left
                     [x2, y2, 0.0],     # bottom back right
                     [x3, y3, 0.0],     # bottom front right
                     [x4, y4, 0.0],     # bottom front left
                     [x1, y1, value],   # top back left
                     [x2, y2, value],   # top back right
                     [x3, y3, value],   # top front right
                     [x4, y4, value]])  # trop front left


def top_vertices(x_origin, y_origin, size, width, value):
    """ Creates the bottom wall of the cube.
    """

    x_origin = x_origin * size
    y_origin = y_origin * size

    x1, y1, = x_origin,                     y_origin + (size - width)
    x2, y2, = x_origin + (size - width),    y_origin + (size - width)
    x3, y3, = x_origin + (size - width),    y_origin + size
    x4, y4, = x_origin,                     y_origin + size

    return np.array([[x1, y1, 0.0],     # bottom back left
                     [x2, y2, 0.0],     # bottom back right
                     [x3, y3, 0.0],     # bottom front right
                     [x4, y4, 0.0],     # bottom front left
                     [x1, y1, value],   # top back left
                     [x2, y2, value],   # top back right
                     [x3, y3, value],   # top front right
                     [x4, y4, value]])  # trop front left


def create_wall(vertices):
    """ Creates a wall given a matrix of vertices
    """

    faces = np.array([[0, 3, 1], [1, 3, 2], [0, 4, 7],
                      [0, 7, 3], [4, 5, 6], [4, 6, 7],
                      [5, 1, 2], [5, 2, 6], [2, 3, 6],
                      [3, 7, 6], [0, 1, 5], [0, 5, 4]])

    # creates a cuboid
    cuboid = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

    # sets rect vertex locations
    for i, f in enumerate(faces):
        for j in range(3):
            cuboid.vectors[i][j] = vertices[f[j], :]

    return cuboid


def create_hollow_cube(x_origin, y_origin, size, width, value):
    left_wall = create_wall(left_vertices(x_origin, y_origin, size, width, value))
    right_wall = create_wall(right_vertices(x_origin, y_origin, size, width, value))
    bottom_wall = create_wall(bottom_vertices(x_origin, y_origin, size, width, value))
    top_wall = create_wall(top_vertices(x_origin, y_origin, size, width, value))

    return mesh.Mesh(np.concatenate([left_wall.data,    right_wall.data,
                                     bottom_wall.data,  top_wall.data])).data


def create_stls(X, x_range, y_range):

    stls = []
    coords = []

    x_length, y_length = len(X[0]), len(X)

    for y in range(int(np.ceil(y_length/y_range))):
        for x in range(int(np.ceil(x_length/x_range))):
            block = []

            for row in X[y * y_range:(y + 1) * y_range]:
                for element in row[x * x_range:(x + 1) * x_range]:
                    block.append(element)

            stls.append(mesh.Mesh(np.concatenate(block)))
            coords.append(str(x) + '-' + str(y))

    return stls, coords


def stl_chunker(X, stl_length=None, stl_width=None, cube_size=10,
                inner_wall_scale=0.5, height_scale=10.0):
    # hollow cube 2D list
    hollow_cubes = [[0 for x in range(X.shape[1])] for y in range(X.shape[0])]

    # creating our cubes
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):

            wall_width = (X[i, j] * cube_size * inner_wall_scale/2.0)
            wall_height = (X[i, j] * height_scale)

            if wall_width < 0.5:
                wall_width = 0.5

            if wall_height < 0.5:
                wall_height = 0.5

            hollow_cubes[i][j] = create_hollow_cube(i, j, cube_size,
                                                    wall_width, wall_height)

    # creates our stls according to a given length
    return create_stls(hollow_cubes, stl_length, stl_width)
