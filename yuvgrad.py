#!/usr/bin/env python3

"""yuvgrad: A gradient generator.

This module generates YUV files with smooth gradients.
"""

import argparse
import copy
import sys
import yuvcommon

VALID_PIX_FMT = ('yuv420p', 'nv12')
RANGE_LIST = ('full', 'limited')
PREDEFINED_IMAGE_LIST = (
    'color',
    'gray',
    'color_eee',
    'sdtv.y',
    'sdtv.u',
    'sdtv.v',
    'sdtv.uv',
    'hdtv.y',
    'hdtv.u',
    'hdtv.v',
    'hdtv.uv',
)
VALUE_LIST_RANGE = ('ymin', 'ymax', 'umin', 'umax', 'vmin', 'vmax')
VALUE_LIST_NO_RANGE = ('ygrad', 'ugrad', 'vgrad')
GRAD_LIST = ('N', 'S', 'W', 'E')

yuv_range = {
    'full': {
        'ymin': 0,
        'ymax': 255,
        'umin': 0,
        'umax': 255,
        'vmin': 0,
        'vmax': 255,
    },
    'limited': {
        'ymin': 16,
        'ymax': 235,
        'umin': 16,
        'umax': 240,
        'vmin': 16,
        'vmax': 240,
    },
}

predefined_images = {}

# color image
predefined_images['color'] = {
    'full': copy.deepcopy(yuv_range['full']),
    'limited': copy.deepcopy(yuv_range['limited']),
}
predefined_images['color']['ygrad'] = 'E'
predefined_images['color']['ugrad'] = 'S'
predefined_images['color']['vgrad'] = 'N'

# gray image
predefined_images['gray'] = copy.deepcopy(predefined_images['color'])
for r in RANGE_LIST:
    predefined_images['gray'][r]['umin'] = 128
    predefined_images['gray'][r]['umax'] = 128
    predefined_images['gray'][r]['vmin'] = 128
    predefined_images['gray'][r]['vmax'] = 128

# color_eee image
predefined_images['color_eee'] = copy.deepcopy(predefined_images['color'])
predefined_images['color_eee']['ygrad'] = 'E'
predefined_images['color_eee']['ugrad'] = 'E'
predefined_images['color_eee']['vgrad'] = 'E'

# SDTV images
# details at conversions.md
# produced using:
# $ ./yuvtools/yuvcube.py -dd --unscaled-transform --sdtv rgb2yuv
SDTV_CUBE = (
    (16, 128, 128),
    (40, 239, 109),
    (169, 165, 16),
    (144, 53, 34),
    (81, 90, 239),
    (106, 202, 221),
    (235, 128, 128),
    (210, 16, 146),
)

# HDTV images
# details at conversions.md
# produced using:
# $ ./yuvtools/yuvcube.py -dd --unscaled-transform --hdtv rgb2yuv
HDTV_CUBE = (
    (16, 128, 128),
    (31, 239, 117),
    (188, 153, 16),
    (172, 41, 26),
    (62, 102, 239),
    (78, 214, 229),
    (235, 127, 128),
    (219, 16, 138),
)


def add_cube_image(cube, vertex_from, vertex_to):
    d = copy.deepcopy(predefined_images['color'])
    d['limited']['ymin'] = cube[vertex_from][0]
    d['limited']['ymax'] = cube[vertex_to][0]
    d['limited']['umin'] = cube[vertex_from][1]
    d['limited']['umax'] = cube[vertex_to][1]
    d['limited']['vmin'] = cube[vertex_from][1]
    d['limited']['vmax'] = cube[vertex_to][2]
    d['ygrad'] = 'E'
    d['ugrad'] = 'E'
    d['vgrad'] = 'E'
    return d


# 1. sdtv.y
# Z[0]: (16, 128, 128)
# Z[6]: (235, 128, 128)
predefined_images['sdtv.y'] = add_cube_image(SDTV_CUBE, 0, 6)

# 2. sdtv.u
# Z[7]: (210, 16, 146)
# Z[1]: (40, 239, 109)
predefined_images['sdtv.u'] = add_cube_image(SDTV_CUBE, 7, 1)

# 3. sdtv.v
# Z[2]: (169, 165, 16)
# Z[4]: (81, 90, 239)
predefined_images['sdtv.v'] = add_cube_image(SDTV_CUBE, 2, 4)

# 4. sdtv.uv
# Z[3]: (144, 53, 34)
# Z[5]: (106, 202, 221)
predefined_images['sdtv.uv'] = add_cube_image(SDTV_CUBE, 3, 5)

# 1. hdtv.y
# Z[0]: (16, 128, 128)
# Z[6]: (235, 127, 128)
predefined_images['hdtv.y'] = add_cube_image(HDTV_CUBE, 0, 6)

# 2. hdtv.u
# Z[7]: (219, 16, 138)
# Z[1]: (31, 239, 117)
predefined_images['hdtv.u'] = add_cube_image(HDTV_CUBE, 7, 1)

