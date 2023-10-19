#!/usr/bin/env python3

"""yuvgrad unittest usage."""

# http://www.voidspace.org.uk/python/articles/introduction-to-unittest.shtml

import binascii
import unittest
import io

import yuvgrad


TEST_LIST = [
    [
        16,
        4,
        "E",
        10,
        19,
        "S",
        0,
        255,
        "N",
        127,
        127,
        "yuv420p",
        """
        0a0a 0b0b 0c0d 0d0e 0e0f 1010 1111 1213
        0a0a 0b0b 0c0d 0d0e 0e0f 1010 1111 1213
        0a0a 0b0b 0c0d 0d0e 0e0f 1010 1111 1213
        0a0a 0b0b 0c0d 0d0e 0e0f 1010 1111 1213
        0000 0000 0000 0000 ffff ffff ffff ffff
        7f7f 7f7f 7f7f 7f7f 7f7f 7f7f 7f7f 7f7f
    """,
    ],
    [
        16,
        4,
        "E",
        10,
        19,
        "S",
        0,
        255,
        "N",
        127,
        127,
        "nv12",
        """
        0a0a 0b0b 0c0d 0d0e 0e0f 1010 1111 1213
        0a0a 0b0b 0c0d 0d0e 0e0f 1010 1111 1213
        0a0a 0b0b 0c0d 0d0e 0e0f 1010 1111 1213
        0a0a 0b0b 0c0d 0d0e 0e0f 1010 1111 1213
        007f 007f 007f 007f 007f 007f 007f 007f
        ff7f ff7f ff7f ff7f ff7f ff7f ff7f ff7f
    """,
    ],
]


class GenerateGradientFileTestCase(unittest.TestCase):
    def testList(self):
        """Test TEST_LIST"""
        for (
            width,
            height,
            ygrad,
            ymin,
            ymax,
            ugrad,
            umin,
            umax,
            vgrad,
            vmin,
            vmax,
            pix_fmt,
            cont,
        ) in TEST_LIST:
            fout = io.BytesIO()
            yuvgrad.generate_gradient_file(
                fout,
                width,
                height,
                ygrad,
                ymin,
                ymax,
                ugrad,
                umin,
                umax,
                vgrad,
                vmin,
                vmax,
                pix_fmt,
            )
            contents = fout.getvalue()
            expected_contents = binascii.unhexlify(
                cont.replace(" ", "").replace("\n", "")
            )
            self.assertEqual(expected_contents, contents)


if __name__ == "__main__":
    unittest.main()
