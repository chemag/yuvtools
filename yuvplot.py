#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.

from __future__ import print_function

import sys
import os
import os.path
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
import argparse
import yuvcommon

FONTSIZE_SMALL = 10
FONTSIZE_MEDIUM = 11
FONTSIZE_BIG = 16

VALID_PIX_FMT = ['yuv420p', 'nv12']

IMAGE_NAME = None

PIXEL_RANGE = range(0, 256)
DIFF_PIXEL_RANGE = range(-255, 256)
IMAGE_EXT = 'png'


# get the histogram of pixel values
def get_pixel_histogram(w, h, data, not_a_diff):
    # assume FR (full-range)
    xdata = PIXEL_RANGE if not_a_diff else DIFF_PIXEL_RANGE
    hist = [0] * (256 if not_a_diff else 511)
    for y in range(h):
        for x in range(w):
            val = int(data[y][x])
            if not not_a_diff:
                val += 256
            hist[val] += 1
    return xdata, hist


# get a distribution of pixel values for a given coordinate
def get_pixel_distribution(w, h, data, calc_axis=0):
    # horizontal \eq (calc_axis == 0)
    distro = np.zeros((256, w if calc_axis == 0 else h))
    for y in range(h):
        for x in range(w):
            val = int(data[y][x])
            distro[val][x if calc_axis == 0 else y] += 1
    return distro


# plot a histogram of luma and/or chromas
def plot_histogram_help(datax, datay, plotsize, location, rowspan,
                        colspan, xlabel, ylabel):
    plt.subplot2grid(plotsize, location, colspan=colspan, rowspan=rowspan)
    plt.plot(datax, datay, '.')
    plt.grid()
    plt.xlabel(xlabel, fontsize=FONTSIZE_SMALL)
    plt.ylabel(ylabel, fontsize=FONTSIZE_SMALL)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)


def plot_histogram(source, name, options, ydata, udata, vdata):
    title = '%s (%s) %s Histogram' % (name, source,
        ('diff(%s)' % options.diff) if options.diff is not None else '')

    fig = plt.figure(num=title, figsize=options.figsize)
    # chroma (4:2:0) dimensions
    w, h = options.width, options.height
    cw, ch = int(w / 2), int(h / 2)

    # get layout
    rows = 0
    if not options.no_luma:
        rows += 1
    if not options.no_chroma:
        rows += 2
    plotsize = (rows, 1)
    row_id = 0

    # print luma
    if not options.no_luma:
        location = (row_id, 0)
        xdata, yhist = get_pixel_histogram(w, h, ydata, options.diff is None)
        plot_histogram_help(xdata, yhist, plotsize, location, 1, 1, 'Y',
                            'Y (luma)')
        fig.set_facecolor('w')
        row_id += 1

    # print chromas
    if not options.no_chroma:
        # print U
        location = (row_id, 0)
        xdata, uhist = get_pixel_histogram(cw, ch, udata, options.diff is None)
        plot_histogram_help(xdata, uhist, plotsize, location, 1, 1, 'Cb',
                            'Cb (U chroma)')
        fig.set_facecolor('w')
        row_id += 1
        # print V
        location = (row_id, 0)
        xdata, vhist = get_pixel_histogram(cw, ch, vdata, options.diff is None)
        plot_histogram_help(xdata, vhist, plotsize, location, 1, 1, 'Cr',
                            'Cr (V chroma)')
        fig.set_facecolor('w')
        row_id += 1

    fig.suptitle(title, fontsize=FONTSIZE_BIG)
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    fig.savefig('%s.hist.%s' % (source, IMAGE_EXT))


def plot_distribution_help(datax, datay1, datay2, name, color):
    line, = plt.plot(datax, datay1, '-', color=color)
    line.set_label('%s.avg' % name)
    line, = plt.plot(datax, datay2, '-', linestyle='dotted', color=color)
    #line.set_label('%s.sttdev' % name)


