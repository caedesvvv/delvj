<head>
<link rel="stylesheet" type="text/css" charset="iso-8859-1" media="all" href="/estilos/madhack.css">
</head>

<?php
//specify your starting directory.
//aquí pones la carpeta principal de loops de video
$root="/home/caedes/LOOPSV/";
$directory = $_GET["directory"];
$file = $_GET["file"];
$case = $_GET["case"];
if ($directory=="") {
    $directory="/";
}
$diref=substr_count($directory,"/");
if($diref>=2) {
    $dirin=explode("/",$directory);
    $diroldcount=strlen($dirin[$diref-1])+1;
}
$oldir=substr($directory,0,-$diroldcount);

function envia_pd($mensaje)
{
	$socket=socket_create(AF_INET,SOCK_DGRAM,getprotobyname("udp"));
	$fmensaje = $mensaje."\n";
	socket_sendto($socket,$fmensaje,strlen($fmensaje),0x100,"localhost",8666 );
}

if($case=="Launch1")
{
	envia_pd("100 symbol ".$file);
	envia_pd("31 location ".$root . $directory);
}
if($case=="Launch2")
{
	envia_pd("200 symbol ".$file);
	envia_pd("32 location ".$root . $directory);
}

if($directory) {
    function dirsize($newdir) {
        $dh=opendir($newdir);
        $size=0;
        while(($newfile=readdir($dh))<>false)
            if($newfile<>"." and $newfile<>"..") {
                $path=$newdir."/".$newfile;
                if(is_dir($path))
                    $size+=dirsize($path);
                elseif(is_file($path))
                    $size+=filesize($path);
            }  
        closedir($dh);
        return $size;
    }
    function filetime($tm) {
        $time=filemtime($tm);
        $yr=date("Y",$time);
        $mo=date("M",$time);
        $da=date("d",$time);
        $realt=$mo."."." ".$da.","." ".$yr;
        return $realt;
    }
    if ($dir=@opendir($root.$directory))
        $dirbuff=array("0"=>"");
    $filebuff=$dirbuff;
    $fzbuff=$dirbuff;
    $dzbuff=$dirbuff;
    while ($file=readdir($dir)) {  
        $file_size=filesize($root.$directory.$file);
        $totalfile=$totalfile+$file_size;
        if($file=="."||$file=="..") {
        }
        else
        {
            if (ereg("([.]{1})",$file,$regs)) {//6
                $filcount=$filcount+1;
                array_push($filebuff,$file);
                array_push($fzbuff,$file_size);
            }//6
            else {//6
                $dircount=$dircount+1;
                array_push($dirbuff,$file);
                array_push($dzbuff,$file_size);
            }//6
        }
    }
    closedir($dir);
}

echo"<form method=post action=$PHP_SELF?directory=\"$directory\">";
echo"<table border=0 cellspacing=0 cellpadding=3 width=90% align=center>";
echo"<tr bgcolor=#BCBFFF><td align=left><h1>CAMBIO DE VIDEOS</h1><td><td align=right><h1><a href='send.php'>EFECTOS</a></h1></td></tr>";
echo"<tr><td> </td><td> </td></tr>";
echo"</table>";
//echo"<table border=0 cellsapcing=0 cellpadding=2 width=90% align=center>";
//echo"<tr bgcolor=#008888><td colspan=6><font face=arial><b>Selector de Videos</b>         </font><font face=arial color=green><b>El directorio actual es $root$directory</b></font></td></tr>";
//echo"</table>";
echo"<table border=0 cellspacing=0 cellpadding=2 width=90% align=center>";
if($oldir!=="") {
    echo"<tr bgcolor=#F5F5DC><td width=12> </td><td><a href=filexplore.php?directory=$oldir><img src=images/folder.png border=0></a></td><td><a href=filexplore.php?directory=$oldir><font face=arial>Subir al directorio anterior</font></a></td><td> </td><td align=right> </td><td></td></tr>";
    echo"<tr bgcolor=#FAEBD7><td width=12> </td><td></td><td><font face=arial size=1><b>Directorio Actual</b></font></td><td><font face=arial size=1><b>\"$directory\"</b></font></td><td></td><td></td></tr>";
}
echo"<tr bgcolor=#BCBFFF background=/icons/bg.gif><td with=12> </td><td width=12> </td><td><font face=arial size=3><strong>Nombre</strong></font></td><td> </td><td><font face=arial size=3><strong>Fecha</strong></font></td><td align=right><font face=arial size=3><strong>Tamaño (bytes)</strong></font></td></tr>";
for($vel=1;$vel<=$dircount;$vel++) {
    $count=$count+1;
    $sum=$count+1;
    $bg=$sum/2;
    $col=floor($bg);
    $ras=$bg-$col;
    if($ras==0) {
        $me="CCCCCC";
    }
    else {
     $me="DDDDDD";
    }
    print"<tr bgcolor=#".$me."><td>  </td><td width=25><a href=filexplore.php?directory=".$directory.$dirbuff[$vel]."/><img src=images/folders.png border=0></a></td><td><a href=filexplore.php?directory=".$directory.$dirbuff[$vel]."/><font face=arial>".$dirbuff[$vel]."</font></a></td><td> </td><td>".filetime($root.$directory.$file.$dirbuff[$vel])."</td><td align=right><font face=arial>".dirsize($root.$directory.$file.$dirbuff[$vel])." bytes</font></td></tr>";
}  
for($vol=1;$vol<=$filcount;$vol++) {
    $edtimg=" ";
    $count1=$count1+1;
    if($ras==0) {
        $sum1=$count1+2;
    }
    else {
        $sum1=$count1+1;
    }
    $bg1=$sum1/2;
    $col1=floor($bg1);
    $ras1=$bg1-$col1;
    if($ras1==0) {
     $mel="CCCCCC";
    }
     else {
     $mel="DDDDDD";
    }  
    //$spltfile=explode(".",$filebuff[$vol]);
    //if(($spltfile[1]=="htm")||($spltfile[1]=="html")||($spltfile[1]<>"")) {
    //    $edtimg="<a href=filexplore.php?directory=$directory&case=Edit&cfile=$filebuff[$vol]><img src=/profile/edit_code.gif border=\"0\"></a>";
    //}
    print"<tr bgcolor=#".$mel."><td width=12></td><td><img src='thumbsvideo/".$filebuff[$vol]."' width=32 height=24></td><td><font face=arial>".$filebuff[$vol]."</font></td><td><a href=filexplore.php?file=".$root.$directory.$filebuff[$vol]."&case=Launch1&directory=$directory ><font face=arial>lanzar 1</font></a> | <a href=filexplore.php?file=".$root.$directory.$filebuff[$vol]."&case=Launch2&directory=$directory><font face=arial>lanzar 2</font></a></td><td>".filetime($root.$directory."".$file."".$filebuff[$vol])." <td align=right><font face=arial size=2>".  $fzbuff[$vol]." bytes</font></td></tr>";
}
print"<tr background=/icons/bg.gif><td width=12></td><td width=12> </td><td> </td><td></td><td><font face=arial><strong>Bytes en total</strong></font></td><td align=right><font face=arial color=blue><strong>".dirsize($root.$directory.$file.$dirbuff[$vel])." bytes</strong></font></td></tr";
echo"</table>";
//echo"<table border=0 cellsapcing=0 cellpadding=2 width=90% align=center>";
//echo"<tr bgcolor=#008888><td colspan=6><font face=arial><b>Selector de videos</b>         </font><font face=arial color=green><b>El directorio actual es $root$directory</b></font></td></tr>";
//echo"</table>";
?> 
