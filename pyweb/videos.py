#!/usr/bin/python
print "Content-type: text/html"
print
import os, sys
import os.path
import cgi
import socket, md5
form = cgi.FieldStorage() 
from ajaxosc import *
print "<head>" 
print "<title>%s</title>"%(web_title)
print '<link rel="stylesheet" href="'+web_style+'" type="text/css">'
print "</head><body>" 
#print "<strong>Python %s</strong>" % sys.version
#for (x,y) in os.environ.items():
#    print "%s\t%s" % (x, y)

dirvideos = videos_dir
currdir = ""
if form.has_key("dir"):
	newdir=form.getvalue("dir")
	newdir=newdir.replace("..","")
	dirvideos= dirvideos + newdir
	currdir = newdir
if len(currdir) == currdir.rfind("/")+1:
	currdir = currdir[:currdir.rfind("/")]
lista = os.listdir(dirvideos)
print "<h1>"+web_text_title+"</h1>"
print "<div class='cuadro'>"
print "<p>"
print "<a href='composicion.py'>composicion</a>"
print "<a href='efectos.py'>efectos</a>"
print "videos"
print "<a href='imagenes.py'>imagenes</a>"
print "</p>"
print "<table>"
i = 0
if not currdir == "":
    dir = currdir[:currdir.rfind("/")]
    if dir == "":
    	dir = "directorio raiz"
    print "<tr><td><a href='/dataj/videos.py?dir="+currdir[:currdir.rfind("/")]+"/'>subir a "+dir+"</a></td></tr>"
for elemento in lista:
    if (i == 0):
    	print "<tr>"
    filename = dirvideos +"/" +elemento
    if os.path.isfile(filename):
	fileonly = filename[filename.rfind("/")+1:]
	standardfile = md5.md5("file://"+filename).hexdigest()
	filefinal = "/thumbnails/normal/"+ standardfile+ ".png"
	print "<td><img  src='"+filefinal+"'/><br/>"
	print elemento+" "+str(os.path.getsize(filename)/(1024*1024))+"M<br/>"
	print "<a href='/dataj/efectos.py?quitartodos=1'>lanzar en 1</a> <a href='/dataj/efectos.py?quitartodos=1'>lanzar en 2</a></td>"
	if form.has_key("quitartodos"):
		envia("/effects/*",[0])
    else:
    	print "<td><img src='/delvj/images/folders.png'><a href='/dataj/videos.py?dir="+currdir+"/"+elemento+"'>"+elemento+" ("+str(len(os.listdir(dirvideos+"/"+"/"+elemento)))+")</a></td>"
    i = i+1
    if (i == 4):
        print "</tr>"
	i = 0
print "</div>"
