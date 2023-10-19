# yuvconv: An rgb2yuv/yuv2rgb converter

# 1. Introduction

This document describes yuvconv, a tool that converts images between YUV and RGB formats.


# 2. Operation

The tool that converts YUV and RGB images is called `yuvconv.py`.


Example 1: convert a YUV image (nv12) to RGB (rgba) using the   a grayscale gradient (all chroma values are 127, luma gradient is left-to-right)

```
$ ./yuvconv.py -i image/color_eee.nv12.fr.yuv --ipix_fmt nv12 --conversion sdtv.computer --opix_fmt rgba -o image/color_eee.nv12.fr.yuv.rgba
$ ffmpeg -f rawvideo -pixel_format rgba -video_size 1280x720 -i image/color_eee.nv12.fr.yuv.rgba image/color_eee.nv12.fr.yuv.rgba.png
```

![Figure 1](image/color_eee.nv12.fr.yuv.rgba.png)

Figure 1 shows the output of the yuvconv.py script (converted to PNG).
