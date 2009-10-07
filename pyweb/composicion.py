#!/usr/bin/env python
import cgitb;cgitb.enable()
import sajax1
pureosc=False
from ajaxosc import *

#lista provisional
controls=[]

load_osc_mapping(osc_definition_file)
i = 0
for a in controls_osc:
	controls.append(i)
	i=i+1

# SAJAX FUNCTIONS
sajax1.sajax_init()
sajax1.sajax_export(move)
sajax1.sajax_export(show_osc_mapping)
sajax1.sajax_handle_client_request()

# HEAD
print """
<html>
<head>
	<title>%s</title>
	<script type="text/javascript" src="/js/range.js"></script>
	<script type="text/javascript" src="/js/timer.js"></script>
	<script type="text/javascript" src="/js/slider.js"></script>
	<link type="text/css" rel="StyleSheet" href="/css/winclassic.css" />
	<link rel="stylesheet" href="%s" type="text/css">
	<script>
	function do_slider(obj,id,min,max) {
		range=max-min
		val=min+(document.getElementById(obj).value*range/100)
		x_move(val,id,do_move_cb_dummy);
		document.getElementById('value_'+id).value=val;
	}
	function do_value(obj,id) {
		val=document.getElementById(obj).value
		x_move(val,id,do_move_cb_dummy);
		document.getElementById(obj).value=val;
	}
	function do_checkbox(obj,id) {
	    if (document.getElementById(obj).checked)
	    {
		x_move(1,id,do_move_cb_dummy);
	    }
	    else
	    {
		x_move(0,id,do_move_cb_dummy);
	    }
	}
	function do_move_cb_dummy(val) {
		document.getElementById("debug").innerHTML = "<p>"+val+"</p>";
	}
""" % (web_title,web_style)
sajax1.sajax_show_javascript()
# PREPARE ALL SLIDERS
print """
	function prepare_slider(id) {
		var s = new Slider(document.getElementById("slider-"+id),
			document.getElementById("slider-input-"+id));
		return s
	}
	function prepare_all() {
      """
for id in controls:
	print """
	   if (document.getElementById("slider-%s")) {
	     var s%s = prepare_slider(%s);
	     s%s.onchange = function () {
	     	do_slider('slider-input-%s',%s,%s,%s);
	     }
	   }

	""" %(id,id,id,id,id,id,controls_osc[id][2],controls_osc[id][3])

print """
	}
	function show_osc_mapping_cb(new_data) {
		document.getElementById("cuadro").innerHTML = new_data;
		document.getElementById("debug").innerHTML = "<p>debug</p>";
		prepare_all();
	}
"""
# SERVER CODE
#for a in controls:
#	print_ajax_callback(a)
print """
	</script>
</head>
"""

# BODY
print """
<body>
	<h1>%s</h1>
	<img src="/php-push.php" />
""" % (web_text_title)
print "<div class='cuadro'>"
print "<p>"
print "composicion"
print "<a href='efectos.py'>efectos</a>"
print "<a href='videos.py'>videos</a>"
print "<a href='imagenes.py'>imagenes</a>"
print "</p>"
print "<div id='cuadro'>"
# CONTROLS
print print_osc_tree()
print """
	</div>
	<div id="debug">
	</div>
	</div>
</body>
</html>
""" % locals()
