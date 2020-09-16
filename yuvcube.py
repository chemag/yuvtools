#!/usr/bin/env python
# Copyright (c) Facebook, Inc. and its affiliates.

import argparse
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib.pyplot as plt
import sys

import yuvconv
import yuvcommon


TV_LIST = ['sdtv', 'hdtv']
default = {
    'num_vertices': 2,
    'tv_type': 'sdtv',
}


# https://stackoverflow.com/questions/44881885/python-draw-parallelepiped/49766400
def add_cube_sides(debug, ax, xs, ys, zs, color='k', **kwargs):
    # ax.scatter3D(xs, ys, zs, color=color)
    # r = [-1,1]
    # X, Y = np.meshgrid(r, r)
    # plot vertices
    verts = []
    d = int(round(len(xs) ** (1 / 3.)))
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
    index_list = (0, d - 1, d**2 - 1, d**2 - d,
                  d**3 - d**2, d**3 - d**2 + d - 1, d**3 - 1, d**3 - d)
    Z = []
    for i, index in enumerate(index_list):
        Z.append([xs[index], ys[index], zs[index]])
        if debug > 0:
            print('Z[%i]: (%i, %i, %i)' % (i, Z[i][0], Z[i][1], Z[i][2]))

    # plot sides
    # list of sides' polygons of figure
    verts = [[Z[0], Z[1], Z[2], Z[3]],
             [Z[4], Z[5], Z[6], Z[7]],
             [Z[0], Z[1], Z[5], Z[4]],
             [Z[2], Z[3], Z[7], Z[6]],
             [Z[1], Z[2], Z[6], Z[5]],
             [Z[4], Z[7], Z[3], Z[0]]]
    ax.add_collection3d(Line3DCollection(verts, linewidths=2, facecolors=color,
                                         **kwargs))
    # add an arrow from (0, 0, 0) to (255, 255, 255)
    ax.quiver(Z[0][0], Z[0][1], Z[0][2], Z[6][0] - Z[0][0], Z[6][1] - Z[0][1],
              Z[6][2] - Z[0][2], color=color)


def generate_equidistant_list(vmin, vmax, numv):
    # f(x) = a * x + b
    # f(0) = a * 0 + b = b = vmin
    b = vmin
    # f(numv - 1) = a * (numv - 1) + b = vmax
    a = 1. * (vmax - b) / (numv - 1)
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
            print('removing value x: %i, y: %i, z: %i' % (x, y, z))
            i += 1
            continue
        else:
            xos.append(x)
            yos.append(y)
            zos.append(z)
    print('--> removed %i/%i values' % (i, len(xs)))
    return xos, yos, zos