# 3. hdtv.v
# Z[2]: (188, 153, 16)
# Z[4]: (62, 102, 239)
predefined_images['hdtv.v'] = add_cube_image(HDTV_CUBE, 2, 4)

# 4. hdtv.uv
# Z[3]: (172, 41, 26)
# Z[5]: (78, 214, 229)
predefined_images['hdtv.uv'] = add_cube_image(HDTV_CUBE, 3, 5)


for image in ('sdtv.y', 'sdtv.u', 'sdtv.v', 'sdtv.uv',
              'hdtv.y', 'hdtv.u', 'hdtv.v', 'hdtv.uv'):
    for value in ('ymin', 'ymax'):
        predefined_images[image]['full'][value] = yuvcommon.scale_fr2lr_16_235(
            predefined_images[image]['limited'][value])
    for value in ('umin', 'umax', 'vmin', 'vmax'):
        predefined_images[image]['full'][value] = yuvcommon.scale_fr2lr_16_240(
            predefined_images[image]['limited'][value])

# set full default values
default_values = {
    'width': 1280,
    'height': 720,
    'pix_fmt': 'yuv420p',
}
default_values.update(predefined_images['color']['full'])
default_values.update(predefined_images['color'])


def generator(xgrad, w, h, xmin, xmax):
    if xgrad == 'E':
        # gradient is left-to-right
        # f(i) = ax + bx*i
        # f(0) = xmin = ax
        ax = xmin
        # f(w) = xmax = ax + bx * w = xmin + bx * (w - 1)
        bx = (xmax - xmin) / (w - 1)

    elif xgrad == 'W':
        # gradient is right-to-left
        # f(i) = ax + bx*i
        # f(0) = xmax = ax
        ax = xmax
        # f(w) = xmin = ax + bx * w = xmax + bx * (w - 1)
        bx = (xmin - xmax) / (w - 1)

    elif xgrad == 'S':
        # gradient is top-down
        # f(j) = ax + bx*j
        # f(0) = xmin = ax
        ax = xmin
        # f(h) = xmax = ax + bx * h = xmin + bx * (h - 1)
        bx = (xmax - xmin) / (h - 1)

    elif xgrad == 'N':
        # gradient is bottom-up
        # f(j) = ax + bx*j
        # f(0) = xmax = ax
        ax = xmax
        # f(h) = xmin = ax + bx * h = (xmax - 1) + bx * (h - 1)
        bx = (xmin - xmax) / (h - 1)

    if xgrad in ('E', 'W'):
        # vertical gradient
        for _ in range(0, h):
            for i in range(0, w):
                val = ax + bx * i
                yield(int(val))

    elif xgrad in ('S', 'N'):
        # horizontal gradient
        for j in range(0, h):
            for _ in range(0, w):
                val = ax + bx * j
                yield(int(val))


