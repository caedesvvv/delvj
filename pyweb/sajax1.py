#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()
import os
import sys
import datetime
import urllib

print "Content-type: text/html"

sajax_debug_mode = False
sajax_export_list = {}
sajax_js_has_been_shown = False

form = cgi.FieldStorage()

def sajax_init():
   pass
   
def sajax_handle_client_request():
   func_name = form.getfirst('rs')
   if func_name is None:
      return
      
   # Bust cache in the head
   print "Expires: Mon, 26 Jul 1997 05:00:00 GMT"  
   print "Last-Modified: %s GMT" % datetime.datetime.utcnow().strftime(
                                                      "%a, %d %m %H:%M:%S")
   # always modified
   print "Cache-Control: no-cache, must-revalidate" # HTTP/1.1
   print "Pragma: no-cache"                         # HTTP/1.0
   print
   
   if not func_name in sajax_export_list:
      print "-:%s not callable" % func_name
   else:
      print "+:",
      rsargs = form.getlist('rsargs[]')
      result = sajax_export_list[func_name](*rsargs)
      print result
   sys.exit()
      
def sajax_get_common_js():
   sajax_debug_modeJS = str(sajax_debug_mode).lower()
   return """\
                // remote scripting library
		// (c) copyright 2005 modernmethod, inc
		var sajax_debug_mode = %(sajax_debug_modeJS)s;
		
		function sajax_debug(text) {
			if (sajax_debug_mode)
				alert("RSD: " + text)
		}
		
 		function sajax_init_object() {
 			sajax_debug("sajax_init_object() called..")
 			
 			var A;
			try {
				A=new ActiveXObject("Msxml2.XMLHTTP");
			} catch (e) {
				try {
					A=new ActiveXObject("Microsoft.XMLHTTP");
				} catch (oc) {
					A=null;
				}
			}
			if(!A && typeof XMLHttpRequest != "undefined")
				A = new XMLHttpRequest();
			if (!A)
				sajax_debug("Could not create connection object.");
			return A;
		}
		function sajax_do_call(func_name, url, args) {
			var i, x, n;
			for (i = 0; i < args.length-1; i++) 
				url = url + "&rsargs[]=" + escape(args[i]);
			url = url + "&rsrnd=" + new Date().getTime();
			x = sajax_init_object();
			x.open("GET", url, true);
			x.onreadystatechange = function() {
				if (x.readyState != 4) 
					return;
				sajax_debug("received " + x.responseText);
				
				var status;
				var data;
				status = x.responseText.charAt(0);
				data = x.responseText.substring(2);
				if (status == "-") 
					alert("Error: " + data);
				else  
					args[args.length-1](data);
			}
			x.send(null);
			sajax_debug(func_name + " url = " + url);
			sajax_debug(func_name + " waiting..");
			delete x;
		}                
   """ % locals()

def sajax_show_common_js():
   print sajax_get_common_js()

def sajax_esc(val):
   return val.replace('"', '\\\\"')	

def sajax_get_one_stub(func_name):
   uri = os.environ['SCRIPT_NAME']
   if os.environ.has_key('QUERY_STRING'):
      uri += "?" + os.environ['QUERY_STRING'] + "&rs=%s" % urllib.quote_plus(func_name)
   else:
      uri += "?rs=%s" % urllib.quote_plus(func_name)
      
   escapeduri = sajax_esc(uri)
   return """
   // wrapper for %(func_name)s
   function x_%(func_name)s(){
      // count args; build URL
      
      sajax_do_call("%(func_name)s",
                    "%(escapeduri)s",
                    x_%(func_name)s.arguments);
      }
      
      """ % locals()

def sajax_show_one_stub(func_name):
   print sajax_get_one_stub(func_name)

def sajax_export(*args):
   decorated = [(f.func_name, f) for f in args]
   sajax_export_list.update(dict(decorated))
     
def sajax_get_javascript():
   global sajax_js_has_been_shown

   html = ''
   if not sajax_js_has_been_shown:
      html += sajax_get_common_js()
      sajax_js_has_been_shown = True
   
   for func_name in sajax_export_list.iterkeys():
      html += sajax_get_one_stub(func_name)

   return html

def sajax_show_javascript():
   print sajax_get_javascript()
