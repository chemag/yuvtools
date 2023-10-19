#!/usr/bin/env python3

"""yuvconv: An rgb2yuv/yuv2rgb converter.

This module converts between YUV and RGB files, using pre-defined or
user-defined matrices.
"""

import argparse
from array import array
import sys
import yuvcommon

VALID_PIX_FMT = ("yuv420p", "nv12", "rgba", "yuv444p", "yuyv422")


# conversion data
# Jack, YIQ Color Space (page 18)
def convert_rgb2yuv_yiq(R, G, B):
    Y = 0.299 * R + 0.587 * G + 0.114 * B  # NOQA: E201,E241
    I = 0.596 * R - 0.275 * G - 0.321 * B  # NOQA: E201,E241,E741
    Q = 0.212 * R - 0.523 * G + 0.311 * B  # NOQA: E201,E241
    return Y, I, Q


def convert_yuv2rgb_yiq(Y, I, Q):  # NOQA: E741
    R = Y + 0.956 * I + 0.621 * Q  # NOQA: E201,E241,E741
    G = Y - 0.272 * I - 0.647 * Q  # NOQA: E201,E241
    B = Y - 1.107 * I + 1.704 * Q  # NOQA: E201,E241
    return R, G, B


# Jack, YUV Color Space (page 18), SDTV with BT.601
# https://en.wikipedia.org/wiki/YUV#SDTV_with_BT.601
# TODO(chemag): broken conversion, fix me (see unittest)
def convert_rgb2yuv_sdtv_basic(R, G, B):
    Y = 0.299 * R + 0.587 * G + 0.114 * B  # NOQA: E201,E241,E222
    U = -0.147 * R - 0.289 * G + 0.436 * B  # NOQA: E201,E241,E222
    V = 0.615 * R - 0.515 * G - 0.100 * B  # NOQA: E201,E241,E222
    return (yuvcommon.normalize(Y), yuvcommon.normalize(U), yuvcommon.normalize(V))


def convert_yuv2rgb_sdtv_basic(Y, U, V):
    R = Y + 1.140 * V  # NOQA: E201,E241,E221
    G = Y - 0.395 * U - 0.581 * V  # NOQA: E201,E241,E221
    B = Y + 2.032 * U  # NOQA: E201,E241,E221
    return (yuvcommon.normalize(R), yuvcommon.normalize(G), yuvcommon.normalize(B))


# Jack, YCbCr Color Space, SDTV, Analog (page 19)
def convert_rgb2yuv_ycbcr_sdtv_analog(R, G, B):
    R, G, B = R / 256.0, G / 256.0, B / 256.0
    Y = 0.299 * R + 0.587 * G + 0.114 * B  # NOQA: E201,E241,E221,E222
    Pb = -0.169 * R - 0.331 * G + 0.500 * B  # NOQA: E201,E241,E221,E222
    Pr = 0.500 * R - 0.419 * G - 0.081 * B  # NOQA: E201,E241,E221,E222
    Y = int(256 * Y)  # NOQA: E201,E241,E221
    Cb = int(256 * Pb + 128)
    Cr = int(256 * Pr + 128)
    return Y, Cb, Cr


# Jack, YCbCr Color Space, SDTV, Analog (page 20)
def convert_yuv2rgb_ycbcr_sdtv_analog(Y, U, V):
    Y, Pb, Pr = Y / 256.0, (U - 128) / 256.0, (V - 128) / 256.0
    R = Y + 1.402 * Pr
    G = Y - 0.714 * Pr - 0.344 * Pb
    B = Y + 1.772 * Pb  # NOQA: E221
    # convert back to integer
    R = int(256 * R)
    G = int(256 * G)
    B = int(256 * B)
    return (yuvcommon.normalize(R), yuvcommon.normalize(G), yuvcommon.normalize(B))


# Jack, YCbCr Color Space, SDTV, Digital (page 19)
def convert_rgb2yuv_ycbcr_sdtv_digital(R, G, B):
    # converts 8-bit digital RGB data with a 16-235 nominal range (Studio RGB)
    R, G, B = yuvcommon.rgb_fr2lr(R, G, B)
    Y = 0.299 * R + 0.587 * G + 0.114 * B  # NOQA: E201,E241,E221,E222
    Cb = -0.172 * R - 0.339 * G + 0.511 * B  # NOQA: E201,E241,E221,E222
    Cr = 0.511 * R - 0.428 * G - 0.083 * B  # NOQA: E201,E241,E221,E222
    return (
        yuvcommon.normalize(Y),
        yuvcommon.normalize(Cb + 128),
        yuvcommon.normalize(Cr + 128),
    )


