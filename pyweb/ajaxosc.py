from config import *
import socket

global position
position="/"
global controls_osc
controls_osc=[]

def envia(mes,pars):
	sudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sudp.connect(('',8666))
	for par in pars:
		mes=mes+" %s"%(par)
	mes+="\n"
	sudp.send(mes)
	sudp.close()

def load_osc_mapping(file):
	global controls_osc
	f=open(file,"r")
	multiplicator=[]
	for a in f.readlines():
	    a=a.strip()
	    if a.startswith("#"):
	    	pass
	    if a.startswith("["):
	    	a=a.strip("[]")
		multiplicator=a.split(",")
	    else:
		temp=a.split(",")
		if len(temp)>1:
		    if len(temp)==2:
		    	temp=temp+[0.0,1.0]
		    if (temp[0].find("*") == -1):
		    	controls_osc.append(temp)
		    else:
		    	for code in multiplicator:
				subst = temp[0].replace("*",code)
		    		controls_osc.append([subst]+temp[1:])
	f.close()

def filter_osc_mapping(curr_position):
	new_controls_osc=[]
	for a in controls_osc:
		if a[0].startswith(curr_position):
			temp=a[0][len(curr_position):]
			if temp.find("/")==-1:
				new_controls_osc.append(a)
	return new_controls_osc
	
def filter_get_children(curr_position):
	new_controls_osc=[]
	for a in controls_osc:
		if a[0].startswith(curr_position):
			temp=a[0][len(curr_position):]
			if temp.find("/")==-1:
				pass
			else:
				temp=temp[:temp.find("/")]
				if temp not in new_controls_osc:
					new_controls_osc.append(temp)
	return new_controls_osc
def html_content(id):
	text=""
	id = int(id)
	name = controls_osc[id][0]
	type = controls_osc[id][1]
	name=name[name.rfind("/")+1:]
	text= "<tr><td>%s</td>"%(name)
	if type == "f":
		text=text+'<td></td><td><input type="text" value="0" size="3" id="value_%s" name="value_%s"\n'%(id,id)
		text=text+'	onchange="do_value('+"'value_"+str(id)+"'"+',%s);"></td>\n'%(id)
		text=text+"<td>"+"""
		<div class="slider" id="slider-%s" tabIndex="1">
		   <input class="slider-input" id="slider-input-%s" name="slider-input-%s" onchange="do_slider('slider-input-%s',%s);"/>
		 </div>
""" % (id,id,id,id,id)
		text=text+"""
		 <script type="text/javascript">
		 var s = new Slider(document.getElementById("slider-%s"), document.getElementById("slider-input-%s"));
		    </script>
		<td></tr>\n""" %(id,id)
	elif type == "fa":
		text=text+'<td></td><td><input type="text" value="0" size="3" id="value_%s" name="value_%s"\n'%(id,id)
		text=text+'	onchange="do_value('+"'value_"+str(id)+"'"+',%s);"></td>\n'%(id)
		text=text+"<td><img align='right' name='thumb_%s' src='/images/sliderthumb.gif' width='22' height='35' alt=''>\n"%(id)
		text=text+"<img align='right' name='track_%s' src='/images/track.gif' width='94' height='35' alt=''><td></tr>\n"%(id)
	elif type == "b":
		text=text+'<td></td><td><input type="checkbox" id="toggle_%s" name="toggle_%s"\n'%(id,id)
		text=text+'	onClick="do_checkbox('+"'toggle_"+str(id)+"'"+',%s);"></td></tr>\n'%(id)
	elif type == "B":
		text=text+'<td></td><td><input type="button" name="button_%s" value="%s"\n'%(id,name)
		text=text+'	onclick="x_move(1,%s,do_move_cb_dummy); return false;"></td></tr>\n'%(id)
	elif type == "t":
		text=text+'<td></td><td><input type="text" value="0" size="3" id="value_%s" name="value_%s"\n'%(id,id)
		text=text+'	onchange="do_value('+"'value_"+str(id)+"'"+',%s);"></td></tr>\n'%(id)
	return text

def draw_controls():
	text="<table>\n"
	selected_controls=filter_osc_mapping(position)
	for a in controls_osc:
		if a in selected_controls:
			text=text+html_content(controls_osc.index(a))
	text=text+"</table>\n"
	return text
def print_osc_tree_x():
	text= "<p>OSC TREE</p>\n"
	text= ""
	tokens=position.split("/")
	partaddress="/"
	name = position[position.rfind("/")+1:]
	empties=0
	for token in tokens:
	    if empties>0 and token==name:
	    	pass
	    else:
		text=text+"<p>"
	    	if token=="":
			empties=empties+1
		else:
			partaddress=partaddress+token+"/"
		text=text+"<b>"+partaddress+"</b>: "
		for a in filter_get_children(partaddress):
			text=text+ "<a href='javascript:x_show_osc_mapping("+'"'+partaddress+a+'/"'+",show_osc_mapping_cb);'>"+a+"</a> | \n"
		text=text+"</p>"
	return text

def print_osc_tree():
	text= "<p>OSC TREE</p>\n"
	text= ""
	tokens=position.split("/")
	partaddress="/"
	name = position[position.rfind("/")+1:]
	empties=0
	for token in tokens:
	    if empties>0 and token==name:
	    	pass
	    else:
		text=text+"<p>"
	    	if token=="":
			empties=empties+1
		else:
			partaddress=partaddress+token+"/"
		text=text+"<b>"+partaddress+"</b>: "
		for a in filter_get_children(partaddress):
			text=text+ "<a href='javascript:x_show_osc_mapping("+'"'+partaddress+a+'/"'+",show_osc_mapping_cb);'>"+a+"</a> | \n"
		text=text+"</p>"
	return text
def show_osc_mapping(new_position):
	global position
	position=new_position
	text = print_osc_tree()
	text = text + draw_controls()
	return text

def move(x,id):
   id = int(id)
   type = controls_osc[id][1]
   try:
      int_id=int(id)
      address=controls_osc[int_id][0]
      if type=="f":
        float_x = float(x)
      	envia(address,[float_x])
      elif type=="b":
        int_x = int(x)
      	envia(address,[int_x])
      elif type=="B":
      	envia(address,[])
      elif type=="t":
      	envia(address,[x])
   except:
      return 0
   return x

def print_ajax_callback(id):
	id = int(id)
	type = controls_osc[id][1]
	if type=='f':
		print "function do_move_cb_%s(val) {"%(id)
		print "	document.getElementById('value_%s').value = val;"%(id)
		print "}"


