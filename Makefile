all: \
    color_eee.nv12.fr.yuv.png color_eee.nv12.lr.yuv.png \
    color_eee.yuv420p.fr.yuv.png color_eee.yuv420p.lr.yuv.png \
    color.nv12.fr.yuv.png color.nv12.lr.yuv.png \
    color.yuv420p.fr.yuv.png color.yuv420p.lr.yuv.png \
    gray.nv12.fr.yuv.png gray.nv12.lr.yuv.png \
    gray.yuv420p.fr.yuv.png gray.yuv420p.lr.yuv.png \
    hdtv.y.fr.nv12.png hdtv.y.lr.nv12.png \
    hdtv.u.fr.nv12.png hdtv.u.lr.nv12.png \
    hdtv.v.fr.nv12.png hdtv.v.lr.nv12.png \
    hdtv.uv.fr.nv12.png hdtv.uv.lr.nv12.png \
    sdtv.y.fr.nv12.png sdtv.y.lr.nv12.png \
    sdtv.u.fr.nv12.png sdtv.u.lr.nv12.png \
    sdtv.v.fr.nv12.png sdtv.v.lr.nv12.png \
    sdtv.uv.fr.nv12.png sdtv.uv.lr.nv12.png


# color_eee
color_eee.nv12.fr.yuv:
	./yuvgrad.py --pix_fmt nv12 --range full --predefined color_eee sources/color_eee.nv12.fr.yuv

color_eee.nv12.fr.yuv.png: color_eee.nv12.fr.yuv
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/color_eee.nv12.fr.yuv sources/color_eee.nv12.fr.yuv.png

color_eee.nv12.lr.yuv:
	./yuvgrad.py --pix_fmt nv12 --range limited --predefined color_eee sources/color_eee.nv12.lr.yuv

color_eee.nv12.lr.yuv.png: color_eee.nv12.lr.yuv
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/color_eee.nv12.lr.yuv sources/color_eee.nv12.lr.yuv.png

color_eee.yuv420p.fr.yuv:
	./yuvgrad.py --pix_fmt yuv420p --range full --predefined color_eee sources/color_eee.yuv420p.fr.yuv

color_eee.yuv420p.fr.yuv.png: color_eee.yuv420p.fr.yuv
	ffmpeg -y -f rawvideo -pixel_format yuv420p -s 1280x720 -i sources/color_eee.yuv420p.fr.yuv sources/color_eee.yuv420p.fr.yuv.png

color_eee.yuv420p.lr.yuv:
	./yuvgrad.py --pix_fmt yuv420p --range limited --predefined color_eee sources/color_eee.yuv420p.lr.yuv

color_eee.yuv420p.lr.yuv.png: color_eee.yuv420p.lr.yuv
	ffmpeg -y -f rawvideo -pixel_format yuv420p -s 1280x720 -i sources/color_eee.yuv420p.lr.yuv sources/color_eee.yuv420p.lr.yuv.png


# color
color.nv12.fr.yuv:
	./yuvgrad.py --pix_fmt nv12 --range full --predefined color sources/color.nv12.fr.yuv

color.nv12.fr.yuv.png: color.nv12.fr.yuv
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/color.nv12.fr.yuv sources/color.nv12.fr.yuv.png

color.nv12.lr.yuv:
	./yuvgrad.py --pix_fmt nv12 --range limited --predefined color sources/color.nv12.lr.yuv

color.nv12.lr.yuv.png: color.nv12.lr.yuv
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/color.nv12.lr.yuv sources/color.nv12.lr.yuv.png

color.yuv420p.fr.yuv:
	./yuvgrad.py --pix_fmt yuv420p --range full --predefined color sources/color.yuv420p.fr.yuv

color.yuv420p.fr.yuv.png: color.yuv420p.fr.yuv
	ffmpeg -y -f rawvideo -pixel_format yuv420p -s 1280x720 -i sources/color.yuv420p.fr.yuv sources/color.yuv420p.fr.yuv.png

color.yuv420p.lr.yuv:
	./yuvgrad.py --pix_fmt yuv420p --range limited --predefined color sources/color.yuv420p.lr.yuv

color.yuv420p.lr.yuv.png: color.yuv420p.lr.yuv
	ffmpeg -y -f rawvideo -pixel_format yuv420p -s 1280x720 -i sources/color.yuv420p.lr.yuv sources/color.yuv420p.lr.yuv.png


# gray
gray.nv12.fr.yuv:
	./yuvgrad.py --pix_fmt nv12 --range full --predefined gray sources/gray.nv12.fr.yuv

gray.nv12.fr.yuv.png: gray.nv12.fr.yuv
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/gray.nv12.fr.yuv sources/gray.nv12.fr.yuv.png

gray.nv12.lr.yuv:
	./yuvgrad.py --pix_fmt nv12 --range limited --predefined gray sources/gray.nv12.lr.yuv

gray.nv12.lr.yuv.png: gray.nv12.lr.yuv
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/gray.nv12.lr.yuv sources/gray.nv12.lr.yuv.png

gray.yuv420p.fr.yuv:
	./yuvgrad.py --pix_fmt yuv420p --range full --predefined gray sources/gray.yuv420p.fr.yuv

gray.yuv420p.fr.yuv.png: gray.yuv420p.fr.yuv
	ffmpeg -y -f rawvideo -pixel_format yuv420p -s 1280x720 -i sources/gray.yuv420p.fr.yuv sources/gray.yuv420p.fr.yuv.png

gray.yuv420p.lr.yuv:
	./yuvgrad.py --pix_fmt yuv420p --range limited --predefined gray sources/gray.yuv420p.lr.yuv

