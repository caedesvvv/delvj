<head>
<link rel="stylesheet" type="text/css" charset="iso-8859-1" media="all" href="/estilos/madhack.css">
</head>
<?php
echo"<table border=0 cellspacing=0 cellpadding=3 width=90% align=center>";
echo"<tr bgcolor=#BCBFFF><td align=left><h1><a href='filexplore.php'>ADMINISTRACION</a></h1><td><td align=right></td></tr>";
echo"<tr><td> </td><td> </td></tr>";
echo"</table>";
?>
<center>
<table>
<tr><td>
General:<br/>
<a href="admin.php?mes=start">Arrancar</a><br/>
<a href="admin.php?mes=stop">Parar</a><br/>

<br/><br/>
Streaming:<br/>
<?php
if($mes=="start")
{
	exec("delvj");
	}
if($mes=="stop")
	exec("killall -9 pd");
if($mes=="stream")
	$textop=str_replace(" ","%32",$texto);
	send_pd("102 location ".$streamlocation);

?>
<?
function send_pd($mensaje)
{
	$socket=socket_create(AF_INET,SOCK_DGRAM,getprotobyname("udp"));
	$fmensaje = $mensaje."\n";
	socket_sendto($socket,$fmensaje,strlen($fmensaje),0x100,"localhost",8666);
}
?>

<form action="send.php">
<input type="hidden" name="mes" value="texto">
<input type="text" name=texto><br/>
x: <input type="number" name=tx size=3 value=160>
y: <input type="number" name=ty size=3 value=120>
<input type="submit" value="Enviar">
</form>
</center>
<br/><br/>
