import pygtk
pygtk.require('2.0')

import gtk
import gtk.glade
import gobject


import popen2
import thread
import time

# Obtener el puntero al interfaz
gtk.threads_init()
xml = gtk.glade.XML("bash_proxy.glade")

global r
global w

# obtener los punteros a los descriptores de archivos
p = popen2.Popen3("bash")
r = p.fromchild
w = p.tochild

# thread de lectura
def automatizacion(r,x):
    l = "start"
    while(not l == ""):
        l = r.readline()
	l = l.strip("\n")
	print l;

thread.start_new_thread(automatizacion,(r,"x"))
#for linea in results:
#    print linea
# Funciones de Respuesta al Interfaz
# thread de salida
def on_button_clicked(*args):
    comando = xml.get_widget("comando")
    texto = comando.get_text()
    w.write(texto+"\n")
    w.flush()

def gtk_main_quit(*args):
    gtk.main_quit()

xml.signal_autoconnect(locals())

gtk.main()
