#!/usr/bin/env python

"""yuvcube: A YUV Cube creator."""


import argparse
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib.pyplot as plt
import sys

import yuvconv
import yuvcommon


TV_LIST = ["sdtv", "hdtv"]
FUNCTIONS = ["rgb2yuv", "yuv2rgb"]

default_values = {
    "debug": 0,
    "clip": True,
    "num_vertices": 2,
    "tv_type": "sdtv",
    "convert_function": None,
    "func": "yuv2rgb",
}


# https://stackoverflow.com/questions/44881885/python-draw-parallelepiped/49766400
def add_cube_sides(debug, ax, xs, ys, zs, color="k", linestyle="solid", **kwargs):
    # ax.scatter3D(xs, ys, zs, color=color)
    # r = [-1,1]
    # X, Y = np.meshgrid(r, r)
    # plot vertices
    verts = []
    d = int(round(len(xs) ** (1 / 3.0)))
    # ^ Y
    # |
    # |        d^3-d^2+d-1   d^3-1
    # |           +------------+
    # |         / :          / |
    # |       /   :        /   |
    # |     /     :      /     |
    # |   +------------+ d^3-d |
    # |   |d^3-d^2|    |       |
    # |   |       +""""|"""""""+ d^2-1
    # |   |     / d-1  |     /
    # |   |   /        |   /
    # |   | /          | /
    # |   +------------+
    # |   0         d^2-d  (d^2 - 1 - (d-1))
    # +--------------------------------------> X
    index_list = (
        0,
        d - 1,
        d**2 - 1,
        d**2 - d,
        d**3 - d**2,
        d**3 - d**2 + d - 1,
        d**3 - 1,
        d**3 - d,
    )
    Z = []
    for i, index in enumerate(index_list):
        Z.append([xs[index], ys[index], zs[index]])
        if debug > 0:
            print("Z[%i]: (%i, %i, %i)" % (i, Z[i][0], Z[i][1], Z[i][2]))

    # plot sides
    # list of sides' polygons of figure
    verts = [
        [Z[0], Z[1], Z[2], Z[3]],
        [Z[4], Z[5], Z[6], Z[7]],
        [Z[0], Z[1], Z[5], Z[4]],
        [Z[2], Z[3], Z[7], Z[6]],
        [Z[1], Z[2], Z[6], Z[5]],
        [Z[4], Z[7], Z[3], Z[0]],
    ]
    ax.add_collection3d(
        Line3DCollection(verts, linewidths=2, facecolors=color, **kwargs)
    )
    # add an arrow from (0, 0, 0) to (255, 255, 255)
    ax.quiver(
        Z[0][0],
        Z[0][1],
        Z[0][2],
        Z[6][0] - Z[0][0],
        Z[6][1] - Z[0][1],
        Z[6][2] - Z[0][2],
        color=color,
        linestyle=linestyle,
    )


def generate_equidistant_list(vmin, vmax, numv):
    # f(x) = a * x + b
    # f(0) = a * 0 + b = b = vmin
    b = vmin
    # f(numv - 1) = a * (numv - 1) + b = vmax
    a = 1.0 * (vmax - b) / (numv - 1)
    return [int(a * x + b) for x in range(numv)]


def generate_cube(line):
    xs, ys, zs = [], [], []
    for x in line:
        for y in line:
            for z in line:
                xs.append(x)
                ys.append(y)
                zs.append(z)
    return xs, ys, zs


def convert_cube(xs, ys, zs, convert_function):
    xos, yos, zos = [], [], []
    for x, y, z in zip(xs, ys, zs):
        xo, yo, zo = convert_function(x, y, z)
        xos.append(xo)
        yos.append(yo)
        zos.append(zo)
    return xos, yos, zos


def remove_valid_elements(xs, ys, zs, reverse=False):
    i = 0
    xos, yos, zos = [], [], []
    for x, y, z in zip(xs, ys, zs):
        if x >= 0 and x < 256 and y >= 0 and y < 256 and z >= 0 and z < 256:
            inside_cube = True
        else:
            inside_cube = False
        if inside_cube ^ reverse:
            print("removing value x: %i, y: %i, z: %i" % (x, y, z))
            i += 1
            continue
        else:
            xos.append(x)
            yos.append(y)
            zos.append(z)
    print("--> removed %i/%i values" % (i, len(xs)))
    return xos, yos, zos