# Jack, YCbCr Color Space, SDTV, Digital (page 20)
def convert_yuv2rgb_ycbcr_sdtv_digital(Y, Cb, Cr):
    R = Y + 1.371 * (Cr - 128)
    G = Y - 0.698 * (Cr - 128) - 0.336 * (Cb - 128)
    B = Y + 1.732 * (Cb - 128)
    # generated 8-bit RGB with a 16-235 nominal range (Studio RGB)
    return yuvcommon.rgb_lr2fr(R, G, B)


# Jack, YCbCr Color Space, SDTV, Computer Systems FR (page 20)
def convert_rgb2yuv_ycbcr_sdtv_computer(R, G, B):
    Y = 0.257 * R + 0.504 * G + 0.098 * B + 16  # NOQA: E201,E241,E221,E222
    Cb = -0.148 * R - 0.291 * G + 0.439 * B + 128  # NOQA: E201,E241,E221,E222
    Cr = 0.439 * R - 0.368 * G - 0.071 * B + 128  # NOQA: E201,E241,E221,E222
    # 8-bit YCbCr and RGB data should be saturated at the 0 and 255 levels
    return (yuvcommon.normalize(Y), yuvcommon.normalize(Cb), yuvcommon.normalize(Cr))


def convert_yuv2rgb_ycbcr_sdtv_computer(Y, Cb, Cr):
    R = 1.164 * (Y - 16) + 1.596 * (Cr - 128)
    G = 1.164 * (Y - 16) - 0.813 * (Cr - 128) - 0.391 * (Cb - 128)
    B = 1.164 * (Y - 16) + 2.018 * (Cb - 128)  # NOQA: E221,E501
    # 8-bit YCbCr and RGB data should be saturated at the 0 and 255 levels
    return (yuvcommon.normalize(R), yuvcommon.normalize(G), yuvcommon.normalize(B))


# https://en.wikipedia.org/wiki/YUV#HDTV_with_BT.709
# TODO(chemag): broken conversion, fix me (see unittest)
def convert_rgb2yuv_hdtv_basic(R, G, B):
    Y = 0.2126 * R + 0.7152 * G + 0.0722 * B  # NOQA: E201,E241,E221,E222
    U = -0.09991 * R - 0.33609 * G + 0.436 * B  # NOQA: E201,E241,E221,E222
    V = 0.615 * R - 0.55861 * G - 0.05639 * B  # NOQA: E201,E241,E221,E222
    return (yuvcommon.normalize(Y), yuvcommon.normalize(U), yuvcommon.normalize(V))


def convert_yuv2rgb_hdtv_basic(Y, U, V):
    R = Y + 1.28033 * V  # NOQA: E201,E241,E221
    G = Y - 0.21482 * U - 0.38059 * V  # NOQA: E201,E241,E221
    B = Y + 2.12798 * U  # NOQA: E201,E241,E221
    return (yuvcommon.normalize(R), yuvcommon.normalize(G), yuvcommon.normalize(B))


# Jack, YCbCr Color Space, HDTV, Analog (page 20)
def convert_rgb2yuv_ycbcr_hdtv_analog(R, G, B):
    R, G, B = R / 256.0, G / 256.0, B / 256.0
    Y = 0.213 * R + 0.715 * G + 0.072 * B  # NOQA: E201,E241,E221,E222
    Pb = -0.115 * R - 0.385 * G + 0.500 * B  # NOQA: E201,E241,E221,E222
    Pr = 0.500 * R - 0.454 * G - 0.046 * B  # NOQA: E201,E241,E221,E222
    Y = int(256 * Y)  # NOQA: E201,E241,E221
    Cb = int(256 * Pb + 128)
    Cr = int(256 * Pr + 128)
    return Y, Cb, Cr


