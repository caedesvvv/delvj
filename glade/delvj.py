#! /usr/bin/python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import sys

import pygtk
pygtk.require('2.0')

import gtk
import gtk.glade
import gobject
import popen2
import os
import os.path
import math
import string
import thread
import time
import fileinput
import socket
try:
	import xmms
except:
	class FakeXMMS:
		def is_running(self):
			return False
	xmms = FakeXMMS()
import user
import md5
import urllib2
import codecs

from xml.dom import minidom

#import gconf

global xml
#global gconf_client
#gconf_client = gconf.client_get_default()

global temporizacion_ent_counter
global temporizacion_sal_counter
global timebase
global grabando
global lanzando
global lanzando_texto
global lanzando_texto3d
global totallock
global search
global search3d
global memory
search = ""
search3d = ""
memory = {}
totallock =  thread.allocate_lock()
# FUNCION DE ENVIO AL PD
timebase = time.time() # el tiempo empieza a contar
temporizacion_ent_counter=5
temporizacion_sal_counter=5

macros = gtk.ListStore(str, str);   # tiempo, comando

gtk.glade.bindtextdomain("delvj")
gtk.glade.textdomain("delvj")

keystates={}
from keymapping import keymapping
for a in keymapping.keys():
	keystates[a]=False

try:
	import OSC
except:
	print "OSC module not present (no problem)"

pureosc=False
def envia(mes):
	global memory
	command = mes.strip("\n")
	value = command[command.find(" ")+1:]
	command = command[:command.find(" ")]
	if not pureosc:
		sudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sudp.connect(('',8666))
		sudp.send(mes)
		sudp.close()
	else:
		try:
			valuef=float(value)
			OSC.Message(command, [valuef]).sendlocal(8667)
		except:
			OSC.Message(command, value.split()).sendlocal(8667)
			print command," ",value
	memory[command] = value
	if (grabando):
	    tiempo = time.time()-timebase
	    macros.append(["%1.2f"%(tiempo),mes.strip("\n")])
	

#def envia(mes):
#	r,w = popen2.popen2("pdsend 8666 localhost udp")
#	w.write(mes)
#	r.close()
#	w.close()
#	tiempo = time.time()-timebase
#	if (grabando):
#	    macros.append(["%1.2f"%(tiempo),mes.strip("\n")])
	

grabando = 0
lanzando = 0
lanzando_texto = 0
lanzando_texto3d = 0

gtk.threads_init()

# create widget tree ...
if len(sys.argv) > 1:
    fname = sys.argv[1]
else:
    fname = '/usr/share/delvj/glade/delvj.glade'
xml = gtk.glade.XML(fname)

# XXX no parece q funcione
#gtk.gdk.keyboard_grab(xml.get_widget("window1").get_root_window(),True)

if os.path.exists("/usr/share/delvj"):
	xml.get_widget("selector_png3d").set_current_folder("/usr/share/delvj/sprites/")
	xml.get_widget("selector_png").set_current_folder("/usr/share/delvj/sprites/")
	xml.get_widget("filechooserdialog_cal3d").set_current_folder("/usr/share/delvj/cal3d/")
	xml.get_widget("filechooserdialog_textos").set_current_folder("/usr/share/delvj/textos/")
	xml.get_widget("filechooserdialog_textos3d").set_current_folder("/usr/share/delvj/textos/")


def on_png_launch3d1_clicked(*args):
	videosel = xml.get_widget("selector_png3d")
	file = videosel.get_filename()
	folder = videosel.get_current_folder()
	envia("/3dp/textureunit/img1/image load "+file+" 0 0\n")
	envia("/3dp/textureunit/img1/dir location "+folder+"\n")
	update_preview_widget(file, "prev_imagen1")
	update_preview_widget(file, "image_prev_img1",128)
	sync_prev(5)
def on_png_launch_clicked3d(*args):
	on_png_launch3d1_clicked(*args)
def on_png_launch3d2_clicked(*args):
	videosel = xml.get_widget("selector_png3d")
	file = videosel.get_filename()
	folder = videosel.get_current_folder()
	envia("/3dp/textureunit/img2/image load "+file+" 0 0\n")
	envia("/3dp/textureunit/img2/dir location "+folder+"\n")
	update_preview_widget(file, "prev_imagen2")
	update_preview_widget(file, "image_prev_img2",128)
	sync_prev(6)
def on_png_launch3d3_clicked(*args):
	videosel = xml.get_widget("selector_png3d")
	file = videosel.get_filename()
	folder = videosel.get_current_folder()
	envia("/3dp/textureunit/img3/image load "+file+" 0 0\n")
	envia("/3dp/textureunit/img3/dir location "+folder+"\n")
	update_preview_widget(file, "prev_imagen3")
	update_preview_widget(file, "image_prev_img3",128)
	sync_prev(7)
def on_png_launch3d4_clicked(*args):
	videosel = xml.get_widget("selector_png3d")
	file = videosel.get_filename()
	folder = videosel.get_current_folder()
	envia("/3dp/textureunit/img4/image load "+file+" 0 0\n")
	envia("/3dp/textureunit/img4/dir location "+folder+"\n")
	update_preview_widget(file, "prev_imagen4")
	update_preview_widget(file, "image_prev_img4",128)
	sync_prev(8)

def launch_image3d(file,folder):
	if (xml.get_widget("png_textura1").get_active()):
		on_png_launch3d1_clicked()
	elif (xml.get_widget("png_textura2").get_active()):
		on_png_launch3d2_clicked()
	elif (xml.get_widget("png_textura3").get_active()):
		on_png_launch3d3_clicked()
	elif (xml.get_widget("png_textura4").get_active()):
		on_png_launch3d4_clicked()

# BUSQUEDA EN GOOGLE
def png_google_search(search):
	rsearch = string.replace(search," ","%20")
	ssearch = string.replace(search," ","+")
	url = "http://images.google.com/images?q="+rsearch
	print url
	urllib2.socket.setdefaulttimeout(3)
	txdata = None
	txheaders = {   
	    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
	    'Accept-Language': 'en-us',
    	    'Keep-Alive': '3',
    	    'Connection': 'keep-alive',
    	    'Connection': 'delay=3',
    	    'Cache-Control': 'max-age=0',
	}

	req = urllib2.Request(url,txdata,txheaders)
	URL =urllib2.urlopen(req)
	DATA = URL.read()
	imgdir =  user.home+"/.delVj/autoimages/"+ssearch+"/"
	if (not os.path.exists(imgdir)):
	    os.mkdir(imgdir)
	imglist = ()


	number = 0
	index = 0
	index = DATA.find("<b>",index+1)
	index = DATA.find("<b>",index+1)
	index = DATA.find("<b>",index+1)
	index = DATA.find("<b>",index+1)
	index = DATA.find("<b>",index+1)
	index = DATA.find("<b>",index+1)  # el cuarto for
	number_text = DATA[index+3:DATA.find("</b>",index+1)]
	number_text = number_text.replace(".","")
	number_text = number_text.replace(",","")
	print number_text
	if (number_text.isdigit()):
		number = string.atof(number_text)
	index = 0
	while (index != -1):
    		index = DATA.find("<img",index)
    		if (index!=-1):
        		index = DATA.find("imgurl",index)
        		index = DATA.find('=',index)
        		end   = DATA.find('&',index+1)
			if (DATA[index+1:end] not in imglist):
	    			imglist = imglist + (DATA[index+1:end],)
	print(imglist)

	for image in imglist:
   	 try:
     	  if (image.find("http://") == -1):
        	imageurl = url + image
     	  else:
        	imageurl = image
     	  print imageurl
     	  req = urllib2.Request(imageurl,txdata,txheaders)
     	  f =urllib2.urlopen(req)
     	  g = f.read()
     	  filefile = imgdir+image[image.rfind("/")+1:]
     	  file = open(filefile, "wb")
     	  file.write(g)
      	  file.close()
     	  if (image.find("jpg")!=-1 or image.find("png")!=-1 or image.find("jpeg")!=-1 or image.find("JPG")!=-1 or image.find("gif")!=-1 or image.find("GIF")!=-1):
	  	launch_image3d(filefile,imgdir)
		#envia("/image/load load "+filefile+" 1 1\n")
   	 except:
     		print "la imagen no existe"

def png_google_search3d(search3d):
	rsearch = string.replace(search3d," ","%20")
	ssearch = string.replace(search3d," ","+")
	url = "http://images.google.com/images?q="+rsearch
	print url
	urllib2.socket.setdefaulttimeout(3)
	txdata = None
	txheaders = {   
	    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
	    'Accept-Language': 'en-us',
    	    'Keep-Alive': '3',
    	    'Connection': 'keep-alive',
    	    'Connection': 'delay=3',
    	    'Cache-Control': 'max-age=0',
	}

	req = urllib2.Request(url,txdata,txheaders)
	URL =urllib2.urlopen(req)
	DATA = URL.read()
	imgdir =  user.home+"/.delVj/autoimages/"+ssearch+"/"
	if (not os.path.exists(imgdir)):
	    os.mkdir(imgdir)
	imglist = ()


	number = 0
	index = 0
	index = DATA.find("<b>",index+1)
	index = DATA.find("<b>",index+1)
	index = DATA.find("<b>",index+1)
	index = DATA.find("<b>",index+1)
	index = DATA.find("<b>",index+1)
	index = DATA.find("<b>",index+1)  # el cuarto for
	number_text = DATA[index+3:DATA.find("</b>",index+1)]
	number_text = number_text.replace(".","")
	number_text = number_text.replace(",","")
	print number_text
	if (number_text.isdigit()):
		number = string.atof(number_text)
	index = 0
	while (index != -1):
    		index = DATA.find("<img",index)
    		if (index!=-1):
        		index = DATA.find("imgurl",index)
        		index = DATA.find('=',index)
        		end   = DATA.find('&',index+1)
			if (DATA[index+1:end] not in imglist):
	    			imglist = imglist + (DATA[index+1:end],)
	for image in imglist:
   	 try:
     	  if (image.find("http://") == -1):
        	imageurl = url + image
     	  else:
        	imageurl = image
     	  print imageurl
     	  req = urllib2.Request(imageurl,txdata,txheaders)
     	  f =urllib2.urlopen(req)
     	  g = f.read()
     	  filefile = imgdir+image[image.rfind("/")+1:]
     	  file = open(filefile, "wb")
     	  file.write(g)
      	  file.close()
     	  if (image.find("jpg")!=-1 or image.find("png")!=-1 or image.find("jpeg")!=-1 or image.find("JPG")!=-1):
        	print "enviando "+"/image/load load "+filefile+" 0 0\n"
		envia("/image/load load "+filefile+" 1 1\n")
   	 except:
     		print "la imagen no existe"

	
# MODELO DE MACROS
modelo_todas_macros = gtk.ListStore(str);   # nombre
modelo_textos = gtk.ListStore(str);   # texto
modelo_textos3d = gtk.ListStore(str);   # texto
dirsecuencias = user.home + "/.delVj/"
if (not os.path.exists(dirsecuencias)):
    os.mkdir(dirsecuencias)
lista = os.listdir(dirsecuencias);
for a in lista:
	modelo_todas_macros.append([a])

modelo_textos.append(['openeeg delremix of the alpha and beta waves'])
modelo_textos3d.append(['openeeg 3d delremix of the alpha and beta waves'])
# MODELO DE RSS
modelo_rssfeeds = gtk.ListStore(str, str);   # tiempo, comando

modelo_rssfeeds.append(['Barrapunto',"http://barrapunto.com/barrapunto.rss"])
modelo_rssfeeds.append(['CrystalSpace',"http://crystal.sourceforge.net/tikiwiki/tiki-articles_rss.php?ver=2"])
modelo_rssfeeds.append(['Indymedia Global',"http://indymedia.org/global.1-0.rss"])
modelo_rssfeeds.append(['Sindominio',"http://sindominio.net/novedades.rdf"])
modelo_rssfeeds.append(['Creative Commons Weblog',"http://creativecommons.org/weblog/rss"])
modelo_rssfeeds.append(['Archive.org',"http://www.archive.org/services/collection-rss.php"])
modelo_rssfeeds.append(['Indymedia BCN',"http://barcelona.indymedia.org/newswire.rss"])
modelo_rssfeeds.append(['Suburbia',"http://sindominio.net/suburbia/backend.php3"])
modelo_rssfeeds.append(['Viquipedia',"http://ca.wikipedia.org/w/index.php?title=Especial:Recentchanges&feed=rss"])
modelo_rssfeeds.append(['Wikipedia',"http://wikipedia.org/w/index.php?title=Especial:Recentchanges&feed=rss"])
modelo_rssfeeds.append(['Indymedia Estrecho',"http://estrecho.indymedia.org/newsfeed.1-0.rdf"])
modelo_rssfeeds.append(['Context Weblog',"http://straddle3.net/context/index.rdf"])




