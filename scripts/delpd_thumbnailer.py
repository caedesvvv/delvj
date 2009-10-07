#! /usr/bin/python
# this script creates video thumbnails according to freedesktop standard
#  - caedes@sindominio.net - GPL code

import os
import os.path
import user
import sys

import popen2

import md5

def create_thumbnail(filename):
    nfilename = os.path.normpath(filename)
    standardfile = md5.md5("file://"+nfilename).hexdigest()
    finalfile=user.home +"/.thumbnails/normal/"+ standardfile+ ".png"
    if (not os.path.exists(finalfile)):
        if(not os.spawnlp(os.P_WAIT,"totem-video-thumbnailer","totem-video-thumbnailer",nfilename,finalfile)):
            print("creado " + finalfile)
	    #popen2.popen2("totem-video-thumbnailer " + filename + " " + finalfile)
	
def do_thumbnails(directory):
    lista = os.listdir(directory);
    for a in lista:
        if (os.path.isdir(directory +"/"+  a)):
	    do_thumbnails(directory +"/"+ a)
	else:
	    create_thumbnail(directory +"/"+ a)
	    
if len(sys.argv)>1:
    do_thumbnails(sys.argv[1])
else:
    do_thumbnails(os.path.realpath(os.path.curdir))