# Jack, YCbCr Color Space, HDTV, Analog (page 21)
def convert_yuv2rgb_ycbcr_hdtv_analog(Y, U, V):
    Y, Pb, Pr = Y / 256.0, (U - 128) / 256.0, (V - 128) / 256.0
    R = Y + 1.575 * Pr
    G = Y - 0.468 * Pr - 0.187 * Pb
    B = Y + 1.856 * Pb  # NOQA: E221
    # convert back to integer
    R = int(256 * R)
    G = int(256 * G)
    B = int(256 * B)
    return (yuvcommon.normalize(R), yuvcommon.normalize(G), yuvcommon.normalize(B))


# Jack, YCbCr Color Space, HDTV, Digital (page 21)
def convert_rgb2yuv_ycbcr_hdtv_digital(R, G, B):
    # converts 8-bit digital RGB data with a 16-235 nominal range (Studio RGB)
    R, G, B = yuvcommon.rgb_fr2lr(R, G, B)
    Y = 0.213 * R + 0.715 * G + 0.072 * B  # NOQA: E201,E241,E221,E222
    Cb = -0.117 * R - 0.394 * G + 0.511 * B + 128  # NOQA: E201,E241,E221,E222
    Cr = 0.511 * R - 0.464 * G - 0.047 * B + 128  # NOQA: E201,E241,E221,E222
    return Y, Cb, Cr


# Jack, YCbCr Color Space, HDTV, Digital (page 21)
def convert_yuv2rgb_ycbcr_hdtv_digital(Y, Cb, Cr):
    R = Y + 1.540 * (Cr - 128)
    G = Y - 0.459 * (Cr - 128) - 0.183 * (Cb - 128)
    B = Y + 1.816 * (Cb - 128)
    # generated 8-bit RGB with a 16-235 nominal range (Studio RGB)
    return yuvcommon.rgb_lr2fr(R, G, B)


# Jack, YCbCr Color Space, HDTV, Computer Systems FR (page 21)
def convert_rgb2yuv_ycbcr_hdtv_computer(R, G, B):
    Y = 0.183 * R + 0.614 * G + 0.062 * B + 16  # NOQA: E201,E241,E221,E222
    Cb = -0.101 * R - 0.338 * G + 0.439 * B + 128  # NOQA: E201,E241,E221,E222
    Cr = 0.439 * R - 0.399 * G - 0.040 * B + 128  # NOQA: E201,E241,E221,E222
    # 8-bit YCbCr and RGB data should be saturated at the 0 and 255 levels
    return (yuvcommon.normalize(Y), yuvcommon.normalize(Cb), yuvcommon.normalize(Cr))


def convert_yuv2rgb_ycbcr_hdtv_computer(Y, Cb, Cr):
    R = 1.164 * (Y - 16) + 1.793 * (Cr - 128)
    G = 1.164 * (Y - 16) - 0.534 * (Cr - 128) - 0.213 * (Cb - 128)
    B = 1.164 * (Y - 16) + 2.115 * (Cb - 128)  # NOQA: E221,E501
    # 8-bit YCbCr and RGB data should be saturated at the 0 and 255 levels
    return (yuvcommon.normalize(R), yuvcommon.normalize(G), yuvcommon.normalize(B))


# YCoCg Color Space (https://en.wikipedia.org/wiki/YCoCg)
def convert_rgb2yuv_ycocg(R, G, B):
    Y = (R >> 2) + (G >> 1) + (B >> 2)  # NOQA: E221,E222
    Co = (R >> 1) - (B >> 1)  # NOQA: E221,E222
    Cg = (-R >> 2) + (G >> 1) - (B >> 2)  # NOQA: E221,E222
    # no normalization needed
    return Y, Co, Cg


def convert_yuv2rgb_ycocg(Y, Co, Cg):
    R = Y + Co + Cg  # NOQA: E221,E222
    G = Y + Cg  # NOQA: E221,E222
    B = Y - Co - Cg  # NOQA: E221,E222
    # no normalization needed
    return R, G, B


# YCoCg-R Color Space (https://en.wikipedia.org/wiki/YCoCg)
def convert_rgb2yuv_ycocgr(R, G, B):
    Co = R - B
    tmp = B + (Co >> 1)
    Cg = G - tmp
    Y = tmp + (Cg >> 1)
    # no normalization needed
    return Y, Co, Cg


def convert_yuv2rgb_ycocgr(Y, Co, Cg):
    tmp = Y - (Cg >> 1)
    G = Cg + tmp
    B = tmp - (Co >> 1)
    R = B + Co
    # no normalization needed
    return R, G, B


