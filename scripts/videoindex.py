#! /usr/bin/python
# creates a web page with thumbnails for a video folder using pregenerated
# thumbs
#  - caedes@sindominio.net - GPL code

import os

files = os.listdir(".")
files.sort()

for file in files:
    if(file[file.rfind("."):]==".mov"):
	print '<a href="'+ file+ '" ><img src="thumbs/' + file + '.png" /></a>'
	

