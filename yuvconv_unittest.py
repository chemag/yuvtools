#!/usr/bin/env python3

"""yuvconv unittest usage."""

# http://www.voidspace.org.uk/python/articles/introduction-to-unittest.shtml

from array import array
import binascii
import unittest

import yuvconv


TEST_LIST = [
    # yuv2yuv (yuv420p -> yuv420p)
    # ./yuvgrad.py --video_size 16x4 --pix_fmt yuv420p --range limited
    #    --predefined sdtv.uv -  |xxd
    ['yuv420p -> yuv420p', 16, 4, 'yuv420p', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        354a 5f74 8a9f b4ca 354a 5f74 8a9f b4ca
        354d 657d 95ad c5dd 354d 657d 95ad c5dd
    """, None, 'yuv420p', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        354a 5f74 8a9f b4ca 354a 5f74 8a9f b4ca
        354d 657d 95ad c5dd 354d 657d 95ad c5dd
    """],
    # yuv2yuv (yuv420p -> nv12)
    ['yuv420p -> nv12', 16, 4, 'yuv420p', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        354a 5f74 8a9f b4ca 354a 5f74 8a9f b4ca
        354d 657d 95ad c5dd 354d 657d 95ad c5dd
    """, None, 'nv12', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        3535 4a4d 5f65 747d 8a95 9fad b4c5 cadd
        3535 4a4d 5f65 747d 8a95 9fad b4c5 cadd
    """],
    # yuv2yuv (nv12 -> yuv420p)
    ['nv12 -> yuv420p', 16, 4, 'nv12', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        3535 4a4d 5f65 747d 8a95 9fad b4c5 cadd
        3535 4a4d 5f65 747d 8a95 9fad b4c5 cadd
    """, None, 'yuv420p', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        354a 5f74 8a9f b4ca 354a 5f74 8a9f b4ca
        354d 657d 95ad c5dd 354d 657d 95ad c5dd
    """],
    # yuv2yuv (yuv420p -> yuv444p)
    ['yuv420p -> yuv444p', 16, 4, 'yuv420p', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        354a 5f74 8a9f b4ca 354a 5f74 8a9f b4ca
        354d 657d 95ad c5dd 354d 657d 95ad c5dd
    """, None, 'yuv444p', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
    """],
    # yuv2yuv (yuv444p -> yuv420p)
    ['yuv444p -> yuv420p', 16, 4, 'yuv444p', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
    """, None, 'yuv420p', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        354a 5f74 8a9f b4ca 354a 5f74 8a9f b4ca
        354d 657d 95ad c5dd 354d 657d 95ad c5dd
    """],
    # yuv2yuv (nv12 -> yuv444p)
    ['nv12 -> yuv444p', 16, 4, 'nv12', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        3535 4a4d 5f65 747d 8a95 9fad b4c5 cadd
        3535 4a4d 5f65 747d 8a95 9fad b4c5 cadd
    """, None, 'yuv444p', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
    """],
    # yuv2yuv (yuv444p -> nv12)
    ['yuv444p -> nv12', 16, 4, 'yuv444p', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
    """, None, 'nv12', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        3535 4a4d 5f65 747d 8a95 9fad b4c5 cadd
        3535 4a4d 5f65 747d 8a95 9fad b4c5 cadd
    """],
    # yuv2yuv (yuv444p -> yuyv422)
    ['yuv444p -> yuyv422', 16, 4, 'yuv444p', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
    """, None, 'yuyv422', """
        9035 8d35 8a4a 884d 855f 8365 8074 7e7d
        7b8a 7995 769f 74ad 71b4 6fc5 6cca 6add
        9035 8d35 8a4a 884d 855f 8365 8074 7e7d
        7b8a 7995 769f 74ad 71b4 6fc5 6cca 6add
        9035 8d35 8a4a 884d 855f 8365 8074 7e7d
        7b8a 7995 769f 74ad 71b4 6fc5 6cca 6add
        9035 8d35 8a4a 884d 855f 8365 8074 7e7d
        7b8a 7995 769f 74ad 71b4 6fc5 6cca 6add
    """],
    # yuv2yuv (yuyv422 -> yuv444p)
    ['yuyv422p -> yuv444p', 16, 4, 'yuyv422', """
        9035 8d35 8a4a 884d 855f 8365 8074 7e7d
        7b8a 7995 769f 74ad 71b4 6fc5 6cca 6add
        9035 8d35 8a4a 884d 855f 8365 8074 7e7d
        7b8a 7995 769f 74ad 71b4 6fc5 6cca 6add
        9035 8d35 8a4a 884d 855f 8365 8074 7e7d
        7b8a 7995 769f 74ad 71b4 6fc5 6cca 6add
        9035 8d35 8a4a 884d 855f 8365 8074 7e7d
        7b8a 7995 769f 74ad 71b4 6fc5 6cca 6add
    """, None, 'yuv444p', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4a4a 5f5f 7474 8a8a 9f9f b4b4 caca
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
        3535 4d4d 6565 7d7d 9595 adad c5c5 dddd
    """],
    # rgb2rgb (rgba -> rgba)
    ['rgba -> rgba', 16, 4, 'rgba', """
        9a00 0aff 9a00 0aff 9b00 0bff 9b00 0bff
        9c00 0cff 9d00 0dff 9d00 0dff 9e00 0eff
        9e00 0eff 9f00 0fff a000 10ff a000 10ff
        a100 11ff a100 11ff a200 12ff a300 13ff
        9a00 0aff 9a00 0aff 9b00 0bff 9b00 0bff
        9c00 0cff 9d00 0dff 9d00 0dff 9e00 0eff
        9e00 0eff 9f00 0fff a000 10ff a000 10ff
        a100 11ff a100 11ff a200 12ff a300 13ff
        9a00 ffff 9a00 ffff 9b00 ffff 9b00 ffff
        9c00 ffff 9d00 ffff 9d00 ffff 9e00 ffff
        9e00 ffff 9f00 ffff a000 ffff a000 ffff
        a100 ffff a100 ffff a200 ffff a300 ffff
        9a00 ffff 9a00 ffff 9b00 ffff 9b00 ffff
        9c00 ffff 9d00 ffff 9d00 ffff 9e00 ffff
        9e00 ffff 9f00 ffff a000 ffff a000 ffff
        a100 ffff a100 ffff a200 ffff a300 ffff
    """, None, 'rgba', """
        9a00 0aff 9a00 0aff 9b00 0bff 9b00 0bff
        9c00 0cff 9d00 0dff 9d00 0dff 9e00 0eff
        9e00 0eff 9f00 0fff a000 10ff a000 10ff
        a100 11ff a100 11ff a200 12ff a300 13ff
        9a00 0aff 9a00 0aff 9b00 0bff 9b00 0bff
        9c00 0cff 9d00 0dff 9d00 0dff 9e00 0eff
        9e00 0eff 9f00 0fff a000 10ff a000 10ff
        a100 11ff a100 11ff a200 12ff a300 13ff
        9a00 ffff 9a00 ffff 9b00 ffff 9b00 ffff
        9c00 ffff 9d00 ffff 9d00 ffff 9e00 ffff
        9e00 ffff 9f00 ffff a000 ffff a000 ffff
        a100 ffff a100 ffff a200 ffff a300 ffff
        9a00 ffff 9a00 ffff 9b00 ffff 9b00 ffff
        9c00 ffff 9d00 ffff 9d00 ffff 9e00 ffff
        9e00 ffff 9f00 ffff a000 ffff a000 ffff
        a100 ffff a100 ffff a200 ffff a300 ffff
    """],
    # yuv2rgb (nv12 -> rgba), SDTV.basic
    ['nv12 -> rgba', 16, 4, 'nv12', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        3535 4a4d 5f65 747d 8a95 9fad b4c5 cadd
        3535 4a4d 5f65 747d 8a95 9fad b4c5 cadd
    """, 'yuv2rgb.sdtv.basic', 'rgba', """
        cc5c fbff c959 f8ff e140 ffff df3e ffff
        f824 ffff f622 ffff ff09 ffff ff07 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        cc5c fbff c959 f8ff e140 ffff df3e ffff
        f824 ffff f622 ffff ff09 ffff ff07 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        cc5c fbff c959 f8ff e140 ffff df3e ffff
        f824 ffff f622 ffff ff09 ffff ff07 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        cc5c fbff c959 f8ff e140 ffff df3e ffff
        f824 ffff f622 ffff ff09 ffff ff07 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
    """],
    # rgb2yuv (rgba -> nv12), SDTV.basic
    ['rgba -> nv12', 16, 4, 'rgba', """
        cc5c fbff c959 f8ff e140 ffff df3e ffff
        f824 ffff f622 ffff ff09 ffff ff07 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        cc5c fbff c959 f8ff e140 ffff df3e ffff
        f824 ffff f622 ffff ff09 ffff ff07 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        cc5c fbff c959 f8ff e140 ffff df3e ffff
        f824 ffff f622 ffff ff09 ffff ff07 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        cc5c fbff c959 f8ff e140 ffff df3e ffff
        f824 ffff f622 ffff ff09 ffff ff07 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
    """, 'rgb2yuv.sdtv.basic', 'nv12', """
        8f8c 8584 7c7a 6e6d 6969 6969 6969 6969
        8f8c 8584 7c7a 6e6d 6969 6969 6969 6969
        8f8c 8584 7c7a 6e6d 6969 6969 6969 6969
        8f8c 8584 7c7a 6e6d 6969 6969 6969 6969
        3434 3c4f 416c 477f 4983 4983 4983 4983
        3434 3c4f 416c 477f 4983 4983 4983 4983
    """],
    # yuv2rgb (nv12 -> rgba), SDTV.analog
    ['nv12 -> rgba', 16, 4, 'nv12', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        3535 4a4d 5f65 747d 8a95 9fad b4c5 cadd
        3535 4a4d 5f65 747d 8a95 9fad b4c5 cadd
    """, 'yuv2rgb.ycbcr.sdtv.analog', 'rgba', """
        26df 0bff 23dc 08ff 42c0 2aff 40be 28ff
        5fa3 4aff 5da1 48ff 7b86 6aff 7984 68ff
        9868 8cff 9666 8aff b54b acff b349 aaff
        d12d cdff cf2b cbff ee10 efff ec0e edff
        26df 0bff 23dc 08ff 42c0 2aff 40be 28ff
        5fa3 4aff 5da1 48ff 7b86 6aff 7984 68ff
        9868 8cff 9666 8aff b54b acff b349 aaff
        d12d cdff cf2b cbff ee10 efff ec0e edff
        26df 0bff 23dc 08ff 42c0 2aff 40be 28ff
        5fa3 4aff 5da1 48ff 7b86 6aff 7984 68ff
        9868 8cff 9666 8aff b54b acff b349 aaff
        d12d cdff cf2b cbff ee10 efff ec0e edff
        26df 0bff 23dc 08ff 42c0 2aff 40be 28ff
        5fa3 4aff 5da1 48ff 7b86 6aff 7984 68ff
        9868 8cff 9666 8aff b54b acff b349 aaff
        d12d cdff cf2b cbff ee10 efff ec0e edff
    """],
    # rgb2yuv (rgba -> nv12), SDTV.analog
    ['rgba -> nv12', 16, 4, 'rgba', """
        26df 0bff 23dc 08ff 42c0 2aff 40be 28ff
        5fa3 4aff 5da1 48ff 7b86 6aff 7984 68ff
        9868 8cff 9666 8aff b54b acff b349 aaff
        d12d cdff cf2b cbff ee10 efff ec0e edff
        26df 0bff 23dc 08ff 42c0 2aff 40be 28ff
        5fa3 4aff 5da1 48ff 7b86 6aff 7984 68ff
        9868 8cff 9666 8aff b54b acff b349 aaff
        d12d cdff cf2b cbff ee10 efff ec0e edff
        26df 0bff 23dc 08ff 42c0 2aff 40be 28ff
        5fa3 4aff 5da1 48ff 7b86 6aff 7984 68ff
        9868 8cff 9666 8aff b54b acff b349 aaff
        d12d cdff cf2b cbff ee10 efff ec0e edff
        26df 0bff 23dc 08ff 42c0 2aff 40be 28ff
        5fa3 4aff 5da1 48ff 7b86 6aff 7984 68ff
        9868 8cff 9666 8aff b54b acff b349 aaff
        d12d cdff cf2b cbff ee10 efff ec0e edff
    """, 'rgb2yuv.ycbcr.sdtv.analog', 'nv12', """
        8f8c 8987 8482 7f7d 7a78 7573 706e 6b69
        8f8c 8987 8482 7f7d 7a78 7573 706e 6b69
        8f8c 8987 8482 7f7d 7a78 7573 706e 6b69
        8f8c 8987 8482 7f7d 7a78 7573 706e 6b69
        3534 4a4d 5e65 737c 8995 9ead b4c5 c9dc
        3534 4a4d 5e65 737c 8995 9ead b4c5 c9dc
    """],
    # yuv2rgb (nv12 -> rgba), SDTV.digital
    ['nv12 -> rgba', 16, 4, 'nv12', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        3535 4a4d 5f65 747d 8a95 9fad b4c5 cadd
        3535 4a4d 5f65 747d 8a95 9fad b4c5 cadd
    """, 'yuv2rgb.ycbcr.sdtv.digital', 'rgba', """
        1def 10ff 19eb 10ff 3ccc 21ff 3aca 1eff
        5dab 45ff 5aa8 43ff 7d89 6aff 7b87 67ff
        9e67 90ff 9b65 8eff be46 b5ff bc43 b2ff
        df24 d9ff dc22 d7ff eb02 ebff fd00 feff
        1def 10ff 19eb 10ff 3ccc 21ff 3aca 1eff
        5dab 45ff 5aa8 43ff 7d89 6aff 7b87 67ff
        9e67 90ff 9b65 8eff be46 b5ff bc43 b2ff
        df24 d9ff dc22 d7ff eb02 ebff fd00 feff
        1def 10ff 19eb 10ff 3ccc 21ff 3aca 1eff
        5dab 45ff 5aa8 43ff 7d89 6aff 7b87 67ff
        9e67 90ff 9b65 8eff be46 b5ff bc43 b2ff
        df24 d9ff dc22 d7ff eb02 ebff fd00 feff
        1def 10ff 19eb 10ff 3ccc 21ff 3aca 1eff
        5dab 45ff 5aa8 43ff 7d89 6aff 7b87 67ff
        9e67 90ff 9b65 8eff be46 b5ff bc43 b2ff
        df24 d9ff dc22 d7ff eb02 ebff fd00 feff
    """],
    # rgb2yuv (rgba -> nv12), SDTV.digital
    ['rgba -> nv12', 16, 4, 'rgba', """
        1def 10ff 19eb 10ff 3ccc 21ff 3aca 1eff
        5dab 45ff 5aa8 43ff 7d89 6aff 7b87 67ff
        9e67 90ff 9b65 8eff be46 b5ff bc43 b2ff
        df24 d9ff dc22 d7ff eb02 ebff fd00 feff
        1def 10ff 19eb 10ff 3ccc 21ff 3aca 1eff
        5dab 45ff 5aa8 43ff 7d89 6aff 7b87 67ff
        9e67 90ff 9b65 8eff be46 b5ff bc43 b2ff
        df24 d9ff dc22 d7ff eb02 ebff fd00 feff
        1def 10ff 19eb 10ff 3ccc 21ff 3aca 1eff
        5dab 45ff 5aa8 43ff 7d89 6aff 7b87 67ff
        9e67 90ff 9b65 8eff be46 b5ff bc43 b2ff
        df24 d9ff dc22 d7ff eb02 ebff fd00 feff
        1def 10ff 19eb 10ff 3ccc 21ff 3aca 1eff
        5dab 45ff 5aa8 43ff 7d89 6aff 7b87 67ff
        9e67 90ff 9b65 8eff be46 b5ff bc43 b2ff
        df24 d9ff dc22 d7ff eb02 ebff fd00 feff
    """, 'rgb2yuv.ycbcr.sdtv.digital', 'nv12', """
        908d 8987 8482 7f7c 7a78 7572 6f6e 6369
        908d 8987 8482 7f7c 7a78 7572 6f6e 6369
        908d 8987 8482 7f7c 7a78 7572 6f6e 6369
        908d 8987 8482 7f7c 7a78 7572 6f6e 6369
        3e33 494c 5f64 737d 8995 9ead b3c4 cadc
        3e33 494c 5f64 737d 8995 9ead b3c4 cadc
    """],
    # yuv2rgb (nv12 -> rgba), SDTV.computer
    ['nv12 -> rgba', 16, 4, 'nv12', """
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        908d 8a88 8583 807e 7b79 7674 716f 6c6a
        3535 4a4d 5f65 747d 8a95 9fad b4c5 cadd
        3535 4a4d 5f65 747d 8a95 9fad b4c5 cadd
    """, 'yuv2rgb.ycbcr.sdtv.computer', 'rgba', """
        1def 00ff 19eb 00ff 3ccc 21ff 3aca 1eff
        5dab 45ff 5aa8 43ff 7d89 6aff 7b87 67ff
        9e67 90ff 9b65 8eff be46 b5ff bc43 b2ff
        df24 d9ff dc22 d7ff ff02 ffff fd00 feff
        1def 00ff 19eb 00ff 3ccc 21ff 3aca 1eff
        5dab 45ff 5aa8 43ff 7d89 6aff 7b87 67ff
        9e67 90ff 9b65 8eff be46 b5ff bc43 b2ff
        df24 d9ff dc22 d7ff ff02 ffff fd00 feff
        1def 00ff 19eb 00ff 3ccc 21ff 3aca 1eff
        5dab 45ff 5aa8 43ff 7d89 6aff 7b87 67ff
        9e67 90ff 9b65 8eff be46 b5ff bc43 b2ff
        df24 d9ff dc22 d7ff ff02 ffff fd00 feff
        1def 00ff 19eb 00ff 3ccc 21ff 3aca 1eff
        5dab 45ff 5aa8 43ff 7d89 6aff 7b87 67ff
        9e67 90ff 9b65 8eff be46 b5ff bc43 b2ff
        df24 d9ff dc22 d7ff ff02 ffff fd00 feff
    """],
    # rgb2yuv (rgba -> nv12), SDTV.computer
    ['rgba -> nv12', 16, 4, 'rgba', """
        1def 00ff 19eb 00ff 3ccc 21ff 3aca 1eff
        5dab 45ff 5aa8 43ff 7d89 6aff 7b87 67ff
        9e67 90ff 9b65 8eff be46 b5ff bc43 b2ff
        df24 d9ff dc22 d7ff ff02 ffff fd00 feff
        1def 00ff 19eb 00ff 3ccc 21ff 3aca 1eff
        5dab 45ff 5aa8 43ff 7d89 6aff 7b87 67ff
        9e67 90ff 9b65 8eff be46 b5ff bc43 b2ff
        df24 d9ff dc22 d7ff ff02 ffff fd00 feff
        1def 00ff 19eb 00ff 3ccc 21ff 3aca 1eff
        5dab 45ff 5aa8 43ff 7d89 6aff 7b87 67ff
        9e67 90ff 9b65 8eff be46 b5ff bc43 b2ff
        df24 d9ff dc22 d7ff ff02 ffff fd00 feff
        1def 00ff 19eb 00ff 3ccc 21ff 3aca 1eff
        5dab 45ff 5aa8 43ff 7d89 6aff 7b87 67ff
        9e67 90ff 9b65 8eff be46 b5ff bc43 b2ff
        df24 d9ff dc22 d7ff ff02 ffff fd00 feff
    """, 'rgb2yuv.ycbcr.sdtv.computer', 'nv12', """
        8f8c 8987 8482 7f7d 7a78 7573 706e 6b69
        8f8c 8987 8482 7f7d 7a78 7573 706e 6b69
        8f8c 8987 8482 7f7d 7a78 7573 706e 6b69
        8f8c 8987 8482 7f7d 7a78 7573 706e 6b69
        3734 494c 5f64 737d 8a94 9ead b3c4 cadd
        3734 494c 5f64 737d 8a94 9ead b3c4 cadd
    """],
    # yuv2rgb (nv12 -> rgba), HDTV.basic
    # ./yuvgrad.py --video_size 16x4 --pix_fmt nv12 --range limited
    #    --predefined hdtv.uv -  |xxd
    ['nv12 -> rgba', 16, 4, 'nv12', """
        aca5 9f99 928c 8680 7973 6d67 605a 544e
        aca5 9f99 928c 8680 7973 6d67 605a 544e
        aca5 9f99 928c 8680 7973 6d67 605a 544e
        aca5 9f99 928c 8680 7973 6d67 605a 544e
        2929 4143 5a5e 7379 8b94 a4af bdca d6e5
        2929 4143 5a5e 7379 8b94 a4af bdca d6e5
    """, 'yuv2rgb.hdtv.basic', 'rgba', """
        e093 ffff d98c fcff f477 ffff ee71 ffff
        ff5a ffff ff54 ffff ff3f ffff ff39 ffff
        ff22 ffff ff1c ffff ff07 ffff ff01 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        e093 ffff d98c fcff f477 ffff ee71 ffff
        ff5a ffff ff54 ffff ff3f ffff ff39 ffff
        ff22 ffff ff1c ffff ff07 ffff ff01 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        e093 ffff d98c fcff f477 ffff ee71 ffff
        ff5a ffff ff54 ffff ff3f ffff ff39 ffff
        ff22 ffff ff1c ffff ff07 ffff ff01 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        e093 ffff d98c fcff f477 ffff ee71 ffff
        ff5a ffff ff54 ffff ff3f ffff ff39 ffff
        ff22 ffff ff1c ffff ff07 ffff ff01 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
    """],
    # rgb2yuv (rgba -> nv12), HDTV.basic
    ['rgba -> nv12', 16, 4, 'rgba', """
        e093 ffff d98c fcff f477 ffff ee71 ffff
        ff5a ffff ff54 ffff ff3f ffff ff39 ffff
        ff22 ffff ff1c ffff ff07 ffff ff01 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        e093 ffff d98c fcff f477 ffff ee71 ffff
        ff5a ffff ff54 ffff ff3f ffff ff39 ffff
        ff22 ffff ff1c ffff ff07 ffff ff01 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        e093 ffff d98c fcff f477 ffff ee71 ffff
        ff5a ffff ff54 ffff ff3f ffff ff39 ffff
        ff22 ffff ff1c ffff ff07 ffff ff01 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
        e093 ffff d98c fcff f477 ffff ee71 ffff
        ff5a ffff ff54 ffff ff3f ffff ff39 ffff
        ff22 ffff ff1c ffff ff07 ffff ff01 ffff
        ff00 ffff ff00 ffff ff00 ffff ff00 ffff
    """, 'rgb2yuv.hdtv.basic', 'nv12', """
        aba4 9b95 8884 7571 605c 4d49 4848 4848
        aba4 9b95 8884 7571 605c 4d49 4848 4848
        aba4 9b95 8884 7571 605c 4d49 4848 4848
        aba4 9b95 8884 7571 605c 4d49 4848 4848
        2929 3144 395f 426e 4c7e 558d 558e 558e
        2929 3144 395f 426e 4c7e 558d 558e 558e
    """],
    # yuv2rgb (nv12 -> rgba), HDTV.analog
    ['nv12 -> rgba', 16, 4, 'nv12', """
        aca5 9f99 928c 8680 7973 6d67 605a 544e
        aca5 9f99 928c 8680 7973 6d67 605a 544e
        aca5 9f99 928c 8680 7973 6d67 605a 544e
        aca5 9f99 928c 8680 7973 6d67 605a 544e
        2929 4143 5a5e 7379 8b94 a4af bdca d6e5
        2929 4143 5a5e 7379 8b94 a4af bdca d6e5
    """, 'yuv2rgb.ycbcr.hdtv.analog', 'rgba', """
        22e4 0aff 1bdd 03ff 3ec7 2aff 38c1 24ff
        5ca9 4bff 56a3 45ff 7a8b 6dff 7485 67ff
        986d 8dff 9267 87ff b750 afff b14a a9ff
        d431 d1ff ce2b cbff f314 f3ff ed0e edff
        22e4 0aff 1bdd 03ff 3ec7 2aff 38c1 24ff
        5ca9 4bff 56a3 45ff 7a8b 6dff 7485 67ff
        986d 8dff 9267 87ff b750 afff b14a a9ff
        d431 d1ff ce2b cbff f314 f3ff ed0e edff
        22e4 0aff 1bdd 03ff 3ec7 2aff 38c1 24ff
        5ca9 4bff 56a3 45ff 7a8b 6dff 7485 67ff
        986d 8dff 9267 87ff b750 afff b14a a9ff
        d431 d1ff ce2b cbff f314 f3ff ed0e edff
        22e4 0aff 1bdd 03ff 3ec7 2aff 38c1 24ff
        5ca9 4bff 56a3 45ff 7a8b 6dff 7485 67ff
        986d 8dff 9267 87ff b750 afff b14a a9ff
        d431 d1ff ce2b cbff f314 f3ff ed0e edff
    """],
    # rgb2yuv (rgba -> nv12), HDTV.analog
    ['rgba -> nv12', 16, 4, 'rgba', """
        22e4 0aff 1bdd 03ff 3ec7 2aff 38c1 24ff
        5ca9 4bff 56a3 45ff 7a8b 6dff 7485 67ff
        986d 8dff 9267 87ff b750 afff b14a a9ff
        d431 d1ff ce2b cbff f314 f3ff ed0e edff
        22e4 0aff 1bdd 03ff 3ec7 2aff 38c1 24ff
        5ca9 4bff 56a3 45ff 7a8b 6dff 7485 67ff
        986d 8dff 9267 87ff b750 afff b14a a9ff
        d431 d1ff ce2b cbff f314 f3ff ed0e edff
        22e4 0aff 1bdd 03ff 3ec7 2aff 38c1 24ff
        5ca9 4bff 56a3 45ff 7a8b 6dff 7485 67ff
        986d 8dff 9267 87ff b750 afff b14a a9ff
        d431 d1ff ce2b cbff f314 f3ff ed0e edff
        22e4 0aff 1bdd 03ff 3ec7 2aff 38c1 24ff
        5ca9 4bff 56a3 45ff 7a8b 6dff 7485 67ff
        986d 8dff 9267 87ff b750 afff b14a a9ff
        d431 d1ff ce2b cbff f314 f3ff ed0e edff
    """, 'rgb2yuv.ycbcr.hdtv.analog', 'nv12', """
        aaa3 9e98 918b 857f 7872 6c66 5f59 534d
        aaa3 9e98 918b 857f 7872 6c66 5f59 534d
        aaa3 9e98 918b 857f 7872 6c66 5f59 534d
        aaa3 9e98 918b 857f 7872 6c66 5f59 534d
        2929 4142 595d 7278 8b94 a3af bdca d5e5
        2929 4142 595d 7278 8b94 a3af bdca d5e5
    """],
    # yuv2rgb (nv12 -> rgba), HDTV.digital
    ['nv12 -> rgba', 16, 4, 'nv12', """
        aca5 9f99 928c 8680 7973 6d67 605a 544e
        aca5 9f99 928c 8680 7973 6d67 605a 544e
        aca5 9f99 928c 8680 7973 6d67 605a 544e
        aca5 9f99 928c 8680 7973 6d67 605a 544e
        2929 4143 5a5e 7379 8b94 a4af bdca d6e5
        2929 4143 5a5e 7379 8b94 a4af bdca d6e5
    """, 'yuv2rgb.ycbcr.hdtv.digital', 'rgba', """
        19f6 10ff 11ee 10ff 39d4 21ff 32cd 1aff
        5ab1 47ff 53aa 40ff 7c8f 6dff 7588 66ff
        9e6d 91ff 9766 8aff c04b b8ff b944 b1ff
        e128 deff da21 d7ff eb06 ebff fd10 feff
        19f6 10ff 11ee 10ff 39d4 21ff 32cd 1aff
        5ab1 47ff 53aa 40ff 7c8f 6dff 7588 66ff
        9e6d 91ff 9766 8aff c04b b8ff b944 b1ff
        e128 deff da21 d7ff eb06 ebff fd10 feff
        19f6 10ff 11ee 10ff 39d4 21ff 32cd 1aff
        5ab1 47ff 53aa 40ff 7c8f 6dff 7588 66ff
        9e6d 91ff 9766 8aff c04b b8ff b944 b1ff
        e128 deff da21 d7ff eb06 ebff fd10 feff
        19f6 10ff 11ee 10ff 39d4 21ff 32cd 1aff
        5ab1 47ff 53aa 40ff 7c8f 6dff 7588 66ff
        9e6d 91ff 9766 8aff c04b b8ff b944 b1ff
        e128 deff da21 d7ff eb06 ebff fd10 feff
    """],
    # rgb2yuv (rgba -> nv12), HDTV.digital
    ['rgba -> nv12', 16, 4, 'rgba', """
        19f6 10ff 11ee 10ff 39d4 21ff 32cd 1aff
        5ab1 47ff 53aa 40ff 7c8f 6dff 7588 66ff
        9e6d 91ff 9766 8aff c04b b8ff b944 b1ff
        e128 deff da21 d7ff eb06 ebff fd10 feff
        19f6 10ff 11ee 10ff 39d4 21ff 32cd 1aff
        5ab1 47ff 53aa 40ff 7c8f 6dff 7588 66ff
        9e6d 91ff 9766 8aff c04b b8ff b944 b1ff
        e128 deff da21 d7ff eb06 ebff fd10 feff
        19f6 10ff 11ee 10ff 39d4 21ff 32cd 1aff
        5ab1 47ff 53aa 40ff 7c8f 6dff 7588 66ff
        9e6d 91ff 9766 8aff c04b b8ff b944 b1ff
        e128 deff da21 d7ff eb06 ebff fd10 feff
        19f6 10ff 11ee 10ff 39d4 21ff 32cd 1aff
        5ab1 47ff 53aa 40ff 7c8f 6dff 7588 66ff
        9e6d 91ff 9766 8aff c04b b8ff b944 b1ff
        e128 deff da21 d7ff eb06 ebff fd10 feff
    """, 'rgb2yuv.ycbcr.hdtv.digital', 'nv12', """
        aca5 9e98 918b 847e 7872 6c66 5f59 4c57
        aca5 9e98 918b 847e 7872 6c66 5f59 4c57
        aca5 9e98 918b 847e 7872 6c66 5f59 4c57
        aca5 9e98 918b 847e 7872 6c66 5f59 4c57
        3427 4042 595d 7379 8a94 a4ae bdc9 d0de
        3427 4042 595d 7379 8a94 a4ae bdc9 d0de
    """],
    # yuv2rgb (nv12 -> rgba), HDTV.computer
    ['nv12 -> rgba', 16, 4, 'nv12', """
        aca5 9f99 928c 8680 7973 6d67 605a 544e
        aca5 9f99 928c 8680 7973 6d67 605a 544e
        aca5 9f99 928c 8680 7973 6d67 605a 544e
        aca5 9f99 928c 8680 7973 6d67 605a 544e
        2929 4143 5a5e 7379 8b94 a4af bdca d6e5
        2929 4143 5a5e 7379 8b94 a4af bdca d6e5
    """, 'yuv2rgb.ycbcr.hdtv.computer', 'rgba', """
        19f6 00ff 11ee 00ff 39d4 21ff 32cd 1aff
        5ab1 46ff 53aa 3fff 7c8f 6dff 7588 66ff
        9e6d 91ff 9766 8aff c04b b8ff b944 b1ff
        e128 deff da21 d7ff ff06 ffff fd00 feff
        19f6 00ff 11ee 00ff 39d4 21ff 32cd 1aff
        5ab1 46ff 53aa 3fff 7c8f 6dff 7588 66ff
        9e6d 91ff 9766 8aff c04b b8ff b944 b1ff
        e128 deff da21 d7ff ff06 ffff fd00 feff
        19f6 00ff 11ee 00ff 39d4 21ff 32cd 1aff
        5ab1 46ff 53aa 3fff 7c8f 6dff 7588 66ff
        9e6d 91ff 9766 8aff c04b b8ff b944 b1ff
        e128 deff da21 d7ff ff06 ffff fd00 feff
        19f6 00ff 11ee 00ff 39d4 21ff 32cd 1aff
        5ab1 46ff 53aa 3fff 7c8f 6dff 7588 66ff
        9e6d 91ff 9766 8aff c04b b8ff b944 b1ff
        e128 deff da21 d7ff ff06 ffff fd00 feff
    """],
    # rgb2yuv (rgba -> nv12), HDTV.computer
    ['rgba -> nv12', 16, 4, 'rgba', """
        19f6 00ff 11ee 00ff 39d4 21ff 32cd 1aff
        5ab1 46ff 53aa 3fff 7c8f 6dff 7588 66ff
        9e6d 91ff 9766 8aff c04b b8ff b944 b1ff
        e128 deff da21 d7ff ff06 ffff fd00 feff
        19f6 00ff 11ee 00ff 39d4 21ff 32cd 1aff
        5ab1 46ff 53aa 3fff 7c8f 6dff 7588 66ff
        9e6d 91ff 9766 8aff c04b b8ff b944 b1ff
        e128 deff da21 d7ff ff06 ffff fd00 feff
        19f6 00ff 11ee 00ff 39d4 21ff 32cd 1aff
        5ab1 46ff 53aa 3fff 7c8f 6dff 7588 66ff
        9e6d 91ff 9766 8aff c04b b8ff b944 b1ff
        e128 deff da21 d7ff ff06 ffff fd00 feff
        19f6 00ff 11ee 00ff 39d4 21ff 32cd 1aff
        5ab1 46ff 53aa 3fff 7c8f 6dff 7588 66ff
        9e6d 91ff 9766 8aff c04b b8ff b944 b1ff
        e128 deff da21 d7ff ff06 ffff fd00 feff
    """, 'rgb2yuv.ycbcr.hdtv.computer', 'nv12', """
        aba5 9e98 918b 857f 7872 6c66 5f59 524e
        aba5 9e98 918b 857f 7872 6c66 5f59 524e
        aba5 9e98 918b 857f 7872 6c66 5f59 524e
        aba5 9e98 918b 857f 7872 6c66 5f59 524e
        2d28 4143 595e 7279 8a94 a4af bdc9 d5e4
        2d28 4143 595e 7279 8a94 a4af bdc9 d5e4
    """],
]


class ConvertImageTestCase(unittest.TestCase):
    def dumpToFile(self, data, filename):
        with open(filename, 'wb') as fout:
            data.tofile(fout)

    def testList(self):
        """Test TEST_LIST"""
        i = 0
        for (test_name, width, height, ipix_fmt, icont, conversion_name,
             opix_fmt, ocont) in TEST_LIST:
            print('# %02i: running %s (%s)' % (i, test_name, conversion_name))
            idata = array('B', binascii.unhexlify(
                icont.replace(' ', '').replace('\n', '')))
            odata = yuvconv.convert_image(idata, width, height, ipix_fmt,
                                          conversion_name, opix_fmt)
            self.dumpToFile(idata, '/tmp/yuvconv.%02i.%s' % (i, ipix_fmt))
            self.dumpToFile(odata, '/tmp/yuvconv.%02i.%s' % (i, opix_fmt))
            expected_odata = array('B', binascii.unhexlify(
                ocont.replace(' ', '').replace('\n', '')))
            self.assertEqual(expected_odata, odata, '%s (%s)' % (
                test_name, conversion_name))
            i += 1


if __name__ == "__main__":
    unittest.main()