def clip_value(x, minx=0, maxx=255):
    return minx if x < minx else (maxx if x > maxx else x)


def show_cube_plot(options):
    if not options.saturation:
        yuvcommon.DO_NOT_NORMALIZE = True

    # get conversion functions
    if options.convert_function is not None:
        convert_rgb2yuv = yuvconv.CONVERSION_FUNCTIONS[options.convert_function][
            "rgb2yuv"
        ]
        convert_yuv2rgb = yuvconv.CONVERSION_FUNCTIONS[options.convert_function][
            "yuv2rgb"
        ]
    elif options.tv_type == "sdtv":
        convert_rgb2yuv = yuvconv.convert_rgb2yuv_ycbcr_sdtv_computer
        convert_yuv2rgb = yuvconv.convert_yuv2rgb_ycbcr_sdtv_computer
    elif options.tv_type == "hdtv":
        convert_rgb2yuv = yuvconv.convert_rgb2yuv_ycbcr_hdtv_computer
        convert_yuv2rgb = yuvconv.convert_yuv2rgb_ycbcr_hdtv_computer

    # decide the order
    fun1 = convert_rgb2yuv if options.func == "rgb2yuv" else convert_yuv2rgb
    fun2 = convert_rgb2yuv if options.func == "yuv2rgb" else convert_yuv2rgb

    # 0. start with a comparison cube with no vertices
    line = generate_equidistant_list(0, 255, options.num_vertices)
    (
        x0s,
        y0s,
        z0s,
    ) = generate_cube(line)

    # 1. convert comparison cube
    x1s, y1s, z1s = convert_cube(x0s, y0s, z0s, fun1)
    if options.clip:
        x1s = list(clip_value(x) for x in x1s)
        y1s = list(clip_value(x) for x in y1s)
        z1s = list(clip_value(x) for x in z1s)

    # 2. convert back to the original coordinate system
    x2s, y2s, z2s = convert_cube(x1s, y1s, z1s, fun2)
    if options.clip:
        x2s = list(clip_value(x) for x in x2s)
        y2s = list(clip_value(x) for x in y2s)
        z2s = list(clip_value(x) for x in z2s)

    # 3. set colors: gray for YUV, red for RGB
    if options.func == "rgb2yuv":
        color0, color1, color2 = "red", "black", "orange"
    else:  # options.func == "yuv2rgb"
        color0, color1, color2 = "black", "r", "gray"

    # 4. plot the cubes

    # 4.1. init the plot
    fig = plt.figure()
    window_title = f"{options.func} clip: {options.clip}"
    fig.canvas.manager.set_window_title(window_title)
    ax = fig.add_subplot(111, projection="3d")

    # coordinate system matching: Y-G, U-B, V-R
    def match_coordinates(xs, ys, zs, src_yuv=True):
        if src_yuv:
            return xs, ys, zs
        else:
            return ys, zs, xs

    # 4.2. start plotting the comparison cube
    xcube0, ycube0, zcube0 = match_coordinates(x0s, y0s, z0s, options.func == "yuv2rgb")
    ax.scatter3D(xcube0, ycube0, zcube0, color=color0, marker="X")
    add_cube_sides(False, ax, xcube0, ycube0, zcube0, color=color0, alpha=0.1)

    # 4.3. plot the first conversion
    xcube1, ycube1, zcube1 = match_coordinates(x1s, y1s, z1s, options.func == "yuv2rgb")
    ax.scatter3D(xcube1, ycube1, zcube1, color=color1)
    add_cube_sides(
        options.debug,
        ax,
        xcube1,
        ycube1,
        zcube1,
        color=color1,
        alpha=0.2,
        linestyle="dashed",
    )

    # 4.4. then plot the back conversion
    xcube2, ycube2, zcube2 = match_coordinates(x2s, y2s, z2s, options.func == "yuv2rgb")
    ax.scatter3D(xcube2, ycube2, zcube2, color=color2)
    add_cube_sides(
        options.debug,
        ax,
        xcube2,
        ycube2,
        zcube2,
        color=color2,
        alpha=0.2,
        linestyle="dashed",
    )

    # 4.5. add labels
    ax.set_xlabel("Y/G")
    ax.set_ylabel("U/B")
    ax.set_zlabel("V/R")

    # 4.6. homogeneize limits
    xlim, ylim, zlim = ax.get_xlim(), ax.get_ylim(), ax.get_zlim()
    lim_min = min(xlim[0], ylim[0], zlim[0])
    lim_max = max(xlim[1], ylim[1], zlim[1])
    ax.set_xlim(lim_min, lim_max)
    ax.set_ylim(lim_min, lim_max)
    ax.set_zlim(lim_min, lim_max)
    if not options.clip and options.func == "yuv2rgb":
        ax.set_xticks([-512, -256, 0, 128, 256, 512])
        ax.set_yticks([-512, -256, 0, 128, 256, 512])
        ax.set_zticks([-512, -256, 0, 128, 256, 512])
    else:  # options.func == "yuv2rgb":
        ax.set_xticks([0, 128, 256])
        ax.set_yticks([0, 128, 256])
        ax.set_zticks([0, 128, 256])

    plt.show()


