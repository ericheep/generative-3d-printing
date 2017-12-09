"""
image-to-stl.py

Takes an image, downsamples into an appropriate size, and then
creates an STL suitable for slicing.
"""

import os
import stl_chunker
import numpy as np

from scipy import misc


def luma_greyscale(X):
    r, g, b = 0.21, 0.72, 0.07
    return (X[:, :, 0] * r + X[:, :, 1] * g + X[:, :, 2] * b)/3.0


def cie_y_greyscale(X):
    CIE = np.array([[0.49,     0.31,       0.20],
                    [0.17697,  0.81240,    0.01063],
                    [0.00,     0.01,       0.99]])

    return np.dot(X, CIE)[:, :, 1]


def image_to_stl(filepath, x_resize=None, y_resize=None, stl_length=None, stl_width=None,
                 cube_size=10, inner_wall_scale=0.5, inner_wall_minimum=0.1, height_scale=10.0,
                 greyscale="cie_y", invert_values=False, invert_thickness=False):
    """ Converts an image file into an STL.

    This allows for generative 3D printable STLs to be produced from any image.

    Parameters
    ----------
    filepath : string
        Image filepath.
    x_resize : int
        Resizes the image to this "pixel" width, the y axis scales along with it.
    y_resize : int
        Resizes the image to this "pixel" height, the x axis scales along with it.
        (NOTE: If both x_resize and y_resize are set, the x_resize will overwrite the y_resize)
    stl_length: int
        If not None, breaks up the image into multple STL files of the given width.
    stl_width: int
        If not None, breaks up the image into multple STL files of the given height.
    cube_length : float
        The width and height of each cube created from a pixel of the image.
    inner_wall_scale : float
        The possible depth of each inner wall.
    inner_wall_minimum : float
        The minimum wall thickness of each cube.
    height_scale : flaot
        The possible height of each cube.
    greyscale : string
        The type of greyscale conversion to use. ("cie_y", "luma")
    """

    # reads image
    X = misc.imread(filepath)

    # for pngs and those pesky alpha layers
    if X.shape[2] > 3:
        X = X[:, :, :3]

    # resizing
    percent_resize = None
    if x_resize is not None:
        percent_resize = x_resize/X.shape[1]
    elif y_resize is not None:
        percent_resize = y_resize/X.shape[0]

    if percent_resize is not None:
        X = misc.imresize(X.astype('float32'), percent_resize, 'nearest')

    # changing length if breaking up image into multiple STL files
    if stl_length is None:
        stl_length = X.shape[1]
    if stl_width is None:
        stl_width = X.shape[0]

    # greyscale conversions
    if greyscale == "cie_y":
        X = cie_y_greyscale(X)
    elif greyscale == "luma":
        X = luma_greyscale(X)

    # standardize
    X = (X - np.mean(X)) / np.std(X)

    # normalize
    X = X - np.min(X)
    X = X/np.max(X)

    if invert_values:
        X = (X * -1.0) + 1.0

    stls, coords = stl_chunker.stl_chunker(X, stl_length=stl_length, stl_width=stl_width,
                                           cube_size=cube_size, inner_wall_scale=inner_wall_scale,
                                           inner_wall_minimum=inner_wall_minimum,
                                           height_scale=height_scale,
                                           invert_thickness=invert_thickness)

    # cuts off extension
    filename, _ = os.path.splitext(filepath)

    # save our stls according to it's coordinate
    for idx, stl in enumerate(stls):
        stl_filename = filename + "-" + str(coords[idx]) + ".stl"
        stl.save(stl_filename)


image_to_stl("images/marilyn.png",
             x_resize=144,
             cube_size=8,
             inner_wall_scale=0.95,
             inner_wall_minimum=1.5,
             height_scale=35.0,
             # stl_length=None,
             # stl_width=None,
             stl_length=48,
             stl_width=47,
             invert_values=True,
             invert_thickness=True)