def plot_distribution(source, name, options, ydata, udata, vdata, calc_axis):
    orientation = 'horizontal' if calc_axis == 0 else 'vertical'
    title = '%s %s Distribution' % (orientation,
        ('diff(%s)' % options.diff) if options.diff is not None else '')

    fig = plt.figure(num=title, figsize=options.figsize)
    # chroma (4:2:0) dimensions
    w, h = options.width, options.height
    cw, ch = w // 2, h // 2
    yplotrange = w if calc_axis == 0 else h
    cplotrange = cw if calc_axis == 0 else ch
    xlabel = 'width' if calc_axis == 0 else 'height'
    ddata = udata - vdata
    # get plot limits
    y_ymax = 255
    y_ymin = 0
    c_ymax = 255
    c_ymin = 0
    if options.diff is not None:
        y_ymin = min(y_ymin, int(np.amin(ydata)))
        c_ymin = min(c_ymin, int(np.amin(udata)))
        c_ymin = min(c_ymin, int(np.amin(vdata)))
    if not options.no_uvdiff:
        c_ymin = min(c_ymin, int(np.amin(ddata)))
    y_ylim = (y_ymin * 1.1, y_ymax)
    c_ylim = (c_ymin * 1.1, c_ymax)

    # get layout
    rows = 0
    if not options.no_luma:
        rows += 1
    if not options.no_chroma:
        rows += 1
    plotsize = (rows, 1)

    # print luma
    row_id = 0
    if not options.no_luma:
        location = (row_id, 0)
        xdata = range(yplotrange)
        ymean = np.mean(ydata, axis=calc_axis)
        ystddev = np.std(ydata, axis=calc_axis)
        plt.subplot2grid(plotsize, location, 1, 1)
        plot_distribution_help(xdata, ymean, ystddev, name, '0.5')
        plt.grid()
        plt.xlabel('Y', fontsize=FONTSIZE_SMALL)
        plt.ylabel('Y', fontsize=FONTSIZE_SMALL)
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-',
                 alpha=0.2)
        plt.legend()
        fig.set_facecolor('w')
        ax = fig.get_axes()
        ax[row_id].set(xlim=(0, yplotrange), ylim=y_ylim)
        row_id += 1

    # print chromas
    if not options.no_chroma:
        location = (row_id, 0)
        xdata = range(cplotrange)
        umean = np.mean(udata, axis=calc_axis)
        ustddev = np.std(udata, axis=calc_axis)
        vmean = np.mean(vdata, axis=calc_axis)
        vstddev = np.std(vdata, axis=calc_axis)
        dmean = np.mean(ddata, axis=calc_axis)
        dstddev = np.std(ddata, axis=calc_axis)
        # print U, V, and the UV diff
        plt.subplot2grid(plotsize, location, 1, 1)
        plot_distribution_help(xdata, umean, ustddev, '%s.U' % name, 'b')
        plot_distribution_help(xdata, vmean, vstddev, '%s.V' % name, 'r')
        if not options.no_uvdiff:
            plot_distribution_help(xdata, dmean, dstddev, '%s.U-V' % name, 'g')
        plt.grid()
        plt.xlabel(xlabel, fontsize=FONTSIZE_SMALL)
        plt.ylabel('chroma', fontsize=FONTSIZE_SMALL)
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-',
                 alpha=0.2)
        plt.legend()
        fig.set_facecolor('w')
        ax = fig.get_axes()
        ax[row_id].set(xlim=(0, cplotrange), ylim=c_ylim)
        row_id += 1

    fig.suptitle(title, fontsize=FONTSIZE_BIG)
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    return fig


def plot_map_help(datay, plotsize, location, rowspan, colspan, title,
                  xlabel, ylabel):
    plt.subplot2grid(plotsize, location, colspan=colspan, rowspan=rowspan)
    image = plt.imshow(datay,
                       aspect='auto',
                       origin='lower',
                       norm=clr.LogNorm(vmin=1 + datay.min(), vmax=1 + datay.max()),
                       cmap=plt.cm.pink.reversed())
    plt.grid()
    plt.title(title, fontsize=FONTSIZE_BIG)
    plt.xlabel(xlabel, fontsize=FONTSIZE_SMALL)
    plt.ylabel(ylabel, fontsize=FONTSIZE_SMALL)
    return image