CONVERSION_DIRECTIONS = (
    "yuv2yuv",
    "yuv2rgb",
    "rgb2yuv",
    "rgb2rgb",
)


CONVERSION_FUNCTIONS = {
    "unit": {
        "yuv2yuv": lambda x, y, z: (x, y, z),
        "rgb2rgb": lambda x, y, z: (x, y, z),
    },
    "sdtv.basic": {
        "rgb2yuv": convert_rgb2yuv_sdtv_basic,
        "yuv2rgb": convert_yuv2rgb_sdtv_basic,
    },
    "yiq": {
        "rgb2yuv": convert_rgb2yuv_yiq,
        "yuv2rgb": convert_yuv2rgb_yiq,
    },
    "sdtv.analog": {
        "rgb2yuv": convert_rgb2yuv_ycbcr_sdtv_analog,
        "yuv2rgb": convert_yuv2rgb_ycbcr_sdtv_analog,
    },
    "sdtv.digital": {
        "rgb2yuv": convert_rgb2yuv_ycbcr_sdtv_digital,
        "yuv2rgb": convert_yuv2rgb_ycbcr_sdtv_digital,
    },
    "sdtv.computer": {
        "rgb2yuv": convert_rgb2yuv_ycbcr_sdtv_computer,
        "yuv2rgb": convert_yuv2rgb_ycbcr_sdtv_computer,
    },
    "hdtv.basic": {
        "rgb2yuv": convert_rgb2yuv_hdtv_basic,
        "yuv2rgb": convert_yuv2rgb_hdtv_basic,
    },
    "hdtv.analog": {
        "rgb2yuv": convert_rgb2yuv_ycbcr_hdtv_analog,
        "yuv2rgb": convert_yuv2rgb_ycbcr_hdtv_analog,
    },
    "hdtv.digital": {
        "rgb2yuv": convert_rgb2yuv_ycbcr_hdtv_digital,
        "yuv2rgb": convert_yuv2rgb_ycbcr_hdtv_digital,
    },
    "hdtv.computer": {
        "rgb2yuv": convert_rgb2yuv_ycbcr_hdtv_computer,
        "yuv2rgb": convert_yuv2rgb_ycbcr_hdtv_computer,
    },
    "ycocg": {
        "yuv2rgb": convert_rgb2yuv_ycocg,
        "rgb2yuv": convert_yuv2rgb_ycocg,
    },
    "ycocgr": {
        "yuv2rgb": convert_rgb2yuv_ycocgr,
        "rgb2yuv": convert_yuv2rgb_ycocgr,
    },
}

# per-component range of the matrix output
default_values = {
    "width": 1280,
    "height": 720,
    "ipix_fmt": "yuv420p",
    "opix_fmt": "rgba",
    "conversion_direction": None,
    "conversion_type": None,
    "yuv2yuv": "unit",
    "rgb2rgb": "unit",
    "rgb2yuv": "sdtv.computer",
    "yuv2rgb": "sdtv.computer",
}


def convert_image(idata, w, h, ipix_fmt, conversion_direction, conversion_type, opix_fmt):
    # allocate output array
    odata = array("B")
    oframe_size = int(w * h * yuvcommon.get_length_factor(opix_fmt))
    odata.extend([255] * oframe_size)

    # calculate the conversion direction
    if conversion_direction is None:
        if yuvcommon.is_yuv(ipix_fmt) and yuvcommon.is_yuv(opix_fmt):
            conversion_direction = "yuv2yuv"
        elif yuvcommon.is_yuv(ipix_fmt) and not yuvcommon.is_yuv(opix_fmt):
            conversion_direction = "yuv2rgb"
        elif not yuvcommon.is_yuv(ipix_fmt) and yuvcommon.is_yuv(opix_fmt):
            conversion_direction = "rgb2yuv"
        elif not yuvcommon.is_yuv(ipix_fmt) and not yuvcommon.is_yuv(opix_fmt):
            conversion_direction = "rgb2rgb"

    if conversion_type is None:
        conversion_type = default_values[conversion_direction]
    conversion_function = CONVERSION_FUNCTIONS[conversion_type][
        conversion_direction
    ]

    # convert arrays
    for j in range(0, h):
        for i in range(0, w):
            # get input components
            a, b, c = yuvcommon.get_component_locations(i, j, w, h, ipix_fmt)
            # get output components
            d, e, f = yuvcommon.get_component_locations(i, j, w, h, opix_fmt)
            # color conversion
            x, y, z = conversion_function(idata[a], idata[b], idata[c])
            try:
                odata[d], odata[e], odata[f] = int(x), int(y), int(z)
            except OverflowError:
                print(
                    "error: overflow %s(%i, %i, %i)"
                    % (conversion_function, idata[a], idata[b], idata[c])
                )
                sys.exit(-1)

    return odata