# RSS CODE

def loadRSS(rssURL):
	urllib2.socket.setdefaulttimeout(3)
	return minidom.parse(urllib2.urlopen(rssURL))
	
DEFAULT_NAMESPACES = \
(None, # RSS 0.91, 0.92, 0.93, 0.94, 2.0
'http://purl.org/rss/1.0/', # RSS 1.0
'http://my.netscape.com/rdf/simple/0.9/' # RSS 0.90
)

def getElementsByTagName(node, tagName, possibleNamespaces=DEFAULT_NAMESPACES):
        for namespace in possibleNamespaces:
               children = node.getElementsByTagNameNS(namespace, tagName)
               if len(children): return children
	return []

def firstRSS(node, tagName, possibleNamespaces=DEFAULT_NAMESPACES):
        children = getElementsByTagName(node, tagName, possibleNamespaces)
	return len(children) and children[0] or None

def textOf(node):
	return node and "".join([child.data for child in node.childNodes]) or ""

DUBLIN_CORE = ('http://purl.org/dc/elements/1.1/',)

#if __name__ == '__main__':
#        import sys

def openRSS(rssURL):
    rsslines = ()
    rssDocument = loadRSS(rssURL)
    for item in getElementsByTagName(rssDocument, 'item'):
        rsslines = rsslines + (textOf(firstRSS(item, 'title')),)
    return rsslines
	

# TECLADO
def on_window1_key_press_event(window,event):
	keyname=event.string
	if keyname in keymapping:
		val="0"
		if keystates[keyname]:
			keystates[keyname]=False
		else:
			val="1"
			keystates[keyname]=True
		envia(keymapping[keyname]+" "+val+"\n")
		print keymapping[keyname]+" "+val

def on_window1_key_release_event(window,event):
	print "RELEASED:",event.string,event.keyval,event.state,event.hardware_keycode

# WIDGETS DE PREVIEW
# prev_mezcla
prev_video1 = xml.get_widget("prev_video1")
prev_video2 = xml.get_widget("prev_video2")
prev_webcam = xml.get_widget("prev_webcam")
prev_imagen1 = xml.get_widget("prev_imagen1")
prev_imagen2 = xml.get_widget("prev_imagen2")
prev_imagen3 = xml.get_widget("prev_imagen3")
prev_imagen4 = xml.get_widget("prev_imagen4")
prev_objects = ["screen2","ball1","ball2","storm","cal3d1","cal3d2","cubes"]
def sync_prev(prev_i):
    	pwid = xml.get_widget("3dp_object_tex"+str(prev_i)+"_screen1")
    	pixbuf = pwid.get_children()[0].get_children()[0].get_pixbuf()
	for obj in prev_objects:
		prev = xml.get_widget("3dp_object_tex"+str(prev_i)+"_"+obj)
		prev.get_children()[0].get_children()[0].set_from_pixbuf(pixbuf)

def sync_prevs():
    for i in range(1,9):
    	sync_prev(i)


sync_prevs()
#print prev.sdad
#prev_video1.set_from_pixbuf(preview2.get_pixbuf())


# MENU CONTEXTUAL
def on_composicion_3d_activate(*args):
    NotebookModos = xml.get_widget("notebook1");
    NotebookModos.set_current_page(0);
def on_efectos1_activate(*args):
    NotebookModos = xml.get_widget("notebook1");
    NotebookModos.set_current_page(1);
def on_videos1_activate(*args):
    NotebookModos = xml.get_widget("notebook1");
    NotebookModos.set_current_page(2);
def on_imagenes1_activate(*args):
    NotebookModos = xml.get_widget("notebook1");
    NotebookModos.set_current_page(3);
def on_textos1_activate(*args):
    NotebookModos = xml.get_widget("notebook1");
    NotebookModos.set_current_page(4);
def on_xmms_control1_activate(*args):
    NotebookModos = xml.get_widget("notebook1");
    NotebookModos.set_current_page(5);
def on_secuencias1_activate(*args):
    NotebookModos = xml.get_widget("notebook1");
    NotebookModos.set_current_page(6);
def on_configuracion1_activate(*args):
    NotebookModos = xml.get_widget("notebook1");
    NotebookModos.set_current_page(7);
    
 
def on_general1_activate(*args):
    xml.get_widget("notebook1").set_current_page(0)
    xml.get_widget("notebook_3dp").set_current_page(0)
def on_pantalla_1_activate(*args):
    xml.get_widget("notebook1").set_current_page(0)
    xml.get_widget("notebook_3dp").set_current_page(1)
def on_pantalla_2_activate(*args):
    xml.get_widget("notebook1").set_current_page(0)
    xml.get_widget("notebook_3dp").set_current_page(2)
def on_bola_1_activate(*args):
    xml.get_widget("notebook1").set_current_page(0)
    xml.get_widget("notebook_3dp").set_current_page(3)
def on_bola_2_activate(*args):
    xml.get_widget("notebook1").set_current_page(0)
    xml.get_widget("notebook_3dp").set_current_page(4)
def on_tormenta1_activate(*args):
    xml.get_widget("notebook1").set_current_page(0)
    xml.get_widget("notebook_3dp").set_current_page(5)
def on_cangrejo1_activate(*args):
    xml.get_widget("notebook1").set_current_page(0)
    xml.get_widget("notebook_3dp").set_current_page(6)
def on_electric_ball1_activate(*args):
    xml.get_widget("notebook1").set_current_page(0)
    xml.get_widget("notebook_3dp").set_current_page(7)
def on_explosion1_activate(*args):
    xml.get_widget("notebook1").set_current_page(0)
    xml.get_widget("notebook_3dp").set_current_page(8)
def on_cubitos1_activate(*args):
    xml.get_widget("notebook1").set_current_page(0)
    xml.get_widget("notebook_3dp").set_current_page(9)
def on_cal3d1_activate(*args):
    xml.get_widget("notebook1").set_current_page(0)
    xml.get_widget("notebook_3dp").set_current_page(10)
def on_cal3d2_activate(*args):
    xml.get_widget("notebook1").set_current_page(0)
    xml.get_widget("notebook_3dp").set_current_page(11)
def on_texto_1_activate(*args):
    xml.get_widget("notebook1").set_current_page(0)
    xml.get_widget("notebook_3dp").set_current_page(12)
def on_texto_2_activate(*args):
    xml.get_widget("notebook1").set_current_page(0)
    xml.get_widget("notebook_3dp").set_current_page(13)

def menu_detach():
	pass
	
def on_menu_popup(widget,event):
	menu = xml.get_widget("menu")
	if(event.button==3):
	    menu.popup(None,None,None,event.button,event.get_time())
	


# THREADS
if(xmms.is_running()):
	xmms_vol = xml.get_widget("xmms_volume")
	xmms_shuffle = xml.get_widget("xmms_random")
	xmms_repeat = xml.get_widget("xmms_repeat")
	xmms_vol.set_value(xmms.get_volume()[0])
	xmms_shuffle.set_active(xmms.is_shuffle())
	xmms_repeat.set_active(xmms.is_repeat())
def on_xmms_refrescar_clicked(*args):
    if(xmms.is_running()):
      try:
	tree = xml.get_widget("xmms_list")
	if tree:
		selection = tree.get_selection()
		(model, iter) = selection.get_selected()
		model.clear()
        	playlist_length = xmms.get_playlist_length()
        	p=playlist_length
        	while (playlist_length>0):
			model.append([xmms.get_playlist_title(p-playlist_length)])
			playlist_length=playlist_length-1
      except:
        pass
        
def google_search():
     global search
     while(1):
     	if (search!=""):
		png_google_search(search)
		search=""
     	time.sleep(1)
def google_search3d():
     global search3d
     while(1):
     	if (search3d!=""):
		png_google_search3d(search3d)
		search3d=""
     	time.sleep(1)


def automatizacion(j,i):
     global lanzando
     global totallock
     nmacro = -1
     tlanzado = time.time()
     veces = 0
     while(1):
	if (lanzando):
	    if (nmacro == -1):	# empezamos ahora
	        nmacro = 0
		tlanzado = time.time()
	    gtk.threads_enter()
	    tree = xml.get_widget("treeview_macros")
	    model = tree.get_model()
	    if (nmacro<len(model)):
	        iter = model.get_iter(nmacro)
		tex = model.get_value(iter,1)
		val = string.atof(model.get_value(iter,0))
		if (val < time.time()-tlanzado):
		    envia(tex + "\n")
		    selection = tree.get_selection()
		    selection.select_iter(iter)
	            nmacro = nmacro +1
	    else:
	        totallock.acquire()
	        lanzando = 0
		totallock.release()
		nmacro = -1
	        xml.get_widget("button_todas_macros_nueva").set_sensitive(1)
	        xml.get_widget("button_todas_macros_borrar").set_sensitive(1)
	        xml.get_widget("button_macros_grabar").set_sensitive(1)
	        xml.get_widget("button_macros_1o_a_0").set_sensitive(1)
	        xml.get_widget("button_macros_a_0").set_sensitive(1)
	        xml.get_widget("button_macros_limpiar").set_sensitive(1)
	        xml.get_widget("treeview_todas_macros").set_sensitive(1)
	        xml.get_widget("treeview_macros").set_sensitive(1)
	
		# parar el sistema de lanzado o empezar otra vez
	    veces = veces + 1
	    if (veces == 10):
	        xml.get_widget("todas_macros_time").set_text("%5.2f" % (time.time()-tlanzado))
		veces = 0
	    gtk.threads_leave()
	    time.sleep(0.03)	# resolucion del temporizador
	else:
	    time.sleep(0.1)
def xmms_control(j,i):
    global lanzando_texto
    global lanzando_texto3d
    ncanciones = 0
    pcanciones = 0
    contador_texto = 0
    contador_texto3d = 0
    while (1):
      # automatizacion del xmms
      if(xmms.is_running()):
        ncanciones = xmms.get_playlist_length()
	if (ncanciones != pcanciones):
	     pcanciones = ncanciones
	     gtk.threads_enter()
	     on_xmms_refrescar_clicked()
	     gtk.threads_leave()
	xmmspos = xmms.get_playlist_pos()
	gtk.threads_enter()
	cancionw = xml.get_widget("cancion_actual")
	titulo_cancion = xmms.get_playlist_title(xmmspos)
	if cancionw:
		if titulo_cancion:
			cancionw.set_text("%s" % titulo_cancion)
		else:
			cancionw.set_text("Sin Cancion")
	gtk.threads_leave()
      # automatizacion de textos
      if (lanzando_texto3d):
        contador_texto3d = contador_texto3d + 1
	gtk.threads_enter()
	seg3d = xml.get_widget("spinbutton_auto_textos_segundos3d").get_value()
	if(contador_texto3d >= seg3d):
	  contador_texto3d = 0
      	  tree = xml.get_widget("treeview_textos3d")
	  model = tree.get_model()
	  iter = model.get_iter_first()
	  if (iter!=None):
	    texto = model.get_value(iter, 0)
	    model.remove(iter)
	    if xml.get_widget("checkbutton_auto_textos_reutilizar3d").get_active():
		model.append([texto])
	    if (xml.get_widget("autotexto_lanzar_3d1").get_active()):
	    	texto = codecs.charmap_encode(texto)
		envia("/3dp/text1/text text %s\n" % (texto[0]))
	    if (xml.get_widget("autotexto_lanzar_3d2").get_active()):
	    	texto = codecs.charmap_encode(texto)
		envia("/3dp/text2/text text %s\n" % (texto[0]))
	gtk.threads_leave()
      if (lanzando_texto):
        contador_texto = contador_texto + 1
	gtk.threads_enter()
	seg = xml.get_widget("spinbutton_auto_textos_segundos").get_value()
	if(contador_texto >= seg):
	  contador_texto = 0
      	  tree = xml.get_widget("treeview_textos")
	  model = tree.get_model()
	  iter = model.get_iter_first()
	  if (iter!=None):
	      texto = model.get_value(iter, 0)
	      model.remove(iter)
	      if xml.get_widget("checkbutton_auto_textos_reutilizar").get_active():
		model.append([texto])
	      entradax = xml.get_widget("texto_x")
	      x = entradax.get_text()
	      entraday = xml.get_widget("texto_y")
	      y = entraday.get_text()
	      
	      textor = string.replace(texto,"1",'"1"')
	      textor = string.replace(textor,"2",'"2"')
	      textor = string.replace(textor,"3",'"3"')
	      textor = string.replace(textor,"4",'"4"')
	      textor = string.replace(textor,"5",'"5"')
	      textor = string.replace(textor,"6",'"6"')
	      textor = string.replace(textor,"7",'"7"')
	      textor = string.replace(textor,"8",'"8"')
	      textor = string.replace(textor,"9",'"9"')
	      textor = string.replace(textor,"0",'"0"')
	      textor = string.replace(textor,"á",'a')
	      textor = string.replace(textor,"é",'e')
	      textor = string.replace(textor,"í",'i')
	      textor = string.replace(textor,"ó",'o')
	      textor = string.replace(textor,"ú",'u')
	      textor = textor.replace(",",".")
	      textor = textor.replace(";",":")
	      textor = string.replace(textor," ","%32")
	      textof = '/text/text text "' + textor + '" %s' % string.atoi(x)
	      print textof
	      envia(textof+' %s\n' % string.atoi(y))
        gtk.threads_leave()
      time.sleep(1)