def plot_map(source, name, options, ydata, udata, vdata, calc_axis):
    orientation = 'horizontal' if calc_axis == 0 else 'vertical'
    title = '%s (%s) %s %s Map' % (name, source,
        ('diff(%s)' % options.diff) if options.diff is not None else '',
        orientation)

    fig = plt.figure(num=title, figsize=options.figsize)
    # chroma (4:2:0) dimensions
    w, h = options.width, options.height
    cw, ch = int(w / 2), int(h / 2)
    xlabel = 'width' if calc_axis == 0 else 'height'

    # get layout
    rows = 0
    if not options.no_luma:
        rows += 1
    if not options.no_chroma:
        rows += 2
    plotsize = (rows, 1)
    row_id = 0

    # print luma
    if not options.no_luma:
        location = (row_id, 0)
        yhist = get_pixel_distribution(w, h, ydata, calc_axis)
        image = plot_map_help(yhist, plotsize, location, 1, 1, 'Y (luma)',
            xlabel, 'luma')
        fig.colorbar(image)
        fig.set_facecolor('w')
        row_id += 1

    # print chromas
    if not options.no_chroma:
        # print U
        location = (row_id, 0)
        uhist = get_pixel_distribution(cw, ch, udata, calc_axis)
        image = plot_map_help(uhist, plotsize, location, 1, 1, 'Cb (U chroma)',
            xlabel, 'Cb')
        fig.colorbar(image)
        fig.set_facecolor('w')
        row_id += 1
        # print V
        location = (row_id, 0)
        vhist = get_pixel_distribution(cw, ch, vdata, calc_axis)
        image = plot_map_help(vhist, plotsize, location, 1, 1, 'Cr (V chroma)',
            xlabel, 'Cr')
        fig.colorbar(image)
        fig.set_facecolor('w')
        row_id += 1

    fig.suptitle(title, fontsize=FONTSIZE_BIG)
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    fig.savefig('%s.map.%s.%s' % (source, orientation, IMAGE_EXT))


def readImage(input_file, w, h, frame_number, pix_fmt):
    # get the full image
    with open(input_file, 'rb') as fin:
        data = yuvcommon.read_image(fin, w, h, pix_fmt, frame_number)

    # get luma and chroma (4:2:0) dimensions
    ysize = int(w * h)
    usize = ysize / 4
    cw, ch = int(w / 2), int(h / 2)

    # read the frame's luma
    ydata = np.zeros((h, w))
    for x in range(0, w):
        for y in range(0, h):
            val = data[w * y + x]
            ydata[y][x] = val

    # read the frame's chromas
    udata = np.zeros((ch, cw))
    vdata = np.zeros((ch, cw))
    if pix_fmt == 'yuv420p':
        for y in range(0, ch):
            for x in range(0, cw):
                val = data[int(cw * y + x + ysize)]
                udata[y][x] += val
        for y in range(0, ch):
            for x in range(0, cw):
                val = data[int(cw * y + x + ysize + usize)]
                vdata[y][x] += val

    elif pix_fmt == 'nv12':
        for x in range(0, cw):
            for y in range(0, ch):
                val = data[w * y + x * 2 + ysize]
                udata[y][x] += val
                val = data[w * y + x * 2 + ysize + 1]
                vdata[y][x] += val

    return ydata, udata, vdata


