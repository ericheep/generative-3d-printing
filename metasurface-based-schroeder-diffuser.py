"""
metasurface-based-schroeder-diffuser.py

Very experimental, creates an STL given a
design frequency and size.
"""

import numpy as np
from stl import mesh


def create_mesh(vertices):

    faces = np.array([[0, 3, 1], [1, 3, 2], [0, 4, 7],
                      [0, 7, 3], [4, 5, 6], [4, 6, 7],
                      [5, 1, 2], [5, 2, 6], [2, 3, 6],
                      [3, 7, 6], [0, 1, 5], [0, 5, 4]])

    cuboid = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

    # sets rect vertex locations
    for i, f in enumerate(faces):
        for j in range(3):
            cuboid.vectors[i][j] = vertices[f[j], :]

    return cuboid


def left_perimeter(x_index, y_index, unit_width, wall_width, z_offset, height):

    x_origin = x_index * unit_width
    y_origin = y_index * unit_width
    z_origin = z_offset
    perimeter_length = unit_width - wall_width

    x1, y1 = x_origin,              y_origin
    x2, y2 = x_origin + wall_width, y_origin
    x3, y3 = x_origin + wall_width, y_origin + perimeter_length
    x4, y4 = x_origin,              y_origin + perimeter_length
    z1, z2 = z_origin,              z_origin + height

    base_mesh_array = mesh_array(x1, y1, x2, y2, x3, y3, x4, y4, z1, z2)
    return create_mesh(base_mesh_array)


def top_perimeter(x_index, y_index, unit_width, wall_width, z_offset, height):

    x_origin = x_index * unit_width
    y_origin = y_index * unit_width
    z_origin = z_offset

    x1, y1 = x_origin + wall_width,       y_origin
    x2, y2 = x_origin + unit_width,       y_origin
    x3, y3 = x_origin + unit_width,       y_origin + wall_width
    x4, y4 = x_origin + wall_width,       y_origin + wall_width
    z1, z2 = z_origin,                    z_origin + height

    base_mesh_array = mesh_array(x1, y1, x2, y2, x3, y3, x4, y4, z1, z2)
    return create_mesh(base_mesh_array)


def right_perimeter(x_index, y_index, unit_width, wall_width, z_offset, height):

    x_origin = x_index * unit_width
    y_origin = y_index * unit_width
    z_origin = z_offset
    perimeter_length = unit_width - wall_width

    x1, y1 = x_origin + perimeter_length,   y_origin + wall_width
    x2, y2 = x_origin + unit_width,         y_origin + wall_width
    x3, y3 = x_origin + unit_width,         y_origin + unit_width
    x4, y4 = x_origin + perimeter_length,   y_origin + unit_width
    z1, z2 = z_origin,                      z_origin + height

    base_mesh_array = mesh_array(x1, y1, x2, y2, x3, y3, x4, y4, z1, z2)
    return create_mesh(base_mesh_array)


def bottom_perimeter(x_index, y_index, unit_width, wall_width, z_offset, height):

    x_origin = x_index * unit_width
    y_origin = y_index * unit_width
    z_origin = z_offset
    perimeter_length = unit_width - wall_width

    x1, y1 = x_origin,                      y_origin + perimeter_length
    x2, y2 = x_origin + perimeter_length,   y_origin + perimeter_length
    x3, y3 = x_origin + perimeter_length,   y_origin + unit_width
    x4, y4 = x_origin,                      y_origin + unit_width
    z1, z2 = z_origin,                      z_origin + height

    base_mesh_array = mesh_array(x1, y1, x2, y2, x3, y3, x4, y4, z1, z2)
    return create_mesh(base_mesh_array)


def create_perimeter(x_index, y_index, unit_width, wall_width, z_offset, height):
    left = left_perimeter(x_index, y_index, unit_width, wall_width, z_offset, height)
    top = top_perimeter(x_index, y_index, unit_width, wall_width, z_offset, height)
    right = right_perimeter(x_index, y_index, unit_width, wall_width, z_offset, height)
    bottom = bottom_perimeter(x_index, y_index, unit_width, wall_width, z_offset, height)

    return mesh.Mesh(np.concatenate([left.data, top.data, right.data, bottom.data])).data


def create_top(x_index, y_index, unit_width, wall_width, z_offset, height):
    wall_width = (unit_width - wall_width)/2

    left = left_perimeter(x_index, y_index, unit_width, wall_width, z_offset, height)
    top = top_perimeter(x_index, y_index, unit_width, wall_width, z_offset, height)
    right = right_perimeter(x_index, y_index, unit_width, wall_width, z_offset, height)
    bottom = bottom_perimeter(x_index, y_index, unit_width, wall_width, z_offset, height)

    return mesh.Mesh(np.concatenate([left.data, top.data, right.data, bottom.data])).data


def create_base(x_index, y_index, unit_width, height):
    x_origin = x_index * unit_width
    y_origin = y_index * unit_width
    z_origin = 0.0

    x1, y1 = x_origin,              y_origin
    x2, y2 = x_origin + unit_width, y_origin
    x3, y3 = x_origin + unit_width, y_origin + unit_width
    x4, y4 = x_origin,              y_origin + unit_width
    z1, z2 = z_origin,              height

    base_mesh_array = mesh_array(x1, y1, x2, y2, x3, y3, x4, y4, z1, z2)
    return create_mesh(base_mesh_array)


def mesh_array(x1, y1, x2, y2, x3, y3, x4, y4, z1, z2):

    return np.array([[x1, y1, z1],     # bottom back left
                     [x2, y2, z1],     # bottom back right
                     [x3, y3, z1],     # bottom front right
                     [x4, y4, z1],     # bottom front left
                     [x1, y1, z2],     # top back left
                     [x2, y2, z2],     # top back right
                     [x3, y3, z2],     # top front right
                     [x4, y4, z2]])    # trop front left


def QRS2D(N, M, f):
    qrs = [[0 for x in range(N)] for y in range(M)]

    for i in range(N):
        for j in range(M):
            qrs[i][j] = (i * i + j * j) % N

    return qrs


def create_diffuser(design_frequency, N, M, c):
    wavelength = c / design_frequency
    w = wavelength / 2.0
    cavity_height = wavelength / 20.0
    base_height = 1.0
    top_height = 1.0
    unit_width = w
    wall_width = 1.0
    qrs = QRS2D(N, M, w)

    # unit 2D list
    units = [[0 for x in range(M)] for y in range(N)]

    for i in range(N):
        for j in range(M):
            resonator_width = np.random.randint(0, unit_width/2)
            base = create_base(i, j, w, base_height)
            perimeter = create_perimeter(i, j, unit_width, wall_width, base_height, cavity_height)
            h = (w * qrs[i][j]) / (2 * N)
            top = create_top(i, j, unit_width, h, cavity_height + base_height, top_height)

            units[i][j] = np.concatenate([base.data, perimeter.data, top.data]).data

    unit_list = []

    for i in range(N):
        for j in range(M):
            unit_list.append(units[i][j])

    stl = mesh.Mesh(np.concatenate(unit_list))
    stl.save("test.stl")


# rows and cols
N = 7
M = 7
design_frequency = 6850.0
c = 343.0 * 1000.0

create_diffuser(design_frequency, N, M, c)