# VISTA DE MACROS
back1select = xml.get_widget("treeview_macros")
renderer = gtk.CellRendererText();
renderer2 = gtk.CellRendererText();

column=gtk.TreeViewColumn("Segundos",renderer);
column.add_attribute(renderer, "text",0)
back1select.insert_column(column,0);

column2=gtk.TreeViewColumn("Comandos",renderer);
column2.add_attribute(renderer, "text",1)
back1select.insert_column(column2,1);

back1select.set_model(macros);

# VISTA DE BLUETOOTH
#back1bluez = xml.get_widget("treeview_bluetooth")
#renderer = gtk.CellRendererText();
#renderer2 = gtk.CellRendererText();
#renderer3 = gtk.CellRendererText();

#column=gtk.TreeViewColumn("MAC",renderer);
#column.add_attribute(renderer, "text",0)
#back1bluez.insert_column(column,0);

#column2=gtk.TreeViewColumn("Nombre",renderer);
#column2.add_attribute(renderer, "text",1)
#back1bluez.insert_column(column2,1);

#column3=gtk.TreeViewColumn("Estado",renderer);
#column3.add_attribute(renderer, "text",2)
#back1bluez.insert_column(column3,2);

#back1bluez.set_model(macros);



# VISTA DE TODAS LAS MACROS
back1select = xml.get_widget("treeview_todas_macros")
renderer = gtk.CellRendererText();

column=gtk.TreeViewColumn("Nombre",renderer);
column.add_attribute(renderer, "text",0)
back1select.insert_column(column,0);

back1select.set_model(modelo_todas_macros);

# VISTA DE TODAS LAS MACROS
back1select = xml.get_widget("treeview_textos")
renderer = gtk.CellRendererText();

column=gtk.TreeViewColumn("Texto",renderer);
column.add_attribute(renderer, "text",0)
back1select.insert_column(column,0);

back1select.set_model(modelo_textos);

back1select = xml.get_widget("treeview_textos3d")
renderer = gtk.CellRendererText();

column=gtk.TreeViewColumn("Texto",renderer);
column.add_attribute(renderer, "text",0)
back1select.insert_column(column,0);

back1select.set_model(modelo_textos3d);

# RSS FEED TREEVIEW
back1select = xml.get_widget("treeview_rssfeeds")
renderer = gtk.CellRendererText();

column=gtk.TreeViewColumn("Titulo",renderer);
column.add_attribute(renderer, "text",0)
back1select.insert_column(column,0);

#column=gtk.TreeViewColumn("Url",renderer);
#column.add_attribute(renderer, "text",1)
#back1select.insert_column(column,1);

back1select.set_model(modelo_rssfeeds);
back1select3d = xml.get_widget("treeview_rssfeeds3d")
renderer = gtk.CellRendererText();

column=gtk.TreeViewColumn("Titulo",renderer);
column.add_attribute(renderer, "text",0)
back1select3d.insert_column(column,0);


back1select3d.set_model(modelo_rssfeeds);

#inicializacion interfaz
videosel = xml.get_widget("selector_videos")
filter = gtk.FileFilter()
filter.add_pattern("*.gif")
filter.add_pattern("*.png")
filter.add_pattern("*.jpg")
filter.add_pattern("*.jpeg")
filter.add_pattern("*.mov")
filter.add_pattern("*.mng")
filter.add_pattern("*.avi")
filter.add_pattern("*.mpg")
filter.add_pattern("*.3gp")
filter.add_pattern("*.ogg")
filter.add_pattern("*.mp3")
filter.add_pattern("*.mpeg")
videosel.set_filter(filter)
preview = gtk.Image()
shorts=videosel.list_shortcut_folders()
videosel.set_preview_widget(preview)
videosel.set_use_preview_label(0)

pngsel = xml.get_widget("selector_png")
filter = gtk.FileFilter()
filter.add_pattern("*.png")
filter.add_pattern("*.jpg")
filter.add_pattern("*.bmp")
filter.add_pattern("*.JPG")
filter.add_pattern("*.gif")
pngsel.set_filter(filter)
preview2 = gtk.Image()
shorts=pngsel.list_shortcut_folders()
pngsel.set_preview_widget(preview2)
pngsel.set_use_preview_label(0)
pngsel = xml.get_widget("selector_png3d")
filter = gtk.FileFilter()
filter.add_pattern("*.png")
filter.add_pattern("*.jpg")
filter.add_pattern("*.bmp")
filter.add_pattern("*.JPG")
filter.add_pattern("*.gif")
pngsel.set_filter(filter)
preview2 = gtk.Image()
shorts=pngsel.list_shortcut_folders()
pngsel.set_preview_widget(preview2)
pngsel.set_use_preview_label(0)
preview3 = gtk.Image()


def update_preview_cb(file_chooser, preview):
    filename = videosel.get_preview_filename()
    try:
      fileonly = filename[filename.rfind("/")+1:]
      filetotal = "/var/www/delvj/thumbsvideo/"+fileonly+".png";
      standardfile = md5.md5("file://"+filename).hexdigest()
      pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(user.home +"/.thumbnails/normal/"+ standardfile+ ".png", 128, 128)
      preview.set_from_pixbuf(pixbuf)
      pixbufs = gtk.gdk.pixbuf_new_from_file_at_size(user.home +"/.thumbnails/normal/"+ standardfile+ ".png", 32, 32)
      preview3.set_from_pixbuf(pixbufs)
      have_preview = True
    except:
      have_preview = False
    videosel.set_preview_widget_active(have_preview)
    return

def update_preview_widget(filename, preview_widget_name,size=32):
    preview_widget = xml.get_widget(preview_widget_name)
    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, size, size)
    preview_widget.set_from_pixbuf(pixbuf)

def update_preview_png(file_chooser, preview2):
    filename = pngsel.get_preview_filename()
    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, 128, 128)
    preview2.set_from_pixbuf(pixbuf)
    have_preview = True
    pngsel.set_preview_widget_active(have_preview)
    return

back1select = xml.get_widget("xmms_list")
renderer = gtk.CellRendererText();
column=gtk.TreeViewColumn("Fichero",renderer);
column.add_attribute(renderer,"text",0)
back1select.insert_column(column,0);
renderer1 = gtk.CellRendererText();

# Inicializar ListStoreS
# List Store de Fondos 
s = gtk.ListStore(str);
if(xmms.is_running()):
    playlist_length = xmms.get_playlist_length()
    p=playlist_length
    while (playlist_length>0):
        s.append([xmms.get_playlist_title(p-playlist_length)])
        playlist_length=playlist_length-1

back1select.set_model(s);


#s = gtk.ListStore(str,str,str);
#back1bluez.set_model(s);

videosel.connect("update-preview", update_preview_cb, preview)
pngsel.connect("update-preview", update_preview_png, preview2)
# Funciones de Respuesta al Menu


if(xmms.is_running()):
    cancionw = xml.get_widget("cancion_actual")
    xmmspos = xmms.get_playlist_pos()
    cancionw.set_text(str(xmms.get_playlist_title(xmmspos))+" ")

thread.start_new_thread(automatizacion,("s","f"))
thread.start_new_thread(google_search,())
thread.start_new_thread(google_search3d,())
thread.start_new_thread(xmms_control,("s","f"))
def gtk_main_quit(*args):
    gtk.main_quit()
		



#MENU:

def on_show_me_the_patches1_activate(*args):
	global memory
	popen2.popen2("bash /usr/share/delvj/scripts/pd-sync-gui.sh &")
	memory = {}

def on_arrancar1_activate(*args):
    global memory
    if "GRAPSPATH" in os.environ:
        popen2.popen2("bash /usr/share/delvj/scripts/pd-sync-graps.sh &")
    else:
        popen2.popen2("bash /usr/share/delvj/scripts/pd-sync.sh &")
    memory = {}
	
def on_parar1_activate(*args):
	popen2.popen2("killall -9 pd")

def on_acerca_de1_activate(*args):
	pass

#EFECTOS:
def on_zoom_in_clicked(widget):
	envia("/effects/zoom 1\n")
	if widget.get_active():
		widget.set_active(False)
def on_zoom_out_clicked(widget):
	envia("/effects/zoom 0\n")
	xml.get_widget("zoom_in").set_active(False)
def on_ascii_in_clicked(widget):
	envia("/effects/ascii 1\n")
	if widget.get_active():
		widget.set_active(False)
def on_ascii_out_clicked(*args):
	envia("/effects/ascii 0\n")
	xml.get_widget("ascii_in").set_active(False)
def on_dados_in_clicked(widget):
	envia("/effects/dice 1\n")
	if widget.get_active():
		widget.set_active(False)
def on_dados_out_clicked(*args):
	envia("/effects/dice 0\n")
	xml.get_widget("dados_in").set_active(False)
def on_rotar_in_clicked(widget):
	envia("/effects/rotate 1\n")
	if widget.get_active():
		widget.set_active(False)
def on_rotar_out_clicked(*args):
	envia("/effects/rotate 0\n")
	xml.get_widget("rotar_in").set_active(False)
def on_simura_in_clicked(widget):
	envia("/effects/simura 1\n")
	if widget.get_active():
		widget.set_active(False)
def on_simura_out_clicked(*args):
	envia("/effects/simura 0\n")
	xml.get_widget("simura_in").set_active(False)
def on_eco_in_clicked(widget):
	envia("/effects/phase 1\n")
	if widget.get_active():
		widget.set_active(False)
def on_eco_out_clicked(*args):
	envia("/effects/phase 0\n")
	xml.get_widget("eco_in").set_active(False)
def on_blur_in_clicked(widget):
	envia("/effects/blur 1\n")
	if widget.get_active():
		widget.set_active(False)
def on_blur_out_clicked(*args):
	envia("/effects/blur 0\n")
	xml.get_widget("blur_in").set_active(False)
def on_contraste_in_clicked(widget):
	envia("/effects/contrast 1\n")
	if widget.get_active():
		widget.set_active(False)
def on_contraste_out_clicked(*args):
	envia("/effects/contrast 0\n")
	xml.get_widget("contraste_in").set_active(False)
def on_compose_in_clicked(widget):
	envia("/effects/compose 1\n")
	if widget.get_active():
		widget.set_active(False)
def on_compose_out_clicked(*args):
	envia("/effects/compose 0\n")
	xml.get_widget("compose_in").set_active(False)
def on_cycle_in_clicked(widget):
	envia("/effects/cycle 1\n")
	if widget.get_active():
		widget.set_active(False)
def on_cycle_out_clicked(*args):
	envia("/effects/cycle 0\n")
	xml.get_widget("cycle_in").set_active(False)
def on_erode_in_clicked(widget):
	envia("/effects/erode 1\n")
	if widget.get_active():
		widget.set_active(False)
def on_erode_out_clicked(*args):
	envia("/effects/erode 0\n")
	xml.get_widget("erode_in").set_active(False)
def on_aging_in_clicked(widget):
	envia("/effects/aging 1\n")
	if widget.get_active():
		widget.set_active(False)