def generate_gradient_file(fout, width, height, ygrad, ymin, ymax, ugrad,
                           umin, umax, vgrad, vmin, vmax, pix_fmt):
    # create the generators
    yw, yh = width, height
    cw, ch = width // 2, height // 2
    ygen = generator(ygrad, yw, yh, ymin, ymax)
    ugen = generator(ugrad, cw, ch, umin, umax)
    vgen = generator(vgrad, cw, ch, vmin, vmax)

    # write the luma
    for yval in ygen:
        fout.write(bytearray([yval]))

    # write the chromas
    if pix_fmt == 'yuv420p':
        # write the U chroma
        for uval in ugen:
            fout.write(bytearray([uval]))
        # write the V chroma
        for vval in vgen:
            fout.write(bytearray([vval]))

    elif pix_fmt == 'nv12':
        # write the U and V values interlaced
        for uval, vval in zip(ugen, vgen):
            fout.write(bytearray([uval]))
            fout.write(bytearray([vval]))


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
    parser.add_argument(
        '-d', '--debug', action='count',
        dest='debug', default=0,
        help='Increase verbosity (use multiple times for more)',)
    parser.add_argument(
        '--quiet', action='store_const',
        dest='debug', const=-1,
        help='Zero verbosity',)
    parser.add_argument(
        '--width', action='store', type=int,
        dest='width', default=default_values['width'],
        metavar='WIDTH',
        help=('use WIDTH width (default: %i)' %
              default_values['width']),)
    parser.add_argument(
        '--height', action='store', type=int,
        dest='height', default=default_values['height'],
        metavar='HEIGHT',
        help=('use HEIGHT height (default: %i)' %
              default_values['height']),)

    class VideoSizeAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            namespace.width, namespace.height = [int(v) for v in
                                                 values[0].split('x')]
    parser.add_argument(
        '--video_size', action=VideoSizeAction, nargs=1,
        help='use <width>x<height>',)
    parser.add_argument(
        '--ymin', action='store', type=int,
        dest='ymin', default=default_values['ymin'],
        metavar='YMIN',
        help=('use YMIN min value for Y (default: %i)' %
              default_values['ymin']),)
    parser.add_argument(
        '--ymax', action='store', type=int,
        dest='ymax', default=default_values['ymax'],
        metavar='YMAX',
        help=('use YMAX max value for Y (default: %i)' %
              default_values['ymax']),)
    parser.add_argument(
        '--umin', action='store', type=int,
        dest='umin', default=default_values['umin'],
        metavar='UMIN',
        help=('use UMIN min value for U (default: %i)' %
              default_values['umin']),)
    parser.add_argument(
        '--umax', action='store', type=int,
        dest='umax', default=default_values['umax'],
        metavar='UMAX',
        help=('use UMAX max value for U (default: %i)' %
              default_values['umax']),)
    parser.add_argument(
        '--vmin', action='store', type=int,
        dest='vmin', default=default_values['vmin'],
        metavar='VMIN',
        help=('use VMIN min value for V (default: %i)' %
              default_values['vmin']),)
    parser.add_argument(
        '--vmax', action='store', type=int,
        dest='vmax', default=default_values['vmax'],
        metavar='VMAX',
        help=('use VMAX max value for V (default: %i)' %
              default_values['vmax']),)

    class CustomAction(argparse.Action):
        def __init__(self, option_strings, dest, **kwargs):
            super(CustomAction, self).__init__(option_strings, dest, **kwargs)

        def __call__(self, parser, namespace, values, option_string=None):
            if option_string == '--full-range':
                namespace.range = 'full'
            elif option_string == '--limited-range':
                namespace.range = 'limited'
            elif option_string == '--range':
                namespace.range = values[0]
            elif option_string == '--predefined':
                namespace.predefined = values[0]
            for v in VALUE_LIST_RANGE:
                if namespace.range is None:
                    namespace.range = 'full'
                if namespace.predefined is None:
                    namespace.predefined = 'color'
                setattr(namespace, v,
                        predefined_images[namespace.predefined]
                        [namespace.range][v])
            for v in VALUE_LIST_NO_RANGE:
                if namespace.predefined is None:
                    namespace.predefined = 'color'
                setattr(namespace, v,
                        predefined_images[namespace.predefined][v])

    parser.add_argument(
        '--range', action=CustomAction, nargs=1,
        choices=RANGE_LIST,
        help='use RANGE for Y, U, V',)
    parser.add_argument(
        '--full-range', action=CustomAction, nargs=0,
        dest='range',
        help='use FULL-RANGE for Y, U, V',)
    parser.add_argument(
        '--limited-range', action=CustomAction, nargs=0,
        dest='range',
        help='use LIMITED-RANGE for Y, U, V',)
    parser.add_argument(
        '--predefined', action=CustomAction, nargs=1,
        choices=PREDEFINED_IMAGE_LIST,
        help='use predefined image',)
    parser.add_argument(
        '--pix_fmt', action='store', type=str,
        dest='pix_fmt', default=default_values['pix_fmt'],
        choices=VALID_PIX_FMT,
        metavar='PIX_FMT',
        help=('chroma format %r (default: %s)' %
              (VALID_PIX_FMT, default_values['pix_fmt'])),)
    parser.add_argument(
        '--ygrad', action='store', type=str,
        dest='ygrad', default=default_values['ygrad'],
        choices=GRAD_LIST,
        metavar='YGRAD',
        help=('y gradient %r (default: %s)' %
              (GRAD_LIST, default_values['ygrad'])),)
    parser.add_argument(
        '--ugrad', action='store', type=str,
        dest='ugrad', default=default_values['ugrad'],
        choices=GRAD_LIST,
        metavar='UGRAD',
        help=('u gradient %r (default: %s)' %
              (GRAD_LIST, default_values['ugrad'])),)
    parser.add_argument(
        '--vgrad', action='store', type=str,
        dest='vgrad', default=default_values['vgrad'],
        choices=GRAD_LIST,
        metavar='VGRAD',
        help=('v gradient %r (default: %s)' %
              (GRAD_LIST, default_values['vgrad'])),)
    parser.add_argument(
        "-o",
        "--outfile",
        dest="outfile",
        type=str,
        default=None,
        metavar='OUTPUT-FILE',
        help='output file',)
    # do the parsing
    options = parser.parse_args(argv[1:])
    return options


def main(argv):
    # parse options
    options = get_options(argv)
    # get outfile
    if options.outfile in (None, '-'):
        options.outfile = sys.stdout
    # print results
    if options.debug > 0:
        print(options)
    # open outfile
    if options.outfile != sys.stdout:
        try:
            fout = open(options.outfile, 'wb')  # noqa: P201
        except IOError:
            print('Error: cannot open file "%s":' % options.outfile)
    else:
        fout = sys.stdout.buffer
    # generate gradient file
    generate_gradient_file(fout, options.width, options.height,
                           options.ygrad, options.ymin, options.ymax,
                           options.ugrad, options.umin, options.umax,
                           options.vgrad, options.vmin, options.vmax,
                           options.pix_fmt)
    # close the file
    fout.close()


if __name__ == '__main__':
    # at least the CLI program name: (CLI) execution
    main(sys.argv)