def get_options(argv):
    """Generic option parser.

    Args:
        argv: list containing arguments

    Returns:
        Namespace - An argparse.ArgumentParser-generated option object
    """
    # init parser
    # usage = 'usage: %prog [options] arg1 arg2'
    # parser = argparse.OptionParser(usage=usage)
    # parser.print_help() to get argparse.usage (large help)
    # parser.print_usage() to get argparse.usage (just usage line)
    parser = argparse.ArgumentParser(description="Generic runner argparser.")
    parser.add_argument(
        "-d",
        "--debug",
        action="count",
        dest="debug",
        default=default_values["debug"],
        help="Increase verbosity (multiple times for more)",
    )
    parser.add_argument(
        "--quiet",
        action="store_const",
        dest="debug",
        const=-1,
        help="Zero verbosity",
    )
    parser.add_argument(
        "--clip",
        action="store_true",
        dest="clip",
        default=default_values["clip"],
        help="Clip values to [0, 255] [default: %s]" % default_values["clip"],
    )
    parser.add_argument(
        "--no-clip",
        action="store_false",
        dest="clip",
        help="Do not clip values to [0, 255] [default: %s]" % default_values["clip"],
    )
    parser.add_argument(
        "--numv",
        action="store",
        type=int,
        dest="num_vertices",
        default=default_values["num_vertices"],
        metavar="NUM_VERTICES",
        help="use NUM_VERTICES vertices",
    )
    parser.add_argument(
        "--tv-type",
        action="store",
        nargs=1,
        dest="tv_type",
        default=default_values["tv_type"],
        choices=TV_LIST,
        help="use TYPE for tv type",
    )
    parser.add_argument(
        "--sdtv",
        action="store_const",
        dest="tv_type",
        const="sdtv",
        help="use SDTV for tv type",
    )
    parser.add_argument(
        "--hdtv",
        action="store_const",
        dest="tv_type",
        const="hdtv",
        help="use HDTV for tv type",
    )
    parser.add_argument(
        "--saturation",
        dest="saturation",
        action="store_true",
        default=False,
        help="Plot saturated parallelepiped",
    )
    parser.add_argument(
        "--unscaled-transform",
        dest="saturation",
        action="store_false",
        default=False,
        help="Plot unscaled transform",
    )
    parser.add_argument(
        "--convert",
        action="store",
        type=str,
        dest="convert_function",
        default=default_values["convert_function"],
        help="Use a specific convert function",
    )
    parser.add_argument(
        "func",
        type=str,
        default=default_values["func"],
        choices=FUNCTIONS,
        help="%s" % (" | ".join(FUNCTIONS)),
    )

    # do the parsing
    options = parser.parse_args(argv[1:])
    # check the values
    if (
        options.convert_function is not None
        and options.convert_function not in yuvconv.CONVERSION_FUNCTIONS
    ):
        print(
            "error: invalid conversion function (%s). Must be one of %s"
            % (options.convert_function, ",".join(yuvconv.CONVERSION_FUNCTIONS))
        )
        sys.exit(-1)

    return options


def main(argv):
    # parse options
    options = get_options(argv)
    # print results
    if options.debug > 0:
        print(options)
    # do something
    show_cube_plot(options)


if __name__ == "__main__":
    # at least the CLI program name: (CLI) execution
    main(sys.argv)