def on_aging_out_clicked(*args):
	envia("/effects/aging 0\n")
	xml.get_widget("aging_in").set_active(False)
def on_warhol_in_clicked(widget):
	envia("/effects/warhol 1\n")
	if widget.get_active():
		widget.set_active(False)
def on_warhol_out_clicked(*args):
	envia("/effects/warhol 0\n")
	xml.get_widget("warhol_in").set_active(False)
def on_radioactive_in_clicked(widget):
	envia("/effects/radioactiv 1\n")
	if widget.get_active():
		widget.set_active(False)
def on_radioactive_out_clicked(*args):
	envia("/effects/radioactiv 0\n")
	xml.get_widget("radioactive_in").set_active(False)
def on_nervous_in_clicked(widget):
	envia("/effects/nervous 1\n")
	if widget.get_active():
		widget.set_active(False)
def on_nervous_out_clicked(*args):
	envia("/effects/nervous 0\n")
	xml.get_widget("nervous_in").set_active(False)
# ... ascii, dados, rotar, simura, eco, blur, contraste

#VIDEOS:
def on_video1_fps_value_changed(widget):
	on_value_changed(widget,"/chan1/fps")
def on_video2_fps_value_changed(widget):
	on_value_changed(widget,"/chan2/fps")
def on_video1_player_toggled(widget):
	on_toggle_value(widget,"/chan1/loader/player")
def on_video2_player_toggled(widget):
	on_toggle_value(widget,"/chan2/loader/player")

def on_button_canal1_negro_clicked(*args):
	envia("/chan1/mode 1\n")
def on_button_canal1_video1_clicked(*args):
	envia("/chan1/mode 0\n")
def on_button_canal2_negro_clicked(*args):
	envia("/chan2/mode 1\n")
def on_button_canal2_video2_clicked(*args):
	envia("/chan2/mode 0\n")
def on_video_thumbnail_clicked(*args):
	videosel = xml.get_widget("selector_videos")
	folder = videosel.get_current_folder()
	popen2.popen2('bash -c "cd '+folder+'; python /usr/share/delvj/scripts/delpd_thumbnailer.py '+folder+'&"')

def on_video_preview_clicked(*args):
	videosel = xml.get_widget("selector_videos")
	file = videosel.get_filename()
	popen2.popen2('xine -G 320x240 -l --no-logo --no-splash -g '+file+'&')

def on_lanzar_video_canal1_clicked(*args):
	videosel = xml.get_widget("selector_videos")
	file = videosel.get_filename()
	folder = videosel.get_current_folder()
	envia("/chan1/file open "+file+"\n")
	envia("/chan1/dir location "+folder+"\n")
	prev_vid1 = xml.get_widget("preview_video1")
	prev_vid1.set_from_pixbuf(preview.get_pixbuf())
	prev_vid1 = xml.get_widget("prev_video1")
	prev_vid1.set_from_pixbuf(preview3.get_pixbuf())
	sync_prev(2)
	
def on_lanzar_video_canal2_clicked(*args):
	videosel = xml.get_widget("selector_videos")
	file = videosel.get_filename()
	folder = videosel.get_current_folder()
	envia("/chan2/file open "+file+"\n")
	envia("/chan2/dir location "+folder+"\n")
	prev_vid2 = xml.get_widget("preview_video2")
	prev_vid2.set_from_pixbuf(preview.get_pixbuf())
	prev_vid1 = xml.get_widget("prev_video2")
	prev_vid1.set_from_pixbuf(preview3.get_pixbuf())
	sync_prev(3)

#AUTOMATIZACION:
def on_toggle_value(widget,address):
	if (widget.get_active()):
		envia(address+" 1\n")
	else:
		envia(address+" 0\n")
def on_canal1_auto_ont_toggled(widget):
	on_toggle_value(widget,"/chan1/auto")
def on_canal2_auto_ont_toggled(widget):
	on_toggle_value(widget,"/chan2/auto")
def on_image3d1_auto_ont_toggled(widget):
	on_toggle_value(widget,"/3dp/textureunit/img1/auto")
def on_image3d2_auto_ont_toggled(widget):
	on_toggle_value(widget,"/3dp/textureunit/img2/auto")
def on_image3d3_auto_ont_toggled(widget):
	on_toggle_value(widget,"/3dp/textureunit/img3/auto")
def on_image3d4_auto_ont_toggled(widget):
	on_toggle_value(widget,"/3dp/textureunit/img4/auto")
	
def on_image_auto_ont_toggled(widget):
	on_toggle_value(widget,"/image/auto")

def on_value_changed(widget,address):
	num = widget.get_value()
	envia(address+" %s\n" % num)

def on_image_golpes_value_changed(widget):
	on_value_changed(widget,"/image/beats")
def on_video1_golpes_value_changed(widget):
	on_value_changed(widget,"/chan1/beats")
def on_video2_golpes_value_changed(widget):
	on_value_changed(widget,"/chan2/beats")
def on_imagen3d1_golpes_value_changed(widget):
	on_value_changed(widget,"/3dp/textureunit/img1/beats")
def on_imagen3d2_golpes_value_changed(widget):
	on_value_changed(widget,"/3dp/textureunit/img2/beats")
def on_imagen3d3_golpes_value_changed(widget):
	on_value_changed(widget,"/3dp/textureunit/img3/beats")
def on_imagen3d4_golpes_value_changed(widget):
	on_value_changed(widget,"/3dp/textureunit/img4/beats")

def on_canal1_auto_on_clicked(*args):
	envia("/chan1/auto 1\n")
def on_canal1_auto_off_clicked(*args):
	envia("/chan1/auto 0\n")
def on_canal2_auto_on_clicked(*args):
	envia("/chan2/auto 1\n")
def on_canal2_auto_off_clicked(*args):
	envia("/chan2/auto 0\n")
def on_cambio_canal_on_clicked(*args):
	envia("/effects/swapchannels 1\n")
def on_cambio_canal_off_clicked(*args):
	envia("/effects/swapchannels 0\n")
def on_png_auto_on_clicked(*args):
    if (xml.get_widget("auto_tex_video").get_active()):
	envia("/image/auto 1\n")
    if (xml.get_widget("auto_texture1").get_active()):
	envia("/3dp/textureunit/img1/auto 1\n")
    if (xml.get_widget("auto_texture1").get_active()):
	envia("/3dp/textureunit/img1/auto 1\n")
    if (xml.get_widget("auto_texture2").get_active()):
	envia("/3dp/textureunit/img2/auto 1\n")
    if (xml.get_widget("auto_texture3").get_active()):
	envia("/3dp/textureunit/img3/auto 1\n")
    if (xml.get_widget("auto_texture4").get_active()):
	envia("/3dp/textureunit/img4/auto 1\n")
def on_png_auto_off_clicked(*args):
    if (xml.get_widget("auto_tex_video").get_active()):
	envia("/image/auto 1\n")
    if (xml.get_widget("auto_texture1").get_active()):
	envia("/3dp/textureunit/img1/auto 0\n")
    if (xml.get_widget("auto_texture1").get_active()):
	envia("/3dp/textureunit/img1/auto 0\n")
    if (xml.get_widget("auto_texture2").get_active()):
	envia("/3dp/textureunit/img2/auto 0\n")
    if (xml.get_widget("auto_texture3").get_active()):
	envia("/3dp/textureunit/img3/auto 0\n")
    if (xml.get_widget("auto_texture4").get_active()):
	envia("/3dp/textureunit/img4/auto 0\n")
def on_canal1_golpes_clicked(*args):
	entrada = xml.get_widget("canal1_auto_fichero")
	texto = entrada.get_text()
	num = string.atoi(texto)
	envia("/chan1/beats %s\n" % num)
def on_canal2_golpes_clicked(*args):
	entrada = xml.get_widget("canal2_auto_fichero")
	texto = entrada.get_text()
	num = string.atoi(texto)
	envia("/chan2/beats %s\n" % num)
def on_png_golpes_clicked(*args):
	entrada = xml.get_widget("png_auto_fichero")
	texto = entrada.get_text()
	num = string.atoi(texto)
        if (xml.get_widget("auto_tex_video").get_active()):
		envia("/image/beats %s\n" % num)
        if (xml.get_widget("auto_texture1").get_active()):
		envia("/3dp/textureunit/img1/beats %s\n" % num)
        if (xml.get_widget("auto_texture2").get_active()):
		envia("/3dp/textureunit/img2/beats %s\n" % num)
        if (xml.get_widget("auto_texture3").get_active()):
		envia("/3dp/textureunit/img3/beats %s\n" % num)
        if (xml.get_widget("auto_texture4").get_active()):
		envia("/3dp/textureunit/img4/beats %s\n" % num)

def on_ritmo_in_on_toggled(widget):
	on_toggle_value(widget,"/ritmo/ritmo/musicctl")
def on_graves_in_on_toggled(widget):
	on_toggle_value(widget,"/ritmo/graves/musicctl")
def on_agudos_in_on_toggled(widget):
	on_toggle_value(widget,"/ritmo/agudos/musicctl")

def on_ritmo_beats_value_changed(widget):
	on_value_changed(widget,"/ritmo/ritmo/beats")
def on_graves_beats_value_changed(widget):
	on_value_changed(widget,"/ritmo/graves/beats")
def on_agudos_beats_value_changed(widget):
	on_value_changed(widget,"/ritmo/agudos/beats")
def on_graves_hz_value_changed(widget):
	on_value_changed(widget,"/ritmo/graves/hz")
def on_agudos_hz_value_changed(widget):
	on_value_changed(widget,"/ritmo/agudos/hz")

def on_ritmo_auto_on_toggled(widget):
	on_toggle_value(widget,"/ritmo/ritmo/auto")
		
def on_ritmo_auto_speed_value_changed(widget):
	on_value_changed(widget,"/ritmo/ritmo/speed")
	
def on_ritmo_auto_beat_clicked(*args):
	envia("/ritmo/ritmo/beat 1\n")
	
def on_graves_auto_on_toggled(widget):
	on_toggle_value(widget,"/ritmo/graves/auto")
		
def on_graves_auto_speed_value_changed(widget):
	on_value_changed(widget,"/ritmo/graves/speed")
	
def on_graves_auto_beat_clicked(*args):
	envia("/ritmo/graves/beat 1\n")
	
def on_agudos_auto_on_toggled(widget):
	on_toggle_value(widget,"/ritmo/agudos/auto")
		
def on_agudos_auto_speed_value_changed(widget):
	on_value_changed(widget,"/ritmo/agudos/speed")
	
def on_agudos_auto_beat_clicked(*args):
	envia("/ritmo/agudos/beat 1\n")

#FUENTES:
def on_color_texto_color_set3d(*args):
	colorpick = xml.get_widget("color_texto3d")
	color = colorpick.get_color()
	alpha = colorpick.get_alpha()
	r = color.red/65535.0
	g = color.green/65535.0
	b = color.blue/65535.0
	if (xml.get_widget("texto_lanzar_3d1").get_active()):
		address = "/3dp/text1/compose/r"
		envia(address + " %s\n" % (r))
		address = "/3dp/text1/compose/g"
		envia(address + " %s\n" % (g))
		address = "/3dp/text1/compose/b"
		envia(address + " %s\n" % (b))
	if (xml.get_widget("texto_lanzar_3d1").get_active()):
		address = "/3dp/text2/compose/r"
		envia(address + " %s\n" % (r))
		address = "/3dp/text2/compose/g"
		envia(address + " %s\n" % (g))
		address = "/3dp/text2/compose/b"
		envia(address + " %s\n" % (b))



def on_color_texto_color_set(*args):
	colorpick = xml.get_widget("color_texto")
	color = colorpick.get_color()
        red = color.red/256
	green = color.green/256
	blue = color.blue/256
	alpha = colorpick.get_alpha()
	if (xml.get_widget("texto_lanzar_video").get_active()):
		envia("/text/r " + str(red) + "\n")
		envia("/text/g " + str(green) + "\n")
		envia("/text/b " + str(blue) + "\n" )
		envia("/text/a %s\n" % (alpha))

def get_font_desc(fontsel):
	import pango
	fn = fontsel.get_font_name()
	fn = fn[:fn.rfind(" ")]
	fn = fn + " 12"
	f = pango.FontDescription(fn)
	return f

