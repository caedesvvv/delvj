<head>
<link rel="stylesheet" type="text/css" charset="iso-8859-1" media="all" href="/estilos/madhack.css">
</head>
<?php
$mes = $_GET["mes"];
$cod = $_GET["cod"];
$texto = $_GET["texto"];
$beats = $_GET["beats"];
echo"<table border=0 cellspacing=0 cellpadding=3 width=90% align=center>";
echo"<tr bgcolor=#BCBFFF><td align=left><h1><a href='filexplore.php'>CAMBIO DE VIDEOS</a></h1><td><td align=right><h1>EFECTOS</h1></td></tr>";
echo"<tr><td> </td><td> </td></tr>";
echo"</table>";
?>
<center>
<table>
<tr><td>
<h3>Efectos:</h3>
<a href="send.php?mes=zoom" alt="Zoom" title="Zoom"><img src="images/intrusion.png"/></a>Zoom <a href="send.php?mes=zoom&cod=1">on</a> <a href="send.php?mes=zoom&cod=0">off</a><br/>
<a href="send.php?mes=ascii" alt="Ascii" title="Ascii"><img src="images/ascii.png"/></a>Ascii <a href="send.php?mes=ascii&cod=1">on</a> <a href="send.php?mes=ascii&cod=0">off</a><br/>
<a href="send.php?mes=dice" alt="Dados" title="Dados"><img src="images/dice.png"/></a>Dados  <a href="send.php?mes=dice&cod=1">on</a> <a href="send.php?mes=dice&cod=0">off</a><br/>
<a href="send.php?mes=rotate" alt="Rotar" title="Rotar"><img src="images/cycle.png"/></a>Rotar <a href="send.php?mes=rotate&cod=1">on</a> <a href="send.php?mes=rotate&cod=0">off</a><br/>
<a href="send.php?mes=simura" alt="Simura" title="Simura"><img src="images/simura.png"/></a>Simura  <a href="send.php?mes=simura&cod=1">on</a> <a href="send.php?mes=simura&cod=0">off</a><br/>
<a href="send.php?mes=motionphase" alt="Eco de Movimiento" title="Eco de Movimiento"><img src="images/motionphase.png"/></a> Eco de Movimiento <a href="send.php?mes=motionphase&cod=1">on</a> <a href="send.php?mes=motionphase&cod=0">off</a><br/>
<a href="send.php?mes=motionblur" alt="Blur de Movimiento" title="Blur de Movimiento"><img src="images/motionfade.png"/></a> Blur de Movimiento <a href="send.php?mes=motionblur&cod=1">on</a> <a href="send.php?mes=motionblur&cod=0">off</a><br/>
<a href="send.php?mes=contrast" alt="Contraste" title="Contraste"><img src="images/contrast.png"/></a> Contraste <a href="send.php?mes=contrast&cod=1">on</a> <a href="send.php?mes=contrast&cod=0">off</a><br/><br/>
<h3>Darle Ritmo:</h3>
<a href="send.php?mes=verde"><img src="images/pdverde.png"/></a> 
<a href="send.php?mes=rojo"><img src="images/pdrojo.png"/></a> 
<a href="send.php?mes=azul"><img src="images/pdazul.png"/></a><br/>

<br/><br/>
<h3>Escribir Texto:</h3>
<?php
if($mes=="zoom")
{
	send_pd("1 $cod");
	}
if($mes=="ascii")
	send_pd("2 $cod");
if($mes=="dice")
	send_pd("3 $cod");
if($mes=="rotate")
	send_pd("4 $cod");
if($mes=="simura")
	send_pd("5 $cod");
if($mes=="motionphase")
	send_pd("6 $cod");
if($mes=="motionblur")
	send_pd("7 $cod");
if($mes=="contrast")
	send_pd("8 $cod");
if($mes=="videoch")
	send_pd("9 $cod");
if($mes=="autochan1")
	send_pd("10 $cod");
if($mes=="autochan2")
	send_pd("11 $cod");
if($mes=="chan1num")
	send_pd("40 $beats");
if($mes=="chan2num")
	send_pd("41 $beats");
if($mes=="rojo")
	send_pd("21 bang");
if($mes=="verde")
	send_pd("20 bang");
if($mes=="azul")
	send_pd("22 bang");
if($mes=="texto")
{
	$textop=str_replace(" ","%32",$texto);
	send_pd("30 text ".$textop." $tx $ty");
}

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
<h3>Automatización videos:</h3>
<a href="send.php?mes=autochan1" alt="Canal 1 Auto" title="Canal 1 Auto"><img src="images/contrast.png"/></a> Canal 1 Auto <a href="send.php?mes=autochan1&cod=1">on</a> <a href="send.php?mes=autochan1&cod=0">off</a>
<form action="send.php">
<input type="hidden" name="mes" value="chan1num">
<input type="number" name=beats size=3 value=10>
nº de golpes
</form>
<a href="send.php?mes=autochan2" alt="Canal 2 Auto" title="Canal 1 Auto"><img src="images/contrast.png"/></a> Canal 2 Auto <a href="send.php?mes=autochan2&cod=1">on</a> <a href="send.php?mes=autochan2&cod=0">off</a><br/>
<form action="send.php">
<input type="hidden" name="mes" value="chan2num">
<input type="number" name=beats size=3 value=20>
nº de golpes
</form>
<a href="send.php?mes=videoch" alt="Cambio de Videos Inteligente" title="Cambio de Videos Inteligente"><img src="images/bitdepth.png"/></a> Cambio de Video Inteligente <a href="send.php?mes=videoch&cod=1">on</a> <a href="send.php?mes=videoch&cod=0">off</a><br/><br/>
</td></tr></table>
<br/><br/>