def get_options(argv):
    parser = argparse.ArgumentParser()
    # debug info
    parser.add_argument('-d', '--debug', action='count',
            dest='debug', default=0,
            help='Increase verbosity (use multiple times for more)',)
    parser.add_argument('--quiet', action='store_const',
            dest='debug', const=-1,
            help='Zero verbosity',)
    # input
    parser.add_argument('--width', action='store', type=int,
            dest='width', default=1280,
            metavar='WIDTH',
            help='use WIDTH width',)
    parser.add_argument('--height', action='store', type=int,
            dest='height', default=720,
            metavar='HEIGHT',
            help='use HEIGHT height',)

    class VideoSizeAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            namespace.width, namespace.height = [int(v) for v in
                                                 values[0].split('x')]
    parser.add_argument('--video_size', action=VideoSizeAction, nargs=1,
            help='use <width>x<height>',)
    parser.add_argument('-f', '--pix_fmt', action='store', type=str,
                        dest='pix_fmt', default='yuv420p',
                        choices=VALID_PIX_FMT,
                        metavar='PIX_FMT',
                        help=('chroma format %r' % VALID_PIX_FMT),)
    parser.add_argument('-n', '--frame_number',
                        required=False,
                        help='frame number',
                        type=int,
                        default=0)
    parser.add_argument('--no_luma',
                        required=False,
                        action='store_true',
                        default=False,
                        help='Do not show luma')
    parser.add_argument('--no_chroma',
                        required=False,
                        action='store_true',
                        default=False,
                        help='Do not show chroma')
    parser.add_argument('--no_uvdiff',
                        required=False,
                        action='store_true',
                        default=False,
                        help='Do not show UV (chroma) diff')
    # output
    parser.add_argument('--image',
                        required=False,
                        help='Export as image to given name',
                        type=str)
    parser.add_argument('--figsize',
                        help='Size of figure (WxH), in inches',
                        type=str,
                        default='10x8')

    # add sub-command parsers
    subparsers = parser.add_subparsers()
    parser_hist = subparsers.add_parser('hist',
                                       help='create a pixel histogram')
    parser_hist.set_defaults(func='hist')
    parser_distro = subparsers.add_parser('distro',
                                       help='create a pixel distribution')
    parser_distro.set_defaults(func='distro')
    parser_map = subparsers.add_parser('map',
                                       help='create a pixel map')
    parser_map.set_defaults(func='map')

    # input files
    for p in (parser_hist, parser_map, parser_distro):
        p.add_argument('source', nargs='+',
                       help='source/name list, separated with spaces')
        p.add_argument('--diff',
                       help='Original image to be compared to',
                       type=str,
                       default=None)

    options = parser.parse_args(argv[1:])

    # post-processing
    options.figsize = (None if options.figsize is None else
        [int(size) for size in options.figsize.split('x')])
    # process source/name list
    options.source_dict = {}
    last_source = None
    for item in options.source:
        # check if item is a valid (readable) file
        if os.access(item, os.R_OK):
            last_source = item
            options.source_dict[last_source] = last_source
        else:
            # assume it is a name
            if last_source is None:
                parser.print_usage()
                sys.exit(-1)
            options.source_dict[last_source] = item

    return options


def process_options(options):
    # parse parameters
    w, h = options.width, options.height

    if options.diff is not None:
        s_ydata, s_udata, s_vdata = readImage(options.diff, w, h,
            options.frame_number, options.pix_fmt)

    for source, name in options.source_dict.items():
        if options.debug > 0:
            print('processing file: "%s" name: "%s"' % (source, name))

        # read input image
        ydata, udata, vdata = readImage(source, w, h, options.frame_number,
                                        options.pix_fmt)
        if options.diff is not None:
            ydata = ydata - s_ydata
            udata = udata - s_udata
            vdata = vdata - s_vdata

        if options.func == 'hist':
            plot_histogram(source, name, options, ydata, udata, vdata)

        elif options.func == 'distro':
            # horizontal plot
            figh = plot_distribution(source, name, options, ydata, udata, vdata, 0)
            # vertical plot
            figv = plot_distribution(source, name, options, ydata, udata, vdata, 1)

        elif options.func == 'map':
            # horizontal plot
            plot_map(source, name, options, ydata, udata, vdata, 0)
            # vertical plot
            plot_map(source, name, options, ydata, udata, vdata, 1)

    if options.func == 'distro':
        # save the distro plots
        figh.savefig('%s.distro.%s.%s' % (source, 'horizontal', IMAGE_EXT))
        figv.savefig('%s.distro.%s.%s' % (source, 'vertical', IMAGE_EXT))

    # XXX(chema)
    #if options.image is None:
    #    plt.show()


if __name__ == '__main__':
    options = get_options(sys.argv)
    if options.debug > 0:
        print(options)
    process_options(options)