def process_options(options):
    # open input file
    if options.infile == "-":
        options.infile = "/dev/fd/0"
    if options.outfile == "-":
        options.outfile = "/dev/fd/1"
    # read input array
    idata = yuvcommon.read_image(
        options.infile, options.width, options.height, options.ipix_fmt, options.frame_number
    )
    # generate gradient file
    odata = convert_image(
        idata,
        options.width,
        options.height,
        options.ipix_fmt,
        options.conversion_direction,
        options.conversion_type,
        options.opix_fmt,
    )
    # write the output file
    with open(options.outfile, "wb") as fout:
        odata.tofile(fout)


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
        default=0,
        help="Increase verbosity (use multiple times for more)",
    )
    parser.add_argument(
        "--quiet",
        action="store_const",
        dest="debug",
        const=-1,
        help="Zero verbosity",
    )
    parser.add_argument(
        "--width",
        action="store",
        type=int,
        dest="width",
        default=default_values["width"],
        metavar="WIDTH",
        help=("use WIDTH width (default: %i)" % default_values["width"]),
    )
    parser.add_argument(
        "--height",
        action="store",
        type=int,
        dest="height",
        default=default_values["height"],
        metavar="HEIGHT",
        help=("use HEIGHT height (default: %i)" % default_values["height"]),
    )

    class VideoSizeAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            namespace.width, namespace.height = [int(v) for v in values[0].split("x")]

    parser.add_argument(
        "--video_size",
        action=VideoSizeAction,
        nargs=1,
        help="use <width>x<height>",
    )
    parser.add_argument(
        "--ipix_fmt",
        action="store",
        type=str,
        dest="ipix_fmt",
        default=default_values["ipix_fmt"],
        choices=VALID_PIX_FMT,
        metavar="INPUT_PIX_FMT",
        help=(
            "input pixel format %r (default: %s)"
            % (VALID_PIX_FMT, default_values["ipix_fmt"])
        ),
    )
    parser.add_argument(
        "--opix_fmt",
        action="store",
        type=str,
        dest="opix_fmt",
        default=default_values["opix_fmt"],
        choices=VALID_PIX_FMT,
        metavar="OUTPUT_PIX_FMT",
        help=(
            "output pixel format %r (default: %s)"
            % (VALID_PIX_FMT, default_values["opix_fmt"])
        ),
    )
    parser.add_argument(
        "--conversion",
        action="store",
        type=str,
        dest="conversion_type",
        default=default_values["conversion_type"],
        choices=list(CONVERSION_FUNCTIONS.keys()),
        metavar="[%s]"
        % (
            " | ".join(
                list(CONVERSION_FUNCTIONS.keys()),
            )
        ),
        help="conversion type",
    )
    parser.add_argument(
        "--direction",
        action="store",
        type=str,
        dest="conversion_direction",
        default=default_values["conversion_direction"],
        choices=list(CONVERSION_FUNCTIONS.keys()),
        metavar="[%s]"
        % (
            " | ".join(
                list(CONVERSION_FUNCTIONS.keys()),
            )
        ),
        help="conversion direction",
    )
    parser.add_argument(
        "-n", "--frame_number", required=False, help="frame number", type=int, default=0
    )
    parser.add_argument(
        "-i",
        "--infile",
        dest="infile",
        type=str,
        default=None,
        metavar="input-file",
        help="input file",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        dest="outfile",
        type=str,
        default=None,
        metavar="output-file",
        help="output file",
    )
    # do the parsing
    options = parser.parse_args(argv[1:])
    return options


def main(argv):
    # parse options
    options = get_options(argv)
    # print results
    if options.debug > 0:
        print(options)
    # get in/out files
    if options.infile in (None, "-"):
        options.infile = sys.stdin
    if options.outfile in (None, "-"):
        options.outfile = sys.stdout
    process_options(options)


if __name__ == "__main__":
    # at least the CLI program name: (CLI) execution
    main(sys.argv)