def find_font_name(fontsel):
	fontsel.set_use_font(1)
	sel = fontsel.get_font_name()
	print sel
	sel = string.replace(sel,"Italic",'')
		
	from ttfquery._scriptregistry import registry
	sel2 = sel[:sel.rfind(" ")]
	size = sel[sel.rfind(" ")+1:]
	try:
		fontNames = registry.matchName(sel2)
	except:
		sel2 = string.replace(sel2,"Semi-Condensed",'')
		sel2 = string.replace(sel2,"Semi-Bold",'')
		sel2 = string.replace(sel2,"Condensed",'')
		sel2 = string.replace(sel2,"Sans L",'')
		sel2 = string.replace(sel2,"Bold",'')
		sel2 = string.replace(sel2,"L,",'')
		if sel2.endswith(" L"):
			sel2 = sel2[:-2]
		sel2 = string.strip(sel2," ")
		fontNames = registry.matchName(sel2)
	specifics = registry.fontMembers(fontNames[0])
	specifics.sort()
	metadata = registry.metadata( registry.fontFile(specifics[0]) )
	fontfile = metadata[0]
	return fontfile

def on_3dp_object_font_font_set(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/font font "
	fontsel = xml.get_widget("3dp_object_font_"+do_3dp_get_current_object(widget))
	fontfile = find_font_name(fontsel)
	f = get_font_desc(fontsel)
	envia(address+fontfile+"\n")
	if do_3dp_get_current_object(widget) == "text1":
		xml.get_widget("texto3d1_texto").modify_font(f)
	else:
		xml.get_widget("texto3d2_texto").modify_font(f)

def on_fuente_texto_font_set3d(*args):
	fontsel = xml.get_widget("fuente_texto3d")
	fontfile = find_font_name(fontsel)
	f = get_font_desc(fontsel)
	if (xml.get_widget("texto_lanzar_3d1").get_active()):
		envia("/3dp/text1/font font "+fontfile+"\n")
		xml.get_widget("texto_texto3d").modify_font(f)
		xml.get_widget("texto3d1_texto").modify_font(f)
	if (xml.get_widget("texto_lanzar_3d2").get_active()):
		envia("/3dp/text1/font font "+fontfile+"\n")
		xml.get_widget("texto_texto3d").modify_font(f)
		xml.get_widget("texto3d2_texto").modify_font(f)

		
def on_fuente_texto_font_set(*args):
	fontsel = xml.get_widget("fuente_texto")
	fontsel.set_use_font(1)
	sel = fontsel.get_font_name()
	size = sel[sel.rfind(" ")+1:]
	fontfile = find_font_name(fontsel)
	dir = os.path.dirname(fontfile)
	fontfile = fontfile[fontfile.rfind("/")+1:fontfile.rfind(".")]
	fontfile = dir +"/"+fontfile + "/" + size
	envia("/text/font font "+fontfile+"\n")
	f = get_font_desc(fontsel)
	text_input = xml.get_widget("texto_texto").modify_font(f)
						    

def on_borrar_texto_clicked(*args):
	envia("/text/text clear\n")
def on_add_texto_clicked(*args):
	entrada = xml.get_widget("texto_texto")
	texto = entrada.get_text()
	model = xml.get_widget("treeview_textos").get_model()
	model.append([texto])
	
def on_add_texto3d_clicked(*args):
	entrada = xml.get_widget("texto_texto3d")
	texto = entrada.get_text()
	model = xml.get_widget("treeview_textos3d").get_model()
	model.append([texto])
def on_enviar_texto_clicked(*args):
	entrada = xml.get_widget("texto_texto")
	texto = entrada.get_text()
	entradax = xml.get_widget("texto_x")
	x = entradax.get_text()
	entraday = xml.get_widget("texto_y")
	y = entraday.get_text()
	textor = string.replace(texto,"1",'"1"')
	textor = string.replace(textor,"2",'"2"')
	textor = string.replace(textor,"3",'"3"')
	textor = string.replace(textor,"4",'"4"')
	textor = string.replace(textor,"5",'"5"')
	textor = string.replace(textor,"6",'"6"')
	textor = string.replace(textor,"7",'"7"')
	textor = string.replace(textor,"8",'"8"')
	textor = string.replace(textor,"9",'"9"')
	textor = string.replace(textor,"0",'"0"')
	textor = textor.replace(",",".")
	textor = textor.replace(";",":")
	textor = string.replace(textor," ","%32")
	#envia('/text/text clear\n');
	textof = '/text/text text "' + textor + '" %s' % string.atoi(x)
	envia(textof+' %s\n' % string.atoi(y))
	entrada.set_property("text","")

def on_enviar_texto_clicked3d(*args):
	entrada = xml.get_widget("texto_texto3d")
	texto = entrada.get_text()
	if (xml.get_widget("texto_lanzar_3d1").get_active()):
	    	texto = codecs.charmap_encode(texto)
		envia("/3dp/text1/text text %s\n" % (texto[0]))
	if (xml.get_widget("texto_lanzar_3d2").get_active()):
	    	texto = codecs.charmap_encode(texto)
		envia("/3dp/text2/text text %s\n" % (texto[0]))
	entrada.set_property("text","")

def on_borrar_texto_clicked3d(*args):
	if (xml.get_widget("texto_lanzar_3d1").get_active()):
		envia("/3dp/text1/on %s\n" % (0))
	if (xml.get_widget("texto_lanzar_3d2").get_active()):
		envia("/3dp/text2/on %s\n" % (0))


def on_enviar_texto3d1_clicked(*args):
	entrada = xml.get_widget("texto3d1_texto")
	texto = entrada.get_text()
	texto = codecs.charmap_decode(texto)
	envia("/3dp/text1/text text %s\n" % (texto[0]))
	entrada.set_property("text","")
	on_w = xml.get_widget("3dp_object_on_text1")
	if not on_w.get_active():
		on_w.set_active(True)
def on_enviar_texto3d2_clicked(*args):
	entrada = xml.get_widget("texto3d2_texto")
	texto = entrada.get_text()
	texto = codecs.charmap_encode(texto)
	envia("/3dp/text2/text text %s\n" % (texto[0]))
	entrada.set_property("text","")
	on_w = xml.get_widget("3dp_object_on_text2")
	if not on_w.get_active():
		on_w.set_active(True)

def on_3d_general_reset_clicked(*args):
	global memory
	envia("/3dp/*/alpha 0.7\n")
	envia("/3dp/*/compose/add 1\n")
	envia("/3dp/*/compose/dtest 0\n")
	envia("/3dp/*/compose/b 1.0\n")
	envia("/3dp/*/compose/g 1.0\n")
	envia("/3dp/*/compose/r 1.0\n")
	envia("/3dp/*/compose/scale 1.0\n")
	envia("/3dp/*/compose/x 0\n")
	envia("/3dp/*/compose/y 0\n")
	envia("/3dp/*/compose/z 0\n")
	envia("/3dp/*/object/* 0\n")
	envia("/3dp/*/rotate/* 0\n")
	envia("/3dp/*/superfor/objetos 0\n")
	envia("/3dp/*/superfor/separacion 1\n")
	envia("/3dp/*/superfor/nerve 0\n")
	envia("/3dp/*/superfor/numero 5\n")
	envia("/3dp/*/on 0\n")
	envia("/3dp/pantalla1/on 1\n")
	envia("/3dp/general/center 1\n")
	envia("/3dp/general/on 1\n")
	envia("/3dp/general/scale 0.75\n")
	envia("/3dp/*/object/screen 1\n")
	envia("/*/auto 0\n")
	envia("/effects/* 0\n")
	envia("/image/load clear\n")
	envia("/ritmo/*/auto 0\n")
	envia("/text/text text %32 160 120\n")
	memory = {}


def on_texto_izquierda_clicked(*args):
	envia("/text/text/center\n")
def on_texto_centrar_clicked(*args):
	envia("/text/text/left\n")

def on_button_auto_textos_cargar_rss_clicked(*args):
	win2 = xml.get_widget("window_rssfeeds")
	win2.show()
def on_button_auto_textos_cargar_rss_clicked3d(*args):
	win2 = xml.get_widget("window_rssfeeds3d")
	win2.show()
def on_rssfeeds_close(*args):
	xml.get_widget("window_rssfeeds").hide()
	return 1
def on_rssfeeds_close3d(*args):
	xml.get_widget("window_rssfeeds3d").hide()
	return 1
def on_button_auto_textos_cargar_comando_clicked(*args):
	win2 = xml.get_widget("window_command")
	win2.show()
def on_window_command_close(*args):
	xml.get_widget("window_command").hide()
	return 1
def on_button_auto_textos_cargar_comando_clicked3d(*args):
	win2 = xml.get_widget("window_command3d")
	win2.show()
def on_window_command_close3d(*args):
	xml.get_widget("window_command3d").hide()
	return 1


def read_text_command(r,p,treeview_name):
    	l = "start"
	while(l.find("\EOF") == -1):
		l = r.readline()
		l = l.strip("\n")
		if l:
			gtk.threads_enter()
			treerss = xml.get_widget(treeview_name)
			model = treerss.get_model()
			tex = codecs.charmap_decode(l)
			model.append([tex[0]])
			gtk.threads_leave()
	r.close()
	p.tochild.close()

def on_window_command_aceptar_clicked(*args):
	comando = xml.get_widget("window_command_text").get_child()
	texto = comando.get_text()
	p = popen2.Popen3("bash")
	r = p.fromchild
	w = p.tochild
	w.write(texto+"\n")
	w.flush()
	thread.start_new_thread(read_text_command,(r,p,"treeview_textos"))
def on_window_command_aceptar_clicked3d(*args):
	comando = xml.get_widget("window_command_text3d").get_child()
	texto = comando.get_text()
	p = popen2.Popen3("bash")
	r = p.fromchild
	w = p.tochild
	w.write(texto+"\n")
	w.flush()
	thread.start_new_thread(read_text_command,(r,p,"treeview_textos3d"))


def on_rssfeeds_cargar_clicked(*args):
	treerss = xml.get_widget("treeview_rssfeeds")
	selection = treerss.get_selection()
	(model, iter) = selection.get_selected()
	if (iter):
		texto = model.get_value(iter, 1)
		rssfeed = openRSS(texto)
		tree = xml.get_widget("treeview_textos")
       		model = tree.get_model()
		for line in rssfeed:
			model.append([line.strip("\n")])
	xml.get_widget("window_rssfeeds").hide()
def on_rssfeeds_cargar_clicked3d(*args):
	treerss = xml.get_widget("treeview_rssfeeds3d")
	selection = treerss.get_selection()
	(model, iter) = selection.get_selected()
	if (iter):
		texto = model.get_value(iter, 1)
		rssfeed = openRSS(texto)
		tree = xml.get_widget("treeview_textos3d")
       		model = tree.get_model()
		for line in rssfeed:
			model.append([line.strip("\n")])
	xml.get_widget("window_rssfeeds3d").hide()


def on_button_auto_textos_cargar_clicked(widget):
	win2 = xml.get_widget("filechooserdialog_textos")
	win2.show()
def on_button_auto_textos_cargar_clicked3d(widget):
	win2 = xml.get_widget("filechooserdialog_textos3d")
	win2.show()

def on_button_auto_textos_lanzar_clicked(widget):
        global lanzando_texto
	lanzando_texto = 1
def on_button_auto_textos_parar_clicked(widget):
        global lanzando_texto
	lanzando_texto = 0
def on_button_auto_textos_lanzar_clicked3d(widget):
        global lanzando_texto3d
	lanzando_texto3d = 1
def on_button_auto_textos_parar_clicked3d(widget):
        global lanzando_texto3d
	lanzando_texto3d = 0

def on_button_auto_textos_limpiar_clicked(widget):
	tree = xml.get_widget("treeview_textos")
	model = tree.get_model()
	model.clear()
def on_button_auto_textos_limpiar_clicked3d(widget):
	tree = xml.get_widget("treeview_textos3d")
	model = tree.get_model()
	model.clear()

def on_filechooserdialog_textos_delete_event(*args):
	win2 = xml.get_widget("filechooserdialog_textos")
	win2.hide()
	return 1

def on_filechooserdialog_textos_aceptar_clicked(*args):
	win2 = xml.get_widget("filechooserdialog_textos")
        win2.hide()
        fileopen = win2.get_filename()
	tree = xml.get_widget("treeview_textos")
        model = tree.get_model()
	for line in fileinput.input(fileopen):
		if (line.strip("\n") == ""):
			pass
		else:
			model.append([line.strip("\n")])
def on_filechooserdialog_textos_delete_event3d(*args):
	win2 = xml.get_widget("filechooserdialog_textos3d")
	win2.hide()
	return 1

def on_filechooserdialog_textos_aceptar_clicked3d(*args):
	win2 = xml.get_widget("filechooserdialog_textos3d")
        win2.hide()
        fileopen = win2.get_filename()
	tree = xml.get_widget("treeview_textos3d")
        model = tree.get_model()
	for line in fileinput.input(fileopen):
		if (line.strip("\n") == ""):
			pass
		else:
			model.append([line.strip("\n")])
	
def on_texto_estatico_clicked(*args):
	envia("/text/layermode layermode static\n")
def on_texto_deslizante_clicked(*args):
	envia("/text/layermode layermode scroll\n")
def on_texto_feed_clicked(*args):
	envia("/text/layermode layermode feed\n")
def on_texto_direccion_clicked(*args):
	envia("/text/direction bang\n")
def on_texto_letra_a_letra_clicked(*args):
	envia("/text/layermode layermode slow\n")

# IMAGENES
def on_png_estirar_clicked(*args):
	envia("/image/estirar bang\n")

def on_png_launch3d_clicked(*args):
	videosel = xml.get_widget("selector_png3d")
	file = videosel.get_filename()
	folder = videosel.get_current_folder()
	videosel.set_preview_widget_active(1)
	launch_image3d(file,folder)

def on_selector_videos_file_activated3d(*args):
	 on_png_launch_clicked3d(*args)

def on_png_launch_clicked(*args):
	videosel = xml.get_widget("selector_png")
	file = videosel.get_filename()
	folder = videosel.get_current_folder()
	videosel.set_preview_widget_active(1)
	entrada = xml.get_widget("png_x")
	texto1 = entrada.get_text()
	num1 = string.atoi(texto1)
	entrada = xml.get_widget("png_y")
	texto2 = entrada.get_text()
	num2 = string.atoi(texto2)
	envia("/image/load load "+file+" %s %s\n" % (num1, num2))
	envia("/image/dir location "+folder+"\n")
	prev_img = xml.get_widget("preview_imagen")
	prev_img.set_from_pixbuf(preview2.get_pixbuf())
	
def on_selector_videos_file_activated(*args):
	 on_lanzar_video_canal1_clicked(*args)

def on_png_clean_clicked(*args):
	envia("/image/load clear\n")
def on_hscale_png_value_changed(widget):
	on_value_changed(widget,"/image/blend")

def on_png_google_clicked(*args):
	win2 = xml.get_widget("dialog_google").show()
def on_google_close(*args):
	xml.get_widget("dialog_google").hide()
def on_button_google_cancelar_clicked(*args):
	xml.get_widget("dialog_google").hide()
def on_button_google_aceptar_clicked(*args):
	global search
	dialog = xml.get_widget("dialog_google")
	text = xml.get_widget("entry_google").get_text()
	search=text
	pngsel = xml.get_widget("selector_png")
	f =  user.home+"/.delVj/autoimages/"
	if (not os.path.exists(f)):
	    os.mkdir(f)
	stext = string.replace(text," ","+")
	f = f + stext
	if (not os.path.exists(f)):
	    os.mkdir(f)
	pngsel.set_current_folder_uri("file://"+f)
	dialog.hide()
def on_png_google_clicked3d(*args):
	win2 = xml.get_widget("dialog_google3d").show()
def on_google_close3d(*args):
	xml.get_widget("dialog_google3d").hide()
def on_button_google_cancelar_clicked3d(*args):
	xml.get_widget("dialog_google3d").hide()
def on_button_google_aceptar_clicked3d(*args):
	global search3d
	dialog = xml.get_widget("dialog_google3d")
	text = xml.get_widget("entry_google3d").get_text()
	search3d=text
	pngsel = xml.get_widget("selector_png3d")
	f =  user.home+"/.delVj/autoimages/"
	if (not os.path.exists(f)):
	    os.mkdir(f)
	stext = string.replace(text," ","+")
	f = f + stext
	if (not os.path.exists(f)):
	    os.mkdir(f)
	pngsel.set_current_folder_uri("file://"+f)
	dialog.hide()

def on_imagen_modo_copiar_clicked(*args):
	envia("/image/copy 1\n")
def on_imagen_modo_add_clicked(*args):
	envia("/image/add 1\n")
def on_imagen_modo_restar_clicked(*args):
	envia("/image/substract 1\n")
def on_imagen_modo_reshade_clicked(*args):
	envia("/image/reshade 1\n")

# CONFIGURACION:
def on_iniciar_grabacion_clicked(*args):
	entrada = xml.get_widget("grabar_fichero")
	texto = entrada.get_text()
	#envia("/record open "+texto+"\n92 start\n")
	envia("/record/start 1\n")
def on_parar_grabacion_clicked(*args):
	envia("/record/stop 1\n")
def on_emitir_streaming_clicked(*args):
	server = xml.get_widget("stream_server").get_text()
	port = xml.get_widget("stream_port").get_text()
	mountpoint = xml.get_widget("stream_mount").get_text()
	password = xml.get_widget("stream_password").get_text()
	#texto = entrada.get_text()
	envia("/stream/play 0\n")
	envia("/stream/theonice passwd %s\n" % (password))
	envia("/stream/theonice connect "+server+" "+mountpoint+" %s\n" % (port))
	envia("/stream/play 1\n")
def on_parar_streaming_clicked(*args):
	envia("/stream/play 0\n")
def on_salida_2videos_toggled(widget):
	on_toggle_value(widget,"/config/twovideos")

def on_salida_2don_toggled(widget):
	on_toggle_value(widget,"/config/on2d")
def on_salida_3don_toggled(widget):
	on_toggle_value(widget,"/3dp/general/on")
def on_salida_3d_monitor_on_toggled(widget):
	on_toggle_value(widget,"/3dp/general/monitor")

def on_salida_doble_clicked(*args):
	envia("/config/twin bang\n")
def on_salida_fullscreen_clicked(*args):
	envia("/config/fullscreen bang\n")
def on_salida_640_clicked(*args):
	envia("/config/640 bang\n")
def on_salida_320_clicked(*args):
	envia("/config/320 bang\n")
# WEBCAM NEW CHANNELS:
# on_toggled
def on_webcam2_on_toggled(widget):
	on_toggle_value(widget,"/3dp/textureunit/cam1/on")
def on_webcam3_on_toggled(widget):
	on_toggle_value(widget,"/3dp/textureunit/cam2/on")
def on_webcam4_on_toggled(widget):
	on_toggle_value(widget,"/3dp/textureunit/cam3/on")
def on_webcam5_on_toggled(widget):
	on_toggle_value(widget,"/3dp/textureunit/cam4/on")
# device_value_changed
def on_webcam2_device_value_changed(widget):
	on_value_changed(widget,"/3dp/textureunit/cam1/device")
def on_webcam3_device_value_changed(widget):
	on_value_changed(widget,"/3dp/textureunit/cam2/device")
def on_webcam4_device_value_changed(widget):
	on_value_changed(widget,"/3dp/textureunit/cam3/device")
def on_webcam5_device_value_changed(widget):
	on_value_changed(widget,"/3dp/textureunit/cam4/device")
# channel_value_changed
def on_webcam2_channel_value_changed(widget):
	on_value_changed(widget,"/3dp/textureunit/cam1/channel")
def on_webcam3_channel_value_changed(widget):
	on_value_changed(widget,"/3dp/textureunit/cam2/channel")
def on_webcam4_channel_value_changed(widget):
	on_value_changed(widget,"/3dp/textureunit/cam3/channel")
def on_webcam5_channel_value_changed(widget):
	on_value_changed(widget,"/3dp/textureunit/cam4/channel")
# fps_value_changed
def on_webcam2_fps_value_changed(widget):
	on_value_changed(widget,"/3dp/textureunit/cam1/fps")
def on_webcam3_fps_value_changed(widget):
	on_value_changed(widget,"/3dp/textureunit/cam2/fps")
def on_webcam4_fps_value_changed(widget):
	on_value_changed(widget,"/3dp/textureunit/cam3/fps")
def on_webcam5_fps_value_changed(widget):
	on_value_changed(widget,"/3dp/textureunit/cam4/fps")

# OLD WEBCAM
def on_webcam1_fps_value_changed(widget):
	on_value_changed(widget,"/webcam/fps")
def on_webcam1_device_value_changed(widget):
	on_value_changed(widget,"/webcam/device")
def on_webcam1_channel_value_changed(widget):
	on_value_changed(widget,"/webcam/channel")
def on_webcam1_on_toggled(widget):
	on_toggle_value(widget,"/webcam/on")
def on_webcam_unrouted_toggled(widget):
	if (widget.get_active()):
		envia("/webcam/mode 0\n")
def on_webcam_channel1_toggled(widget):
	if (widget.get_active()):
		envia("/webcam/mode 1\n")
def on_webcam_channel2_toggled(widget):
	if (widget.get_active()):
		envia("/webcam/mode 2\n")
def on_webcam1_zoom_value_changed(widget):
	on_value_changed(widget,"/webcam/zoom")

# XMMS CONTROL

def on_xmms_lanzar_clicked(*args):
    if(xmms.is_running()):
	tree = xml.get_widget("xmms_list")
	selection = tree.get_selection()
	(model, [iter]) = selection.get_selected_rows()
	for index in iter:
		xmms.set_playlist_pos(index)
	
def on_xmms_prev_clicked(*args):
    if(xmms.is_running()):
	xmms.playlist_prev()
def on_xmms_play_clicked(*args):
    if(xmms.is_running()):
	xmms.play()
def on_xmms_pause_clicked(*args):
    if(xmms.is_running()):
	xmms.pause()
def on_xmms_stop_clicked(*args):
    if(xmms.is_running()):
	xmms.stop()
def on_xmms_eject_clicked(*args):
    if(xmms.is_running()):
	xmms.eject()
def on_xmms_next_clicked(*args):
    if(xmms.is_running()):
	xmms.playlist_next()
	cancionw = xml.get_widget("cancion_actual")
	xmmspos = xmms.get_playlist_pos()
	cancionw.set_text(xmms.get_playlist_title(xmmspos))

def on_xmms_random_toggled(widget):
    if(xmms.is_running()):
	if (widget.get_active()):
		xmms.toggle_shuffle(0)
	else:
		xmms.toggle_shuffle(0)
def on_xmms_repeat_toggled(widget):
    if(xmms.is_running()):
	if (widget.get_active()):
		xmms.toggle_repeat(0)
	else:
		xmms.toggle_repeat(0)
def on_xmms_volume_value_changed(widget):
    if(xmms.is_running()):
	value = widget.get_value()
	xmms.set_volume(value,value)

def on_conectar_xmms_a_pd1_activate(*args):
    if(xmms.is_running()):
	popen2.popen2("jack_connect xmms_0:out_1 pure_data_0:input0 &")
	popen2.popen2("sleep 1s &&jack_connect xmms_0:out_2 pure_data_0:input1 &")

# MACROS
# treeview_macros

# DIALOGO
def on_dialog_close(*args):
	dialog = xml.get_widget("dialog_nueva_macro")
	dialog.hide()
	dialog = xml.get_widget("dialog_grabar_macro")
	dialog.hide()
	return 1

def on_nueva_macro_aceptar_clicked(*args):
	dialog = xml.get_widget("dialog_nueva_macro")
	text = xml.get_widget("nueva_macro_texto").get_text()
	tree = xml.get_widget("treeview_todas_macros")
	model = tree.get_model()
	if (text !=  ""):
		model.append([text])
		f =  file(user.home+"/.delVj/"+text,"w")
		f.close()
	dialog.hide()

def on_button_macros_lanzar_clicked(widget):
	# nose usa
	pass
xml.get_widget("button_macros_parar").set_sensitive(0)
def on_button_macros_grabar_clicked(widget):
	xml.get_widget("treeview_todas_macros").set_sensitive(0)
	xml.get_widget("button_todas_macros_nueva").set_sensitive(0)
	xml.get_widget("button_todas_macros_borrar").set_sensitive(0)
	xml.get_widget("button_todas_macros_lanzar").set_sensitive(0)
	xml.get_widget("button_macros_limpiar").set_sensitive(0)
	xml.get_widget("button_macros_grabar").set_sensitive(0)
	xml.get_widget("button_macros_1o_a_0").set_sensitive(0)
	xml.get_widget("button_macros_a_0").set_sensitive(0)
	#xml.get_widget("button_macros_guardar").set_sensitive(0)
	#xml.get_widget("button_macros_cargar").set_sensitive(0)
	xml.get_widget("button_macros_parar").set_sensitive(1)
	global timebase
	global grabando
	timebase = time.time() # el tiempo empieza a contar
	grabando = 1
def on_button_macros_limpiar_clicked(widget):
	global timebase
	macros.clear()
	timebase = time.time() # el tiempo empieza a contar

def grabar_macro():
	tree = xml.get_widget("treeview_todas_macros")
	selection = tree.get_selection()
	(model, iter) = selection.get_selected()
	texto = model.get_value(iter, 0)
	ficheromacro = file(user.home+"/.delVj/"+texto,"w")
	tree = xml.get_widget("treeview_macros")
	model = tree.get_model()
	i = 0
	while(i<len(model)):
	    iter = model.get_iter(i)
	    tim = model.get_value(iter,0)
	    tex = model.get_value(iter,1)
	    ficheromacro.write(tim + " " + tex + "\n")
	    i = i + 1
	ficheromacro.close()
		
def on_button_macros_parar_clicked(widget):
	global grabando
	xml.get_widget("treeview_todas_macros").set_sensitive(1)
	xml.get_widget("button_todas_macros_nueva").set_sensitive(1)
	xml.get_widget("button_todas_macros_borrar").set_sensitive(1)
	xml.get_widget("button_todas_macros_lanzar").set_sensitive(1)
	xml.get_widget("button_macros_limpiar").set_sensitive(1)
	xml.get_widget("button_macros_grabar").set_sensitive(1)
	xml.get_widget("button_macros_1o_a_0").set_sensitive(1)
	xml.get_widget("button_macros_a_0").set_sensitive(1)
	#xml.get_widget("button_macros_guardar").set_sensitive(1)
	#xml.get_widget("button_macros_cargar").set_sensitive(1)
	xml.get_widget("button_macros_parar").set_sensitive(0)
	grabar_macro()
	grabando = 0
def on_button_macros_a_0_clicked(widget):
	tree = xml.get_widget("treeview_macros")
	model = tree.get_model()
	i = 0
	base = 0
	while (i<len(model)):
	    iter = model.get_iter(i)
	    model.set_value(iter,0,"0.00")
	    i = i+1
def on_button_macros_1o_a_0_clicked(widget):
	tree = xml.get_widget("treeview_macros")
	model = tree.get_model()
	i = 0
	base = 0
	while (i<len(model)):
	    iter = model.get_iter(i)
	    val = string.atof(model.get_value(iter,0))
	    if (i == 0):
	        base = val
	    val = val - base
	    model.set_value(iter,0,"%1.2f"%(val))
	    i = i+1
def on_button_macros_adelantar_clicked(widget):
	pass
def on_button_macros_borrar_comando_clicked(widget):
	pass
def on_button_macros_grabar_cambios_clicked(widget):
        grabar_macro()

def on_treeview_todas_macros_row_activated(*args):
	print("doble click")

def on_treeview_todas_macros_select_cursor_row(*args):
	tree = xml.get_widget("treeview_todas_macros")
	selection = tree.get_selection()
	(model, iter) = selection.get_selected()
	texto = model.get_value(iter, 0)
	tree = xml.get_widget("treeview_macros")
	model = tree.get_model()
	model.clear()
        for line in fileinput.input(user.home+"/.delVj/"+texto):
	    tex = line[line.find(" ")+1:]
	    tim = line[:line.find(" ")]
	    model.append([tim,tex.strip("\n")])

# 3DP
global estado_3dp
estado_3dp = {"pantalla1" : 1}


def helper_set_visible(boolval,object):
	if (boolval):
		xml.get_widget(object).show()
	else:
		xml.get_widget(object).hide()
	

def do_3dp_get_current_object(widget):
	if (not widget.get_name().find("general") == -1):
		return("general")
	if (not widget.get_name().find("screen1") == -1):
		return("pantalla1")
	if (not widget.get_name().find("screen2") == -1):
		return("pantalla2")
	if (not widget.get_name().find("ball1") == -1):
		return("bola1")
	if (not widget.get_name().find("ball2") == -1):
		return("bola2")
	if (not widget.get_name().find("electricball") == -1):
		return("turbina")
	if (not widget.get_name().find("crab") == -1):
		return("cangrejo")
	if (not widget.get_name().find("storm") == -1):
		return("storm")
	if (not widget.get_name().find("explosion") == -1):
		return("explosion")
	if (not widget.get_name().find("cubes") == -1):
		return("cubitos")
	if (not widget.get_name().find("cal3d1") == -1):
		return("cal3d1")
	if (not widget.get_name().find("cal3d2") == -1):
		return("cal3d2")
	if (not widget.get_name().find("text1") == -1):
		return("text1")
	if (not widget.get_name().find("text2") == -1):
		return("text2")
	if (not widget.get_name().find("light") == -1):
		return("light")

#objeto
def on_3dp_object_esfera_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/object/ball"
	on_toggle_value(widget,address)
def on_3dp_object_mesfera_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/object/ballmesh"
	on_toggle_value(widget,address)
def on_3dp_object_cubo_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/object/cube"
	on_toggle_value(widget,address)
def on_3dp_object_mcubo_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/object/cubemesh"
	on_toggle_value(widget,address)
def on_3dp_object_pantalla_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/object/screen"
	on_toggle_value(widget,address)
def on_3dp_object_mpantalla_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/object/screenmesh"
	on_toggle_value(widget,address)

# texturas
def on_3dp_object_tex1_licked(widget):
	value = 1
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/texture"
	envia(address + " %s\n" % (value))
def on_3dp_object_tex2_clicked(widget):
	value = 2
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/texture"
	envia(address + " %s\n" % (value))
def on_3dp_object_tex3_clicked(widget):
	value = 3
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/texture"
	envia(address + " %s\n" % (value))
def on_3dp_object_text4_clicked(widget):
	value = 4
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/texture"
	envia(address + " %s\n" % (value))
def on_3dp_object_tex5_clicked(widget):
	value = 5
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/texture"
	envia(address + " %s\n" % (value))
def on_3dp_object_tex6_clicked(widget):
	value = 6
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/texture"
	envia(address + " %s\n" % (value))
def on_3dp_object_tex7_clicked(widget):
	value = 7
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/texture"
	envia(address + " %s\n" % (value))
def on_3dp_object_tex8_clicked(widget):
	value = 8
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/texture"
	envia(address + " %s\n" % (value))


# cangrejo
def on_3dp_object_speed_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/speed"
	value = widget.get_value()
	envia(address + " %s\n" % (value))

def on_3dp_object_arti_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/articulate"
	value = widget.get_value()
	envia(address + " %s\n" % (value))

def on_3dp_object_artispeed_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/articulateanimspeed"
	value = widget.get_value()
	envia(address + " %s\n" % (value))

def on_3dp_object_long_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/toruslen"
	value = widget.get_value()
	envia(address + " %s\n" % (value))

def on_3dp_object_tamcub_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/cubesize"
	value = widget.get_value()
	envia(address + " %s\n" % (value))

def on_3dp_object_tamall_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/torussize"
	value = widget.get_value()
	envia(address + " %s\n" % (value))

def on_3dp_object_grosorall_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/toruswidth"
	value = widget.get_value()
	envia(address + " %s\n" % (value))

def on_config_close(widget, menu):
    win = xml.get_widget("window_config")
    win.hide()
    widget = xml.get_widget("menuitem_config")
    widget.set_active(False)
    return 1

def on_show_window_config(widget):
    win = xml.get_widget("window_config")
    address = "/3dp/turbina/control/x"
    if widget.get_active():
        win.show()
    else:
        win.hide()

def on_general_xflanger(widget):
    address = "/3dp/general/compose/zsin"
    on_toggle_value(widget,address)
def on_general_xflanger_amp(widget):
    address = "/3dp/general/compose/zsinamp"
    value = widget.get_value()
    envia(address + " %s\n" % (value))
def on_general_xflanger_speed(widget):
    address = "/3dp/general/compose/zsinspeed"
    value = 10/(widget.get_value()+0.01)
    envia(address + " %s\n" % (value))
def on_general_xflanger_bymusic(widget):
    address = "/3dp/general/compose/zsinmusic"
    on_toggle_value(widget,address)

#turbina
def on_turbina_bang(widget):
    address = "/3dp/turbina/control/bang\n"
    envia(address)
def on_turbina_usex(widget):
    address = "/3dp/turbina/control/x"
    on_toggle_value(widget,address)
def on_turbina_usey(widget):
    address = "/3dp/turbina/control/y"
    on_toggle_value(widget,address)
def on_turbina_usez(widget):
    address = "/3dp/turbina/control/z"
    on_toggle_value(widget,address)
def on_turbina_greencontrol(widget):
    address = "/3dp/turbina/control/greencontrol"
    on_toggle_value(widget,address)
def on_turbina_bluecontrol(widget):
    address = "/3dp/turbina/control/bluecontrol"
    on_toggle_value(widget,address)
def on_turbina_red(widget):
    address = "/3dp/turbina/control/redcontrol"
    on_toggle_value(widget,address)


# CUBITOS
# :value_changed
def on_3dp_object_cubesfor_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/cubes/for"
	value = widget.get_value()
	envia(address + " %s\n" % (value))
def on_3dp_object_cubesdist_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/cubes/distance"
	value = widget.get_value()
	envia(address + " %s\n" % (value))
def on_3dp_object_cubescubesize_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/cubes/cubesize"
	value = widget.get_value()
	envia(address + " %s\n" % (value))
def on_3dp_object_cubessquaresize_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/cubes/squaresize"
	value = widget.get_value()
	envia(address + " %s\n" % (value))
# :toggles
def on_3dp_object_articulateanim_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/articulateanim"
	on_toggle_value(widget,address)
def on_3dp_object_cubescubeson_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/cubes/cubeson"
	on_toggle_value(widget,address)
def on_3dp_object_cubessquareson_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/cubes/squareson"
	on_toggle_value(widget,address)
def on_3dp_object_cubesgrow_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/cubes/grow"
	on_toggle_value(widget,address)
def on_3dp_object_cubesreset_clicked(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/cubes/reset"
	envia(address + " %s\n" % (1))


# rotaciones
def on_3dp_object_centrar_clicked(widget):
	if (do_3dp_get_current_object(widget) == "general"):
		envia("/3dp/general/center 1\n");
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/rotate/x 0\n")
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/rotate/y 0\n")
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/rotate/z 0\n")
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/compose/x 0\n")
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/compose/y 0\n")
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/compose/z 0\n")
	#envia("/3dp/"+do_3dp_get_current_object(widget)+"/compose/r 1\n")
	#envia("/3dp/"+do_3dp_get_current_object(widget)+"/compose/g 1\n")
	#envia("/3dp/"+do_3dp_get_current_object(widget)+"/compose/b 1\n")
	#envia("/3dp/"+do_3dp_get_current_object(widget)+"/compose/scale 1\n")
	name = widget.get_name()[widget.get_name().rfind("_")+1:]
	xml.get_widget("3dp_object_rotx_"+name).set_value(0)
	xml.get_widget("3dp_object_roty_"+name).set_value(0)
	xml.get_widget("3dp_object_rotz_"+name).set_value(0)
	xml.get_widget("3dp_object_x_"+name).set_value(0)
	xml.get_widget("3dp_object_y_"+name).set_value(0)
	xml.get_widget("3dp_object_z_"+name).set_value(0)
	#if (xml.get_widget("3dp_object_size_"+name)):
		#xml.get_widget("3dp_object_size_"+name).set_value(1)

def on_3dp_object_stop_clicked(widget):
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/rotate/autox 0\n")
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/rotate/autoy 0\n")
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/rotate/autoz 0\n")
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/rotate/nervex 0\n")
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/rotate/nervey 0\n")
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/rotate/nervez 0\n")
	name = widget.get_name()[widget.get_name().rfind("_")+1:]
	xml.get_widget("3dp_object_autorotx_"+name).set_active(0)
	xml.get_widget("3dp_object_autoroty_"+name).set_active(0)
	xml.get_widget("3dp_object_autorotz_"+name).set_active(0)
	xml.get_widget("3dp_object_nerverotx_"+name).set_active(0)
	xml.get_widget("3dp_object_nerveroty_"+name).set_active(0)
	xml.get_widget("3dp_object_nerverotz_"+name).set_active(0)

# rotacion 
def on_3dp_object_rotvel_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/rotate/speed"
	value = widget.get_value()
	envia(address + " %s\n" % ((value)))

def on_3dp_object_rotx_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/rotate/x"
	value = widget.get_value()
	envia(address + " %s\n" % (value))
def on_3dp_object_roty_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/rotate/y"
	value = widget.get_value()
	envia(address + " %s\n" % (value))
def on_3dp_object_rotz_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/rotate/z"
	value = widget.get_value()
	envia(address + " %s\n" % (value))

# auto rot
def on_3dp_object_depth_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/compose/dtest"
	on_toggle_value(widget,address)

def on_3dp_object_add_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/compose/add"
	name = widget.get_name()[widget.get_name().rfind("_")+1:]
	if (widget.get_active()):
		envia(address + " 1\n");
        	xml.get_widget("3dp_object_opacity_"+name).set_sensitive(1)
	else:
		envia(address + " 0\n");
        	xml.get_widget("3dp_object_opacity_"+name).set_sensitive(0)

def on_3dp_object_autorotx_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/rotate/autox"
	on_toggle_value(widget,address)
def on_3dp_object_autoroty_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/rotate/autoy"
	on_toggle_value(widget,address)
def on_3dp_object_autorotz_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/rotate/autoz"
	on_toggle_value(widget,address)

# cal3d
global curr_cal3d
curr_cal3d = "cal3d1"
def on_3dp_cal3d_file_clicked(widget):
	global curr_cal3d
	curr_cal3d = do_3dp_get_current_object(widget)
	win2 = xml.get_widget("filechooserdialog_cal3d")
	win2.show()
def on_filechooserdialog_cal3d_delete_event(*args):
	win2 = xml.get_widget("filechooserdialog_cal3d")
	win2.hide()
	return 1

def on_filechooserdialog_cal3d_aceptar_clicked(*args):
	win2 = xml.get_widget("filechooserdialog_cal3d")
        win2.hide()
        fileopen = win2.get_filename()
	address = "/3dp/"+curr_cal3d+"/model open"
	envia(address + " %s\n" % (fileopen))
	
def on_3dp_cal3d_speed_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/speed"
	value = widget.get_value()
	envia(address + " %s\n" % (value))
def on_3dp_cal3d_position_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/frame"
	value = widget.get_value()
	envia(address + " %s\n" % (value))
def on_3dp_cal3d_detail_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/resolution"
	value = widget.get_value()
	envia(address + " %s\n" % (value))
def on_3dp_cal3d_a1_clicked(widget):
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/setcycle 0\n")
def on_3dp_cal3d_a2_clicked(widget):
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/setcycle 1\n")
def on_3dp_cal3d_a3_clicked(widget):
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/setcycle 2\n")
def on_3dp_cal3d_a4_clicked(widget):
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/setcycle 3\n")
def on_3dp_cal3d_a5_clicked(widget):
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/setcycle 4\n")
def on_3dp_cal3d_a6_clicked(widget):
	envia("/3dp/"+do_3dp_get_current_object(widget)+"/setcycle 5\n")
# nerve rot
def on_3dp_object_nerverotx_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/rotate/nervex"
	on_toggle_value(widget,address)
def on_3dp_object_nerveroty_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/rotate/nervey"
	on_toggle_value(widget,address)
def on_3dp_object_nerverotz_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/rotate/nervez"
	on_toggle_value(widget,address)

# ejes principales
def on_3dp_object_x_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/compose/x"
	value = widget.get_value()
	envia(address + " %s\n" % (value))
def on_3dp_object_y_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/compose/y"
	value = widget.get_value()
	envia(address + " %s\n" % (value))
def on_3dp_object_z_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/compose/z"
	value = widget.get_value()
	envia(address + " %s\n" % (value))
def on_3dp_object_color_color_set(widget):
	color = widget.get_color()
	r = color.red/65535.0
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/compose/r"
	envia(address + " %s\n" % (r))
	g = color.green/65535.0
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/compose/g"
	envia(address + " %s\n" % (g))
	b = color.blue/65535.0
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/compose/b"
	envia(address + " %s\n" % (b))


def on_3dp_general_size_value_changed(widget):
	envia("/3dp/general/compose/scale %s\n" % (widget.get_value()))
def on_3dp_general_luminosidad_value_changed(widget):
	envia("/3dp/general/texgain %s\n" % (widget.get_value()))
def on_3dp_object_opacity_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/compose/a"
	on_value_changed(widget,address)
def on_3dp_object_superfor_number_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/superfor/numero"
	on_value_changed(widget,address)

def on_3dp_object_separacion_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/superfor/separacion"
	on_value_changed(widget,address)
def on_3dp_object_size_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/compose/scale"
	on_value_changed(widget,address)
def on_3dp_object_rotoblur_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/rot"
	on_value_changed(widget,address)
def on_3dp_object_distorsion_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/distorsion"
	on_value_changed(widget,address)
def on_3dp_object_for_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/for"
	on_value_changed(widget,address)


def on_3dp_general_centrar_clicked(*args):
	envia("/3dp/general/center 1\n");

def on_3dp_cal3d_clicked(widget):
    if (widget.get_active()):
	xml.get_widget("3dp_objeto_seleccionado_label").set_text("Objeto Seleccionado - Cal3d")
def on_3dp_texto1_clicked(widget):
    if (widget.get_active()):
	xml.get_widget("3dp_objeto_seleccionado_label").set_text("Objeto Seleccionado - Texto 1")
def on_3dp_texto2_clicked(widget):
    if (widget.get_active()):
	xml.get_widget("3dp_objeto_seleccionado_label").set_text("Objeto Seleccionado - Texto 2")
def on_3dp_cubitos_clicked(widget):
    if (widget.get_active()):
	xml.get_widget("3dp_objeto_seleccionado_label").set_text("Objeto Seleccionado - Cubitos")
def on_3dp_pantalla1_clicked(widget):
    if (widget.get_active()):
	xml.get_widget("3dp_objeto_seleccionado_label").set_text("Objeto Seleccionado - Pantalla 1")
def on_3dp_pantalla2_clicked(widget):
    if (widget.get_active()):
	xml.get_widget("3dp_objeto_seleccionado_label").set_text("Objeto Seleccionado - Pantalla 2")
def on_3dp_bola1_clicked(widget):
    if (widget.get_active()):
	xml.get_widget("3dp_objeto_seleccionado_label").set_text("Objeto Seleccionado - Bola 1")
def on_3dp_bola2_clicked(widget):
    if (widget.get_active()):
	xml.get_widget("3dp_objeto_seleccionado_label").set_text("Objeto Seleccionado - Bola 2")
def on_3dp_electricball_clicked(widget):
    if (widget.get_active()):
	xml.get_widget("3dp_objeto_seleccionado_label").set_text("Objeto Seleccionado - Bola Electrica")
def on_3dp_cangrejo_clicked(widget):
    if (widget.get_active()):
	xml.get_widget("3dp_objeto_seleccionado_label").set_text("Objeto Seleccionado - Cangrejo")
def on_3dp_tormenta_clicked(widget):
    if (widget.get_active()):
	xml.get_widget("3dp_objeto_seleccionado_label").set_text("Objeto Seleccionado - Tormenta")
def on_3dp_explosion_clicked(widget):
    if (widget.get_active()):
	xml.get_widget("3dp_objeto_seleccionado_label").set_text("Objeto Seleccionado - Explosion")

def on_3dp_object_on_toggled(widget):
        global estado_3dp
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/on"
	xml_w = xml.get_widget("3dp_" +widget.get_name()[widget.get_name().rfind("_")+1:]+"_label")
	if (widget.get_active()):
		envia(address + " 1\n");
	        estado_3dp[do_3dp_get_current_object(widget)] = 1;
		color = gtk.gdk.Color()
		color.red = 1
		color.blue = 0
		color.green = 0
		xml_w.modify_text(gtk.STATE_NORMAL,color)
		xml_w.drag_highlight()
	else:
		envia(address + " 0\n");
	        estado_3dp[do_3dp_get_current_object(widget)] = 0;
		color = gtk.gdk.Color()
		color.red = 0
		color.blue = 0
		color.green = 0
		xml_w.modify_text(gtk.STATE_NORMAL,color)
		xml_w.drag_unhighlight()
		
def on_3dp_object_x1_clicked(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/superfor/objetos"
	envia(address + " 0\n")
def on_3dp_object_x2_clicked(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/superfor/objetos"
	envia(address + " 1\n")
def on_3dp_object_x3_clicked(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/superfor/objetos"
	envia(address + " 2\n")
def on_3dp_object_x4_clicked(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/superfor/objetos"
	envia(address + " 3\n")
def on_3dp_object_superfor_nerve_value_changed(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/superfor/nerve "
	envia(address +str(widget.get_value()) +"\n")

def on_3dp_object_rotacion_automatica_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/autorot"
	on_toggle_value(widget,address)
def on_3dp_object_nervioso_toggled(widget):
	address = "/3dp/"+do_3dp_get_current_object(widget)+"/nervous"
	on_toggle_value(widget,address)

# treeview_todas_macros
def on_button_todas_macros_grabar_estado_clicked(widget):
	win2 = xml.get_widget("dialog_grabar_macro")
	win2.show()
def on_button_todas_macros_limpiar_estado_clicked(widget):
	global memory
	memory = {}

def on_grabar_macro_aceptar_clicked(widget):
	dialog = xml.get_widget("dialog_grabar_macro")
	text = xml.get_widget("grabar_macro_texto").get_text()
	tree = xml.get_widget("treeview_todas_macros")
	model = tree.get_model()
	dialog.hide()
	if (text !=  ""):
		model.append([text])
		ficheromacro = file(user.home+"/.delVj/"+text,"w")
		memory_keys = memory.keys()
		memory_keys.sort()
		for key in memory_keys:
	    		ficheromacro.write("0.0" + " "+key +" " + memory[key] + "\n")
		ficheromacro.close()

def on_button_todas_macros_nueva_clicked(widget):
	win2 = xml.get_widget("dialog_nueva_macro")
	win2.show()
def on_button_todas_macros_borrar_clicked(widget):
	tree = xml.get_widget("treeview_todas_macros")
	selection = tree.get_selection()
	(model, iter) = selection.get_selected()
	texto = model.get_value(iter, 0)
	os.remove(user.home+"/.delVj/"+texto)
	model.remove(iter)
def on_button_todas_macros_lanzar_clicked(widget):
	global lanzando
	global totallock
	totallock.acquire()
	lanzando = 1
	totallock.release()
	xml.get_widget("button_todas_macros_nueva").set_sensitive(0)
	xml.get_widget("button_todas_macros_borrar").set_sensitive(0)
	xml.get_widget("button_macros_grabar").set_sensitive(0)
	xml.get_widget("button_macros_a_0").set_sensitive(0)
	xml.get_widget("button_macros_1o_a_0").set_sensitive(0)
	xml.get_widget("button_macros_limpiar").set_sensitive(0)
	xml.get_widget("treeview_todas_macros").set_sensitive(0)
	xml.get_widget("treeview_macros").set_sensitive(0)
def on_button_todas_macros_lanzar_reset_clicked(widget):
	on_3d_general_reset_clicked(widget)
	on_button_todas_macros_lanzar_clicked(widget)
	
	
# BLUETOOTH
#import bluez
def on_bluetooth_conectar_clicked(widget):
	pass
def on_bluetooth_aceptar_clicked(widget):
	pass
def on_bluetooth_actualizar_clicked(widget):
	tree_bluez = xml.get_widget("treeview_bluetooth")
	bluez_model = tree_bluez.get_model()
	bluez_model.clear()
	try:
		sock = bluez.hci_open_dev(0)
	except:
		print "error accessing bluetooth device"
		return
	try:
		results = bluez.hci_inquiry(sock, duration=8, flush_cache=True)
		print "discovered: %s" % results
	except bluez.error:
		print "Error communicating with local bluetooth device."
		print "Wait a bit and try again, or try resetting the bluetooth device."
		return
	for addr in results:
		try:
			name = bluez.hci_read_remote_name( sock, addr, timeout=5192 )
		except bluez.error, e:
			name = str(e)
		print "%s - [%s]" % (addr, name)
		bluez_model.append([addr,name,'desconectado'])
	sock.close()

# Funciones de Respuesta al Interfaz
xml.signal_autoconnect(locals())

gtk.main()
