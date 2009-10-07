#!/usr/bin/python
print "Content-type: text/html"
print
import os, sys
import cgi
import socket
form = cgi.FieldStorage() 
from ajaxosc import *
print "<head>" 
print "<title>%s</title>"%(web_title)
print '<link rel="stylesheet" href="'+web_style+'" type="text/css">'
print "</head><body>" 
#print "<strong>Python %s</strong>" % sys.version
#for (x,y) in os.environ.items():
#    print "%s\t%s" % (x, y)

efectos = ["zoom","dice","rotate","phase","blur","contrast","cycle","erode","aging","warhol","radioactiv","simura","ascii","nervous"]
print "<h1>"+web_text_title+"</h1>"
print "<div class='cuadro'>"
print "<p>"
print "<a href='composicion.py'>composicion</a>"
print "efectos"
print "<a href='videos.py'>videos</a>"
print "<a href='imagenes.py'>imagenes</a>"
print "</p>"
#print form.keys()
i = 0
print "<table>"
for efecto in efectos:
        if i == 0:
		print "<tr>"
	print "<td width='80'>"
	print efecto + "<br/>"
	print "<img src='/delvj/images/"+efecto+".png'/><br/>"
	print "<a href='/dataj/efectos.py?"+efecto+"=1'>on</a> <a href='/dataj/efectos.py?"+efecto+"=0'>off</a><br/>"
	print "</td>"
	if form.has_key(efecto):
		envia("/effects/"+efecto,[form.getvalue(efecto)])
	i = i + 1
	if i == 4:
		print "</tr>"
		i = 0
print "</table>"

print "<p><a href='/dataj/efectos.py?quitartodos=1'>Quitar Todos</a></p>"
if form.has_key("quitartodos"):
	envia("/effects/*",[0])
print "</div>"
