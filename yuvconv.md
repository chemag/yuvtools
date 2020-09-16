# yuvconv: An rgb2yuv/yuv2rgb converter

This module converts between YUV and RGB files, using pre-defined or
user-defined matrices.

Examples:

* create a yuv420p grayscale gradient (all chroma values are 127, luma
  gradient is left-to-right)

```
$ ./yuvconv.py out.yuv420p.gray.yuv
$ ffmpeg -f rawvideo -pixel_format yuv420p -video_size 1280x720 -i out.yuv420p.gray.yuv out.yuv420p.gray.yuv.png
```

* create a yuv420p color gradient (luma gradient is left-to-right, U gradient
  is top-down, V gradient is bottom-up

```
$ ./yuvconv.py --umin 0 --umax 256 --vmin 0 --vmax 256 out.yuv420p.yuv
$ ffmpeg -f rawvideo -pixel_format yuv420p -video_size 1280x720 -i out.yuv420p.yuv out.yuv420p.yuv.png
```

* create a nv12 grayscale gradient (all chroma values are 127, luma
  gradient is left-to-right)

```
$ ./yuvconv.py --pix_fmt nv12 out.nv12.gray.yuv
$ ffmpeg -f rawvideo -pixel_format nv12 -video_size 1280x720 -i out.nv12.gray.yuv out.nv12.gray.yuv.png
```

* create a nv12 color gradient (luma gradient is left-to-right, U gradient
  is top-down, V gradient is bottom-up

```
$ ./yuvconv.py --umin 0 --umax 256 --vmin 0 --vmax 256 --pix_fmt nv12 out.nv12.yuv
$ ffmpeg -f rawvideo -pixel_format nv12 -video_size 1280x720 -i out.nv12.yuv out.nv12.yuv.png
```

* create a limited-range, gray gradient

```
$ ./yuvconv.py -d --gray --limited-range /tmp/out.yuv
Namespace(color=None, debug=1, full_range=None, gray=None, height=720, \
  limited_range=None, outfile='/tmp/out.yuv', pix_fmt='yuv420p', umax=128, \
  umin=127, vmax=128, vmin=127, width=1280, ymax=235, ymin=16)
```