def plot_cube(options):
    # create input data
    line = generate_equidistant_list(0, 255, options.num_vertices)
    if options.func == 'rgb2yuv':
        # start with rgb
        rs, gs, bs = generate_cube(line)
    else:  # 'yuv2rgb':
        # start with yuv
        ys, us, vs = generate_cube(line)

    if not options.saturation:
        yuvcommon.DO_NOT_NORMALIZE = True

    # get conversion functions
    if options.tv_type == 'sdtv':
        convert_rgb2yuv = yuvconv.convert_rgb2yuv_ycbcr_sdtv_computer
        convert_yuv2rgb = yuvconv.convert_yuv2rgb_ycbcr_sdtv_computer
    elif options.tv_type == 'hdtv':
        convert_rgb2yuv = yuvconv.convert_rgb2yuv_ycbcr_hdtv_computer
        convert_yuv2rgb = yuvconv.convert_yuv2rgb_ycbcr_hdtv_computer

    if options.func == 'rgb2yuv':
        # convert to yuv
        ys, us, vs = convert_cube(rs, gs, bs, convert_rgb2yuv)
    else:  # 'yuv2rgb':
        # convert to rgb
        rs, gs, bs = convert_cube(ys, us, vs, convert_yuv2rgb)

    if not options.saturation:
        # # remove valid elements from the produced cube
        # if options.func == 'rgb2yuv':
        #     ys, us, vs = remove_valid_elements(ys, us, vs)
        # else:  # 'yuv2rgb':
        #     rs, gs, bs = remove_valid_elements(rs, gs, bs)
        0

    else:
        # convert back to the original coordinate system
        if options.func == 'rgb2yuv':
            # convert back to rgb
            r2s, g2s, b2s = convert_cube(ys, us, vs, convert_yuv2rgb)
        else:  # 'yuv2rgb':
            # convert back to yuv
            y2s, u2s, v2s = convert_cube(rs, gs, bs, convert_rgb2yuv)

    # init the plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # ax.scatter3D(ys, us, vs, color=color)
    # add_cube_sides(options.debug, ax, ys, us, vs)

    if not options.saturation:
        if options.func == 'rgb2yuv':
            ax.scatter3D(ys, us, vs, color='g')
            add_cube_sides(options.debug, ax, ys, us, vs, color='g', alpha=0.2)
            ax.set_xlabel('Y')
            ax.set_ylabel('U')
            ax.set_zlabel('V')
        else:  # 'yuv2rgb':
            ax.scatter3D(rs, gs, bs, color='r')
            add_cube_sides(options.debug, ax, rs, gs, bs, color='r', alpha=0.2)
            ax.set_xlabel('R')
            ax.set_ylabel('G')
            ax.set_zlabel('B')

    else:
        if options.func == 'rgb2yuv':
            ax.scatter3D(r2s, g2s, b2s, color='r')
            add_cube_sides(options.debug, ax, r2s, g2s, b2s, color='r',
                           alpha=0.2)
            ax.set_xlabel('R')
            ax.set_ylabel('G')
            ax.set_zlabel('B')
        else:  # 'yuv2rgb':
            ax.scatter3D(y2s, u2s, v2s, color='g')
            add_cube_sides(options.debug, ax, y2s, u2s, v2s, color='g',
                           alpha=0.2)
            ax.set_xlabel('Y')
            ax.set_ylabel('U')
            ax.set_zlabel('V')

    # add a comparison cube
    l2 = (0, 255)
    xss, yss, zss, = generate_cube(l2)
    add_cube_sides(False, ax, xss, yss, zss, color='k', alpha=.1)

    # homogeneize limits
    xlim, ylim, zlim = ax.get_xlim(), ax.get_ylim(), ax.get_zlim()
    lim_min = min(xlim[0], ylim[0], zlim[0])
    lim_max = max(xlim[1], ylim[1], zlim[1])
    ax.set_xlim(lim_min, lim_max)
    ax.set_ylim(lim_min, lim_max)
    ax.set_zlim(lim_min, lim_max)

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
    parser = argparse.ArgumentParser(description='Generic runner argparser.')
    parser.add_argument('-d', '--debug', action='count',
                        dest='debug', default=0,
                        help='Increase verbosity (multiple times for more)',)
    parser.add_argument('--quiet', action='store_const',
                        dest='debug', const=-1,
                        help='Zero verbosity',)
    parser.add_argument('--numv', action='store', type=int,
                        dest='num_vertices', default=default['num_vertices'],
                        metavar='NUM_VERTICES',
                        help='use NUM_VERTICES vertices',)
    parser.add_argument('--tv-type', action='store', nargs=1,
                        dest='tv_type', default=default['tv_type'],
                        choices=TV_LIST,
                        help='use TYPE for tv type',)
    parser.add_argument('--sdtv', action='store_const',
                        dest='tv_type', const='sdtv',
                        help='use SDTV for tv type',)
    parser.add_argument('--hdtv', action='store_const',
                        dest='tv_type', const='hdtv',
                        help='use HDTV for tv type',)
    parser.add_argument('--unscaled-transform', dest='saturation',
                        action='store_false', default=False,
                        help='Plot unscaled transform',)
    parser.add_argument('--saturation', dest='saturation', action='store_true',
                        default=False,
                        help='Plot saturation parallelepiped',)
    # add sub-command parsers
    subparsers = parser.add_subparsers()
    # independent sub-commands
    parser_rgb2yuv = subparsers.add_parser('rgb2yuv',
                                           help='plot a rgb2yuv matrix')
    parser_rgb2yuv.set_defaults(func='rgb2yuv')
    parser_yuv2rgb = subparsers.add_parser('yuv2rgb',
                                           help='plot a yuv2rgb matrix')
    parser_yuv2rgb.set_defaults(func='yuv2rgb')
    # do the parsing
    options = parser.parse_args(argv[1:])
    return options


def main(argv):
    # parse options
    options = get_options(argv)
    # print results
    if options.debug > 0:
        print(options)
    # do something
    plot_cube(options)


if __name__ == '__main__':
    # at least the CLI program name: (CLI) execution
    main(sys.argv)