gray.yuv420p.lr.yuv.png: gray.yuv420p.lr.yuv
	ffmpeg -y -f rawvideo -pixel_format yuv420p -s 1280x720 -i sources/gray.yuv420p.lr.yuv sources/gray.yuv420p.lr.yuv.png


# hdtv.y
hdtv.y.fr.nv12:
	./yuvgrad.py --pix_fmt nv12 --range full --predefined hdtv.y sources/hdtv.y.fr.nv12

hdtv.y.fr.nv12.png: hdtv.y.fr.nv12
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/hdtv.y.fr.nv12 sources/hdtv.y.fr.nv12.png

hdtv.y.lr.nv12:
	./yuvgrad.py --pix_fmt nv12 --range limited --predefined hdtv.y sources/hdtv.y.lr.nv12

hdtv.y.lr.nv12.png: hdtv.y.lr.nv12
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/hdtv.y.lr.nv12 sources/hdtv.y.lr.nv12.png


# hdtv.u
hdtv.u.fr.nv12:
	./yuvgrad.py --pix_fmt nv12 --range full --predefined hdtv.u sources/hdtv.u.fr.nv12

hdtv.u.fr.nv12.png: hdtv.u.fr.nv12
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/hdtv.u.fr.nv12 sources/hdtv.u.fr.nv12.png

hdtv.u.lr.nv12:
	./yuvgrad.py --pix_fmt nv12 --range limited --predefined hdtv.u sources/hdtv.u.lr.nv12

hdtv.u.lr.nv12.png: hdtv.u.lr.nv12
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/hdtv.u.lr.nv12 sources/hdtv.u.lr.nv12.png


# hdtv.v
hdtv.v.fr.nv12:
	./yuvgrad.py --pix_fmt nv12 --range full --predefined hdtv.v sources/hdtv.v.fr.nv12

hdtv.v.fr.nv12.png: hdtv.v.fr.nv12
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/hdtv.v.fr.nv12 sources/hdtv.v.fr.nv12.png

hdtv.v.lr.nv12:
	./yuvgrad.py --pix_fmt nv12 --range limited --predefined hdtv.v sources/hdtv.v.lr.nv12

hdtv.v.lr.nv12.png: hdtv.v.lr.nv12
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/hdtv.v.lr.nv12 sources/hdtv.v.lr.nv12.png


# hdtv.uv
hdtv.uv.fr.nv12:
	./yuvgrad.py --pix_fmt nv12 --range full --predefined hdtv.uv sources/hdtv.uv.fr.nv12

hdtv.uv.fr.nv12.png: hdtv.uv.fr.nv12
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/hdtv.uv.fr.nv12 sources/hdtv.uv.fr.nv12.png

hdtv.uv.lr.nv12:
	./yuvgrad.py --pix_fmt nv12 --range limited --predefined hdtv.uv sources/hdtv.uv.lr.nv12

hdtv.uv.lr.nv12.png: hdtv.uv.lr.nv12
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/hdtv.uv.lr.nv12 sources/hdtv.uv.lr.nv12.png


# sdtv.y
sdtv.y.fr.nv12:
	./yuvgrad.py --pix_fmt nv12 --range full --predefined sdtv.y sources/sdtv.y.fr.nv12

sdtv.y.fr.nv12.png: sdtv.y.fr.nv12
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/sdtv.y.fr.nv12 sources/sdtv.y.fr.nv12.png

sdtv.y.lr.nv12:
	./yuvgrad.py --pix_fmt nv12 --range limited --predefined sdtv.y sources/sdtv.y.lr.nv12

sdtv.y.lr.nv12.png: sdtv.y.lr.nv12
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/sdtv.y.lr.nv12 sources/sdtv.y.lr.nv12.png


# sdtv.u
sdtv.u.fr.nv12:
	./yuvgrad.py --pix_fmt nv12 --range full --predefined sdtv.u sources/sdtv.u.fr.nv12

sdtv.u.fr.nv12.png: sdtv.u.fr.nv12
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/sdtv.u.fr.nv12 sources/sdtv.u.fr.nv12.png

sdtv.u.lr.nv12:
	./yuvgrad.py --pix_fmt nv12 --range limited --predefined sdtv.u sources/sdtv.u.lr.nv12

sdtv.u.lr.nv12.png: sdtv.u.lr.nv12
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/sdtv.u.lr.nv12 sources/sdtv.u.lr.nv12.png


# sdtv.v
sdtv.v.fr.nv12:
	./yuvgrad.py --pix_fmt nv12 --range full --predefined sdtv.v sources/sdtv.v.fr.nv12

sdtv.v.fr.nv12.png: sdtv.v.fr.nv12
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/sdtv.v.fr.nv12 sources/sdtv.v.fr.nv12.png

sdtv.v.lr.nv12:
	./yuvgrad.py --pix_fmt nv12 --range limited --predefined sdtv.v sources/sdtv.v.lr.nv12

sdtv.v.lr.nv12.png: sdtv.v.lr.nv12
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/sdtv.v.lr.nv12 sources/sdtv.v.lr.nv12.png


# sdtv.uv
sdtv.uv.fr.nv12:
	./yuvgrad.py --pix_fmt nv12 --range full --predefined sdtv.uv sources/sdtv.uv.fr.nv12

sdtv.uv.fr.nv12.png: sdtv.uv.fr.nv12
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/sdtv.uv.fr.nv12 sources/sdtv.uv.fr.nv12.png

sdtv.uv.lr.nv12:
	./yuvgrad.py --pix_fmt nv12 --range limited --predefined sdtv.uv sources/sdtv.uv.lr.nv12

sdtv.uv.lr.nv12.png: sdtv.uv.lr.nv12
	ffmpeg -y -f rawvideo -pixel_format nv12 -s 1280x720 -i sources/sdtv.uv.lr.nv12 sources/sdtv.uv.lr.nv12.png



